"""
Gemini Smart RAG - Best Gemini Solution
Only Google API key needed, unlimited storage, very low cost
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import PyPDF2
import docx
from google import genai
from google.genai import types
import chromadb
from chromadb.config import Settings
import hashlib
import json
import time

from src.utils.logger import setup_logger
from src.utils.excel_handler import ExcelHandler

logger = setup_logger(__name__)


class GeminiSmartRAG:
    """
    Gemini Smart RAG - Best Solution with Gemini

    Features:
    - Only 1 API key needed (Google/Gemini)
    - Unlimited storage (local ChromaDB)
    - Very low cost (~$0.50-1/month for 1000 queries)
    - Excellent quality (Gemini 2.0 Flash)
    - Easy setup (3 minutes)
    - Easy sharing (export/import database)
    - Fast indexing (local + Gemini embeddings)

    Why use Gemini:
    - Much cheaper than OpenAI
    - Excellent quality (Gemini 2.0)
    - Free embeddings
    - Long context (2M tokens)
    - Multimodal support
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        persist_directory: str = "./gemini_smart_rag_db",
        model: str = "gemini-2.0-flash-exp",
        embedding_model: str = "models/text-embedding-004"
    ):
        """
        Initialize Gemini Smart RAG

        Args:
            api_key: Google API key (only one needed!)
            persist_directory: Where to store the database locally
            model: Gemini model (gemini-2.0-flash-exp recommended)
            embedding_model: Gemini embedding model (text-embedding-004)
        """
        # Get API key
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key required. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter. Get key at: https://aistudio.google.com/apikey"
            )

        # Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)
        self.model = model
        self.embedding_model = embedding_model

        # Initialize local ChromaDB
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        self.chroma_client = chromadb.Client(Settings(
            persist_directory=str(self.persist_directory),
            anonymized_telemetry=False
        ))

        # File index for tracking
        self.file_index_path = self.persist_directory / ".file_index.json"
        self.file_index = self._load_file_index()

        logger.info(f"Gemini Smart RAG initialized")
        logger.info(f"  Model: {self.model}")
        logger.info(f"  Embeddings: {self.embedding_model}")
        logger.info(f"  Storage: {self.persist_directory} (local)")

    def _load_file_index(self) -> Dict:
        """Load file index"""
        if self.file_index_path.exists():
            with open(self.file_index_path) as f:
                return json.load(f)
        return {}

    def _save_file_index(self):
        """Save file index"""
        with open(self.file_index_path, 'w') as f:
            json.dump(self.file_index, f, indent=2)

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()

    def create_collection(self, name: str) -> None:
        """Create a new collection"""
        try:
            self.chroma_client.create_collection(name=name)
            logger.info(f"Created collection: {name}")
        except Exception as e:
            if "already exists" in str(e):
                logger.info(f"Collection {name} already exists")
            else:
                raise

    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections"""
        collections = self.chroma_client.list_collections()
        result = []
        for col in collections:
            count = col.count()
            result.append({
                'name': col.name,
                'count': count
            })
        return result

    def _generate_gemini_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini"""
        try:
            embeddings = []
            # Batch process to avoid rate limits
            batch_size = 100

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]

                for text in batch:
                    result = self.client.models.embed_content(
                        model=self.embedding_model,
                        content=text
                    )
                    embeddings.append(result.embeddings[0].values)

                # Small delay to avoid rate limits
                if i + batch_size < len(texts):
                    time.sleep(0.1)

            return embeddings
        except Exception as e:
            logger.error(f"Gemini embedding failed: {e}")
            raise

    def _extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from various file formats"""
        suffix = file_path.suffix.lower()

        try:
            if suffix == '.pdf':
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    return '\n\n'.join(page.extract_text() for page in reader.pages)

            elif suffix == '.txt' or suffix == '.md':
                return file_path.read_text(encoding='utf-8', errors='ignore')

            elif suffix == '.docx':
                doc = docx.Document(file_path)
                return '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)

            elif suffix in ['.xlsx', '.xls']:
                handler = ExcelHandler()
                return handler.convert_to_markdown(file_path)

            else:
                logger.warning(f"Unsupported file type: {suffix}")
                return ""

        except Exception as e:
            logger.error(f"Failed to extract text from {file_path}: {e}")
            return ""

    def _chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Split text into chunks"""
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]

            if chunk.strip():
                chunks.append(chunk.strip())

            start += chunk_size - chunk_overlap

        return chunks

    def upload_file(
        self,
        file_path: Union[str, Path],
        collection_name: str,
        metadata: Optional[Dict] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        skip_duplicates: bool = True
    ) -> int:
        """
        Upload a file to the RAG system

        Args:
            file_path: Path to file
            collection_name: Collection to add to
            metadata: Optional metadata
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            skip_duplicates: Skip if file already indexed

        Returns:
            Number of chunks indexed
        """
        file_path = Path(file_path)

        # Check for duplicates
        if skip_duplicates:
            file_hash = self._calculate_file_hash(file_path)
            if file_hash in self.file_index:
                logger.info(f"File already indexed: {file_path.name}")
                return 0

        # Extract text
        text = self._extract_text_from_file(file_path)
        if not text:
            logger.warning(f"No text extracted from {file_path.name}")
            return 0

        # Chunk text
        chunks = self._chunk_text(text, chunk_size, chunk_overlap)
        if not chunks:
            return 0

        # Generate embeddings using Gemini
        embeddings = self._generate_gemini_embeddings(chunks)

        # Prepare metadata
        base_metadata = {
            'filename': file_path.name,
            'filepath': str(file_path),
            'file_type': file_path.suffix
        }
        if metadata:
            base_metadata.update(metadata)

        metadatas = [
            {**base_metadata, 'chunk_id': i}
            for i in range(len(chunks))
        ]

        # Generate IDs
        file_hash = self._calculate_file_hash(file_path)
        ids = [f"{file_hash}_{i}" for i in range(len(chunks))]

        # Add to collection
        collection = self.chroma_client.get_collection(collection_name)
        collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

        # Update file index
        self.file_index[file_hash] = {
            'filename': file_path.name,
            'path': str(file_path),
            'chunks': len(chunks),
            'collection': collection_name
        }
        self._save_file_index()

        logger.info(f"Indexed {file_path.name}: {len(chunks)} chunks")
        return len(chunks)

    def batch_upload(
        self,
        file_paths: List[Path],
        collection_name: str,
        batch_size: int = 20,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        Upload multiple files

        Args:
            file_paths: List of file paths
            collection_name: Collection name
            batch_size: Files per batch
            show_progress: Show progress bar

        Returns:
            Statistics dictionary
        """
        from tqdm import tqdm

        stats = {
            'total': len(file_paths),
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'total_chunks': 0
        }

        iterator = tqdm(file_paths, desc="Indexing") if show_progress else file_paths

        for file_path in iterator:
            try:
                chunks = self.upload_file(file_path, collection_name)
                if chunks > 0:
                    stats['successful'] += 1
                    stats['total_chunks'] += chunks
                else:
                    stats['skipped'] += 1
            except Exception as e:
                logger.error(f"Failed to index {file_path.name}: {e}")
                stats['failed'] += 1

        return stats

    def query(
        self,
        question: str,
        collection_name: str,
        n_results: int = 5,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Query the RAG system

        Args:
            question: User's question
            collection_name: Collection to search
            n_results: Number of sources to retrieve
            temperature: LLM temperature

        Returns:
            Answer with sources
        """
        # Generate query embedding
        query_embedding = self._generate_gemini_embeddings([question])[0]

        # Search in ChromaDB
        collection = self.chroma_client.get_collection(collection_name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Prepare context
        sources = []
        context_parts = []

        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            sources.append({
                'text': doc,
                'filename': metadata.get('filename', 'Unknown'),
                'chunk_id': metadata.get('chunk_id', 0),
                'distance': distance,
                'relevance': 1 - distance
            })
            context_parts.append(f"[Source {i+1}] {doc}")

        context = "\n\n".join(context_parts)

        # Generate answer using Gemini
        prompt = f"""Based on the following sources, please answer the question.

Sources:
{context}

Question: {question}

Please provide a comprehensive answer based on the sources above. Cite sources using [Source N] format."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=2048
                )
            )

            answer = response.text
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            answer = f"Error generating answer: {e}"

        return {
            'answer': answer,
            'sources': sources,
            'n_sources': len(sources),
            'model': self.model
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        collections = self.list_collections()
        total_docs = sum(c['count'] for c in collections)

        # Calculate database size
        db_size = sum(
            f.stat().st_size
            for f in self.persist_directory.rglob('*')
            if f.is_file()
        ) / (1024 * 1024)  # MB

        return {
            'collections': len(collections),
            'collections_detail': collections,
            'total_documents': total_docs,
            'database_size_mb': db_size,
            'indexed_files': len(self.file_index),
            'persist_directory': str(self.persist_directory)
        }


# Convenience function
def create_gemini_smart_rag(api_key: Optional[str] = None) -> GeminiSmartRAG:
    """Create a Gemini Smart RAG instance"""
    return GeminiSmartRAG(api_key=api_key)
