"""本地RAG实现 - 使用ChromaDB和本地embeddings
Local RAG implementation - Uses ChromaDB and local embeddings
No cloud storage, no size limits, all data stored locally
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types
import PyPDF2
import docx

from src.utils.logger import setup_logger
from src.utils.excel_handler import ExcelHandler

logger = setup_logger(__name__)


class LocalRAG:
    """
    完全本地化的RAG系统
    Fully local RAG system with no cloud dependencies

    Features:
    - Local vector database (ChromaDB)
    - Local embeddings (sentence-transformers)
    - No size limits
    - All data stored locally
    - Can still use Gemini API for generation (only query, not storage)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = "gemini-2.5-flash",
        persist_directory: str = "./chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        初始化本地RAG系统
        Initialize local RAG system

        Args:
            api_key: Google API key for generation (optional)
            default_model: Gemini model for text generation
            persist_directory: Local directory to store vector database
            embedding_model: Sentence transformer model for embeddings
        """
        # Setup Gemini client for text generation only
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.default_model = default_model
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("No API key provided. Will only support embedding and search.")

        # Setup local embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)

        # Setup ChromaDB (local vector database)
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)

        self.chroma_client = chromadb.Client(Settings(
            persist_directory=str(self.persist_directory),
            anonymized_telemetry=False
        ))

        logger.info(f"Local RAG initialized. Database: {self.persist_directory}")

    def create_collection(self, name: str, metadata: Optional[Dict] = None) -> str:
        """
        创建本地collection（类似Google的store）
        Create local collection (similar to Google's store)

        Args:
            name: Collection name
            metadata: Optional metadata

        Returns:
            Collection name
        """
        try:
            collection = self.chroma_client.create_collection(
                name=name,
                metadata=metadata or {}
            )
            logger.info(f"Created collection: {name}")
            return name
        except Exception as e:
            # Collection might already exist
            logger.info(f"Collection {name} already exists or error: {e}")
            return name

    def list_collections(self) -> List[Dict[str, Any]]:
        """
        列出所有本地collections
        List all local collections
        """
        collections = self.chroma_client.list_collections()
        return [
            {
                'name': col.name,
                'metadata': col.metadata,
                'count': col.count()
            }
            for col in collections
        ]

    def _extract_text_from_file(self, file_path: Path) -> str:
        """
        从文件中提取文本
        Extract text from various file types
        """
        suffix = file_path.suffix.lower()

        try:
            if suffix == '.txt' or suffix == '.md':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()

            elif suffix == '.pdf':
                text = []
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text.append(page.extract_text())
                return '\n'.join(text)

            elif suffix == '.docx':
                doc = docx.Document(file_path)
                return '\n'.join([para.text for para in doc.paragraphs])

            elif suffix in ['.xlsx', '.xls']:
                # Use ExcelHandler
                return ExcelHandler.excel_to_structured_text(str(file_path))

            else:
                logger.warning(f"Unsupported file type: {suffix}")
                return ""

        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return ""

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        将文本分块
        Split text into chunks
        """
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)

                if break_point > chunk_size * 0.5:  # At least 50% through
                    chunk = text[start:start + break_point + 1]
                    end = start + break_point + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return [c for c in chunks if c]  # Remove empty chunks

    def upload_file(
        self,
        file_path: Union[str, Path],
        collection_name: str,
        metadata: Optional[Dict[str, str]] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> int:
        """
        上传文件到本地RAG系统
        Upload file to local RAG system

        Args:
            file_path: Path to file
            collection_name: Target collection
            metadata: Optional metadata
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            Number of chunks indexed
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Extract text
        logger.info(f"Extracting text from {file_path.name}")
        text = self._extract_text_from_file(file_path)

        if not text:
            logger.warning(f"No text extracted from {file_path.name}")
            return 0

        # Chunk text
        chunks = self._chunk_text(text, chunk_size, chunk_overlap)
        logger.info(f"Split into {len(chunks)} chunks")

        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.embedding_model.encode(chunks, show_progress_bar=True)

        # Get collection
        collection = self.chroma_client.get_collection(collection_name)

        # Prepare metadata
        base_metadata = metadata or {}
        base_metadata.update({
            'filename': file_path.name,
            'file_type': file_path.suffix,
        })

        # Add to collection
        ids = [f"{file_path.name}_{i}" for i in range(len(chunks))]
        metadatas = [{**base_metadata, 'chunk_id': i} for i in range(len(chunks))]

        collection.add(
            embeddings=embeddings.tolist(),
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

        logger.info(f"Uploaded {len(chunks)} chunks from {file_path.name}")
        return len(chunks)

    def query(
        self,
        question: str,
        collection_name: str,
        n_results: int = 5,
        temperature: float = 0.7,
        use_gemini: bool = True
    ) -> Dict[str, Any]:
        """
        查询本地RAG系统
        Query local RAG system

        Args:
            question: User question
            collection_name: Collection to search
            n_results: Number of relevant chunks to retrieve
            temperature: Generation temperature
            use_gemini: Whether to use Gemini for generation

        Returns:
            Dict with answer, sources, and metadata
        """
        # Get collection
        collection = self.chroma_client.get_collection(collection_name)

        # Generate query embedding
        query_embedding = self.embedding_model.encode([question])[0]

        # Search similar chunks
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )

        # Extract documents and metadata
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []

        # Build context from retrieved documents
        context = "\n\n---\n\n".join([
            f"[Source: {meta.get('filename', 'Unknown')}]\n{doc}"
            for doc, meta in zip(documents, metadatas)
        ])

        # Generate answer
        if use_gemini and self.client:
            # Use Gemini for generation
            prompt = f"""Based on the following context, answer the question. If the answer is not in the context, say so.

Context:
{context}

Question: {question}

Answer:"""

            response = self.client.models.generate_content(
                model=self.default_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                )
            )

            answer = response.text if hasattr(response, 'text') else str(response)
        else:
            # Simple concatenation without generation
            answer = f"Found {len(documents)} relevant passages:\n\n{context}"

        # Format sources
        sources = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            sources.append({
                'filename': meta.get('filename', 'Unknown'),
                'chunk_id': meta.get('chunk_id', 0),
                'text': doc[:200] + '...' if len(doc) > 200 else doc,
                'distance': float(dist),
                'metadata': meta
            })

        return {
            'answer': answer,
            'sources': sources,
            'n_sources': len(sources),
            'context': context
        }

    def delete_collection(self, collection_name: str):
        """删除collection / Delete collection"""
        try:
            self.chroma_client.delete_collection(collection_name)
            logger.info(f"Deleted collection: {collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise

    def get_stats(self) -> Dict[str, Any]:
        """
        获取系统统计信息
        Get system statistics
        """
        collections = self.list_collections()
        total_docs = sum(c['count'] for c in collections)

        db_size = sum(
            f.stat().st_size
            for f in self.persist_directory.rglob('*')
            if f.is_file()
        )

        return {
            'collections': len(collections),
            'total_documents': total_docs,
            'database_size_mb': db_size / (1024 * 1024),
            'persist_directory': str(self.persist_directory),
            'collections_detail': collections
        }
