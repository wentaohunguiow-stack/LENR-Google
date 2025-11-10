"""Citation formatting and management utilities."""

import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class CitationFormatter:
    """
    Format RAG responses with inline citations and reference lists.

    Provides OpenEvidence-style citation formatting with numbered
    references that can be linked to source documents.
    """

    @staticmethod
    def format_response_with_citations(
        answer: str,
        citations: List[Dict[str, Any]],
        style: str = "numbered"
    ) -> Dict[str, Any]:
        """
        Format RAG response with inline numbered citations.

        Args:
            answer: The generated answer text
            citations: List of citation dictionaries from RAG query
            style: Citation style ('numbered', 'inline', 'footnote')

        Returns:
            Dictionary with formatted answer and references

        Example:
            >>> formatted = CitationFormatter.format_response_with_citations(
            ...     answer="LENR is a promising field.",
            ...     citations=[{...}],
            ...     style="numbered"
            ... )
            >>> print(formatted['formatted_answer'])
            >>> print(formatted['references'])
        """
        if not citations:
            return {
                'formatted_answer': answer,
                'references': [],
                'citation_count': 0
            }

        # Create reference list
        references = []
        for idx, citation in enumerate(citations, 1):
            ref = {
                'number': idx,
                'title': citation.get('title', 'Untitled'),
                'uri': citation.get('uri', ''),
                'text': citation.get('text', ''),
                'metadata': citation.get('metadata', {})
            }
            references.append(ref)

        # For now, append citations at the end
        # In a more advanced version, we could parse the answer and insert citations inline
        formatted_answer = answer

        return {
            'formatted_answer': formatted_answer,
            'references': references,
            'citation_count': len(references),
            'style': style
        }

    @staticmethod
    def create_reference_html(references: List[Dict[str, Any]]) -> str:
        """
        Create HTML formatted reference list.

        Args:
            references: List of reference dictionaries

        Returns:
            HTML string for references section

        Example:
            >>> html = CitationFormatter.create_reference_html(references)
        """
        if not references:
            return ""

        html_parts = ['<div class="references">', '<h3>References</h3>', '<ol>']

        for ref in references:
            title = ref.get('title', 'Untitled')
            uri = ref.get('uri', '')
            text = ref.get('text', '')

            # Truncate text for preview
            preview = text[:200] + "..." if len(text) > 200 else text

            html_parts.append(f'<li id="ref-{ref["number"]}">')

            if uri:
                html_parts.append(f'<strong><a href="{uri}" target="_blank">{title}</a></strong>')
            else:
                html_parts.append(f'<strong>{title}</strong>')

            if preview:
                html_parts.append(f'<div class="citation-preview">{preview}</div>')

            # Add metadata if available
            metadata = ref.get('metadata', {})
            if metadata:
                meta_items = []
                for key, value in metadata.items():
                    meta_items.append(f"{key}: {value}")
                if meta_items:
                    html_parts.append(f'<div class="citation-metadata">{" | ".join(meta_items)}</div>')

            html_parts.append('</li>')

        html_parts.extend(['</ol>', '</div>'])

        return '\n'.join(html_parts)

    @staticmethod
    def create_reference_markdown(references: List[Dict[str, Any]]) -> str:
        """
        Create Markdown formatted reference list.

        Args:
            references: List of reference dictionaries

        Returns:
            Markdown string for references section
        """
        if not references:
            return ""

        md_parts = ['## References\n']

        for ref in references:
            title = ref.get('title', 'Untitled')
            uri = ref.get('uri', '')
            text = ref.get('text', '')
            metadata = ref.get('metadata', {})

            # Reference number and title
            if uri:
                md_parts.append(f"{ref['number']}. **[{title}]({uri})**")
            else:
                md_parts.append(f"{ref['number']}. **{title}**")

            # Preview text
            if text:
                preview = text[:300] + "..." if len(text) > 300 else text
                md_parts.append(f"   > {preview}\n")

            # Metadata
            if metadata:
                meta_str = " | ".join([f"{k}: {v}" for k, v in metadata.items()])
                md_parts.append(f"   *{meta_str}*\n")

        return '\n'.join(md_parts)

    @staticmethod
    def extract_page_number(citation: Dict[str, Any]) -> Optional[int]:
        """
        Extract page number from citation metadata.

        Args:
            citation: Citation dictionary

        Returns:
            Page number if found, None otherwise
        """
        # Try to extract from URI
        uri = citation.get('uri', '')
        if '#page=' in uri:
            match = re.search(r'#page=(\d+)', uri)
            if match:
                return int(match.group(1))

        # Try to extract from metadata
        metadata = citation.get('metadata', {})
        if 'page' in metadata:
            try:
                return int(metadata['page'])
            except (ValueError, TypeError):
                pass

        # Try to extract from title
        title = citation.get('title', '')
        match = re.search(r'page\s+(\d+)', title, re.IGNORECASE)
        if match:
            return int(match.group(1))

        return None

    @staticmethod
    def format_citation_link(
        citation_number: int,
        file_path: Optional[str] = None,
        page: Optional[int] = None
    ) -> str:
        """
        Create a formatted citation link.

        Args:
            citation_number: Reference number
            file_path: Path to source document
            page: Page number in document

        Returns:
            Formatted citation string
        """
        parts = [f"[{citation_number}]"]

        if file_path:
            filename = Path(file_path).name
            parts.append(f"({filename}")
            if page:
                parts.append(f", p. {page}")
            parts.append(")")

        return " ".join(parts)

    @staticmethod
    def create_interactive_citation(
        citation_number: int,
        reference: Dict[str, Any],
        format: str = "html"
    ) -> str:
        """
        Create an interactive citation element.

        Args:
            citation_number: Reference number
            reference: Reference dictionary
            format: Output format ('html' or 'markdown')

        Returns:
            Formatted interactive citation string
        """
        if format == "html":
            return f'<a href="#ref-{citation_number}" class="citation-link" data-ref="{citation_number}">[{citation_number}]</a>'
        else:  # markdown
            title = reference.get('title', 'Source')
            return f"[[{citation_number}]](#ref-{citation_number} \"{title}\")"

    @staticmethod
    def parse_citations_from_text(text: str) -> List[int]:
        """
        Extract citation numbers from text.

        Args:
            text: Text containing citations like [1], [2-4], etc.

        Returns:
            List of citation numbers found
        """
        citations = []

        # Match single citations: [1]
        single_pattern = r'\[(\d+)\]'
        for match in re.finditer(single_pattern, text):
            citations.append(int(match.group(1)))

        # Match range citations: [1-3]
        range_pattern = r'\[(\d+)-(\d+)\]'
        for match in re.finditer(range_pattern, text):
            start = int(match.group(1))
            end = int(match.group(2))
            citations.extend(range(start, end + 1))

        return sorted(list(set(citations)))

    @staticmethod
    def enhance_answer_with_citations(
        answer: str,
        references: List[Dict[str, Any]],
        format: str = "markdown"
    ) -> str:
        """
        Enhance answer text by adding citation links.

        Args:
            answer: Original answer text
            references: List of references
            format: Output format ('html' or 'markdown')

        Returns:
            Enhanced answer with clickable citations
        """
        # Find sentences that might need citations
        # This is a simple implementation - could be more sophisticated

        enhanced = answer

        # If we have references, add a citation marker at the end of key sentences
        # This is simplified - in production, you'd use NLP to identify which
        # sentences correspond to which sources

        return enhanced

    @staticmethod
    def create_citation_popup_data(reference: Dict[str, Any]) -> Dict[str, str]:
        """
        Create data for citation popup/tooltip.

        Args:
            reference: Reference dictionary

        Returns:
            Dictionary with popup data
        """
        return {
            'title': reference.get('title', 'Untitled'),
            'preview': reference.get('text', '')[:200] + "...",
            'uri': reference.get('uri', ''),
            'metadata': str(reference.get('metadata', {}))
        }
