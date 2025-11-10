"""Document viewing and navigation utilities."""

import base64
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import fitz  # PyMuPDF


class DocumentViewer:
    """
    Handle document viewing and navigation for citation jumping.

    Supports PDF viewing with page navigation and text highlighting.
    """

    @staticmethod
    def get_pdf_page_count(pdf_path: str) -> int:
        """
        Get the number of pages in a PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Number of pages
        """
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        doc.close()
        return page_count

    @staticmethod
    def extract_pdf_page_text(pdf_path: str, page_number: int) -> str:
        """
        Extract text from a specific PDF page.

        Args:
            pdf_path: Path to PDF file
            page_number: Page number (0-indexed)

        Returns:
            Text content of the page
        """
        doc = fitz.open(pdf_path)
        if 0 <= page_number < len(doc):
            page = doc[page_number]
            text = page.get_text()
            doc.close()
            return text
        doc.close()
        return ""

    @staticmethod
    def search_text_in_pdf(pdf_path: str, search_text: str) -> List[Tuple[int, List]]:
        """
        Search for text in PDF and return page numbers and locations.

        Args:
            pdf_path: Path to PDF file
            search_text: Text to search for

        Returns:
            List of tuples (page_number, rectangles) where text was found
        """
        doc = fitz.open(pdf_path)
        results = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text_instances = page.search_for(search_text)
            if text_instances:
                results.append((page_num, text_instances))

        doc.close()
        return results

    @staticmethod
    def render_pdf_page_as_image(
        pdf_path: str,
        page_number: int,
        zoom: float = 2.0
    ) -> bytes:
        """
        Render a PDF page as an image.

        Args:
            pdf_path: Path to PDF file
            page_number: Page number (0-indexed)
            zoom: Zoom factor for rendering

        Returns:
            Image bytes (PNG format)
        """
        doc = fitz.open(pdf_path)
        page = doc[page_number]

        # Render page to image
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # Convert to PNG bytes
        img_bytes = pix.tobytes("png")

        doc.close()
        return img_bytes

    @staticmethod
    def highlight_text_in_pdf_page(
        pdf_path: str,
        page_number: int,
        search_text: str,
        zoom: float = 2.0
    ) -> bytes:
        """
        Render PDF page with highlighted text.

        Args:
            pdf_path: Path to PDF file
            page_number: Page number (0-indexed)
            search_text: Text to highlight
            zoom: Zoom factor

        Returns:
            Image bytes with highlighted text
        """
        doc = fitz.open(pdf_path)
        page = doc[page_number]

        # Search for text
        text_instances = page.search_for(search_text)

        # Highlight found text
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            highlight.update()

        # Render page
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")

        doc.close()
        return img_bytes

    @staticmethod
    def get_pdf_metadata(pdf_path: str) -> Dict[str, str]:
        """
        Extract metadata from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary of metadata
        """
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        doc.close()
        return metadata or {}

    @staticmethod
    def create_pdf_viewer_link(
        pdf_path: str,
        page_number: Optional[int] = None,
        search_text: Optional[str] = None
    ) -> str:
        """
        Create a link to view PDF with optional page and search parameters.

        Args:
            pdf_path: Path to PDF file
            page_number: Page to jump to (1-indexed for display)
            search_text: Text to highlight

        Returns:
            Formatted link string
        """
        link_parts = [f"file://{Path(pdf_path).absolute()}"]

        if page_number is not None:
            link_parts.append(f"#page={page_number}")

        if search_text:
            link_parts.append(f"&search={search_text}")

        return "".join(link_parts)

    @staticmethod
    def encode_pdf_for_display(pdf_path: str) -> str:
        """
        Encode PDF as base64 for embedding in HTML/web.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Base64 encoded PDF string
        """
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        return base64.b64encode(pdf_bytes).decode('utf-8')

    @staticmethod
    def find_citation_in_document(
        file_path: str,
        citation_text: str,
        context_chars: int = 200
    ) -> Optional[Dict[str, any]]:
        """
        Find a citation excerpt in a document and return its location.

        Args:
            file_path: Path to document
            citation_text: Citation text to find
            context_chars: Characters of context to include

        Returns:
            Dictionary with location info or None if not found
        """
        file_path = Path(file_path)

        if file_path.suffix.lower() == '.pdf':
            # Search in PDF
            results = DocumentViewer.search_text_in_pdf(str(file_path), citation_text[:100])

            if results:
                page_num, rectangles = results[0]
                return {
                    'file_path': str(file_path),
                    'page_number': page_num + 1,  # 1-indexed for display
                    'found': True,
                    'location_type': 'pdf_page'
                }

        elif file_path.suffix.lower() in ['.txt', '.md']:
            # Search in text file
            text = file_path.read_text()
            pos = text.find(citation_text[:100])

            if pos != -1:
                # Calculate approximate line number
                line_num = text[:pos].count('\n') + 1

                return {
                    'file_path': str(file_path),
                    'line_number': line_num,
                    'position': pos,
                    'found': True,
                    'location_type': 'text_position'
                }

        return None


class CitationNavigator:
    """
    Navigate between citations and their sources.

    Provides utilities for jumping to citation locations.
    """

    def __init__(self, documents_dir: str):
        """
        Initialize citation navigator.

        Args:
            documents_dir: Directory containing source documents
        """
        self.documents_dir = Path(documents_dir)

    def locate_citation_source(
        self,
        citation: Dict,
        available_files: List[str]
    ) -> Optional[Dict]:
        """
        Locate the source document for a citation.

        Args:
            citation: Citation dictionary from RAG query
            available_files: List of available document paths

        Returns:
            Location information dictionary
        """
        citation_text = citation.get('text', '')
        title = citation.get('title', '')

        # Try to match citation to a document
        for file_path in available_files:
            file_name = Path(file_path).stem.lower()

            # Check if title matches filename
            if title.lower() in file_name or file_name in title.lower():
                # Found potential match - search for exact location
                location = DocumentViewer.find_citation_in_document(
                    file_path,
                    citation_text
                )

                if location:
                    return location

        return None

    def create_navigation_link(self, location: Dict) -> str:
        """
        Create a navigation link for a citation location.

        Args:
            location: Location dictionary from locate_citation_source

        Returns:
            Navigation link string
        """
        if location.get('location_type') == 'pdf_page':
            return DocumentViewer.create_pdf_viewer_link(
                location['file_path'],
                location.get('page_number')
            )
        elif location.get('location_type') == 'text_position':
            return f"file://{location['file_path']}#line={location.get('line_number', 1)}"
        else:
            return f"file://{location.get('file_path', '')}"

    def get_citation_preview(
        self,
        location: Dict,
        context_lines: int = 3
    ) -> str:
        """
        Get a preview of text around a citation location.

        Args:
            location: Location dictionary
            context_lines: Number of context lines to include

        Returns:
            Preview text
        """
        file_path = location.get('file_path')
        if not file_path:
            return ""

        file_path = Path(file_path)

        if location.get('location_type') == 'pdf_page':
            page_num = location.get('page_number', 1) - 1  # 0-indexed
            return DocumentViewer.extract_pdf_page_text(str(file_path), page_num)

        elif location.get('location_type') == 'text_position':
            text = file_path.read_text()
            pos = location.get('position', 0)

            # Extract context around position
            start = max(0, pos - 200)
            end = min(len(text), pos + 200)

            preview = text[start:end]
            if start > 0:
                preview = "..." + preview
            if end < len(text):
                preview = preview + "..."

            return preview

        return ""
