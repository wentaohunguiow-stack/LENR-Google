"""
Enterprise RAG Implementation - Premium Performance
Best-in-class components for production use
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import PyPDF2
import docx
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
import cohere
from anthropic import Anthropic

from src.utils.logger import setup_logger
from src.utils.excel_handler import ExcelHandler

logger = setup_logger(__name__)


class EnterpriseRAG:
    """
    Enterprise-grade RAG system with premium components

    Features:
    - Best embeddings: OpenAI text-embedding-3-large (3072 dimensions)
    - Managed vector DB: Pinecone (serverless, auto-scaling)
    - Smart reranking: Cohere rerank-english-v3.0
    - Best LLM: Claude 3.5 Sonnet (200K context)
    - Production-ready: High availability, monitoring
    - No size limits: Scales to millions of documents
    """

    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        pinecone_api_key: Optional[str] = None,
        cohere_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None,
        index_name: str = "enterprise-rag",
        embedding_model: str = "text-embedding-3-large",
        llm_model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        Initialize Enterprise RAG with premium services

        Args:
            openai_api_key: OpenAI API key (for best embeddings)
            pinecone_api_key: Pinecone API key (for managed vector DB)
            cohere_api_key: Cohere API key (for smart reranking)
            anthropic_api_key: Anthropic API key (for Claude 3.5)
            index_name: Pinecone index name
            embedding_model: OpenAI embedding model
            llm_model: Anthropic LLM model
        """
        # API keys
        self.openai_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.pinecone_key = pinecone_api_key or os.getenv("PINECONE_API_KEY")
        self.cohere_key = cohere_api_key or os.getenv("COHERE_API_KEY")
        self.anthropic_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")

        # Initialize OpenAI (embeddings)
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
            self.embedding_model = embedding_model
            self.embedding_dim = 3072  # text-embedding-3-large
            logger.info(f"OpenAI embeddings initialized: {embedding_model}")
        else:
            raise ValueError("OpenAI API key required for premium embeddings")

        # Initialize Pinecone (vector database)
        if self.pinecone_key:
            self.pc = Pinecone(api_key=self.pinecone_key)
            self.index_name = index_name
            self._init_pinecone_index()
            logger.info(f"Pinecone initialized: {index_name}")
        else:
            raise ValueError("Pinecone API key required for managed vector DB")

        # Initialize Cohere (reranking)
        if self.cohere_key:
            self.cohere_client = cohere.Client(self.cohere_key)
            logger.info("Cohere reranking initialized")
        else:
            logger.warning("Cohere API key not provided. Reranking disabled.")
            self.cohere_client = None

        # Initialize Anthropic (LLM)
        if self.anthropic_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_key)
            self.llm_model = llm_model
            logger.info(f"Anthropic Claude initialized: {llm_model}")
        else:
            logger.warning("Anthropic API key not provided. Using basic retrieval.")
            self.anthropic_client = None

    def _init_pinecone_index(self):
        """Initialize Pinecone serverless index"""
        # Check if index exists
        if self.index_name not in self.pc.list_indexes().names():
            logger.info(f"Creating Pinecone index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=self.embedding_dim,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )

        self.index = self.pc.Index(self.index_name)

    def _extract_text_from_file(self, file_path: Path) -> str:
        """Extract text from various file types"""
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
                return ExcelHandler.excel_to_structured_text(str(file_path))

            else:
                logger.warning(f"Unsupported file type: {suffix}")
                return ""

        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return ""

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into chunks with overlap"""
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]

            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)

                if break_point > chunk_size * 0.5:
                    chunk = text[start:start + break_point + 1]
                    end = start + break_point + 1

            chunks.append(chunk.strip())
            start = end - overlap

        return [c for c in chunks if c]

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI text-embedding-3-large"""
        logger.info(f"Generating premium embeddings for {len(texts)} chunks...")

        response = self.openai_client.embeddings.create(
            input=texts,
            model=self.embedding_model
        )

        return [item.embedding for item in response.data]

    def upload_file(
        self,
        file_path: Union[str, Path],
        metadata: Optional[Dict[str, str]] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> int:
        """
        Upload file to enterprise RAG system

        Args:
            file_path: Path to file
            metadata: Optional metadata (e.g., category, date)
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            Number of chunks indexed
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Extract text
        logger.info(f"Processing {file_path.name}")
        text = self._extract_text_from_file(file_path)

        if not text:
            logger.warning(f"No text extracted from {file_path.name}")
            return 0

        # Chunk text
        chunks = self._chunk_text(text, chunk_size, chunk_overlap)
        logger.info(f"Split into {len(chunks)} chunks")

        # Generate embeddings
        embeddings = self._generate_embeddings(chunks)

        # Prepare metadata
        base_metadata = metadata or {}
        base_metadata.update({
            'filename': file_path.name,
            'file_type': file_path.suffix,
        })

        # Upsert to Pinecone
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_metadata = {**base_metadata, 'chunk_id': i, 'text': chunk}
            vectors.append({
                'id': f"{file_path.stem}_{i}",
                'values': embedding,
                'metadata': chunk_metadata
            })

        # Batch upsert (100 at a time for optimal performance)
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)

        logger.info(f"✅ Indexed {len(chunks)} chunks from {file_path.name}")
        return len(chunks)

    def query(
        self,
        question: str,
        top_k: int = 20,
        rerank_top_k: int = 5,
        use_reranking: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Query enterprise RAG with advanced retrieval

        Args:
            question: User question
            top_k: Initial retrieval count
            rerank_top_k: Final count after reranking
            use_reranking: Use Cohere reranking
            temperature: Claude temperature
            max_tokens: Max response tokens

        Returns:
            Dict with answer, sources, and metadata
        """
        # Generate query embedding
        logger.info(f"Query: {question}")
        query_embedding = self._generate_embeddings([question])[0]

        # Search Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Extract documents
        documents = []
        for match in results['matches']:
            documents.append({
                'text': match['metadata']['text'],
                'filename': match['metadata']['filename'],
                'score': float(match['score']),
                'chunk_id': match['metadata'].get('chunk_id', 0)
            })

        # Rerank with Cohere if enabled
        if use_reranking and self.cohere_client and len(documents) > 0:
            logger.info("Reranking with Cohere...")
            doc_texts = [doc['text'] for doc in documents]

            rerank_results = self.cohere_client.rerank(
                model="rerank-english-v3.0",
                query=question,
                documents=doc_texts,
                top_n=min(rerank_top_k, len(doc_texts))
            )

            # Reorder documents by relevance
            reranked_docs = []
            for result in rerank_results.results:
                doc = documents[result.index]
                doc['rerank_score'] = float(result.relevance_score)
                reranked_docs.append(doc)

            documents = reranked_docs

        # Build context from top documents
        context = "\n\n---\n\n".join([
            f"[Source: {doc['filename']}]\n{doc['text']}"
            for doc in documents[:rerank_top_k]
        ])

        # Generate answer with Claude 3.5 Sonnet
        if self.anthropic_client:
            prompt = f"""Based on the following context, answer the question accurately and concisely.
If the answer is not in the context, say so.

Context:
{context}

Question: {question}

Answer:"""

            message = self.anthropic_client.messages.create(
                model=self.llm_model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            answer = message.content[0].text
        else:
            answer = f"Retrieved {len(documents)} relevant passages:\n\n{context}"

        return {
            'answer': answer,
            'sources': documents[:rerank_top_k],
            'n_sources': len(documents),
            'context': context,
            'model': self.llm_model if self.anthropic_client else "retrieval-only"
        }

    def batch_upload(
        self,
        file_paths: List[Union[str, Path]],
        show_progress: bool = True
    ) -> Dict[str, int]:
        """
        Batch upload multiple files

        Args:
            file_paths: List of file paths
            show_progress: Show progress bar

        Returns:
            Dict with upload statistics
        """
        total_chunks = 0
        successful = 0
        failed = 0

        iterator = file_paths
        if show_progress:
            try:
                from tqdm import tqdm
                iterator = tqdm(file_paths, desc="Uploading files")
            except ImportError:
                pass

        for file_path in iterator:
            try:
                chunks = self.upload_file(file_path)
                total_chunks += chunks
                successful += 1
            except Exception as e:
                logger.error(f"Failed to upload {file_path}: {e}")
                failed += 1

        return {
            'total_files': len(file_paths),
            'successful': successful,
            'failed': failed,
            'total_chunks': total_chunks
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        stats = self.index.describe_index_stats()

        return {
            'total_vectors': stats.total_vector_count,
            'dimension': stats.dimension,
            'index_fullness': stats.index_fullness,
            'namespaces': list(stats.namespaces.keys()) if stats.namespaces else []
        }

    def delete_by_filename(self, filename: str):
        """Delete all vectors for a specific file"""
        # Query to get IDs
        dummy_vector = [0.0] * self.embedding_dim
        results = self.index.query(
            vector=dummy_vector,
            filter={"filename": {"$eq": filename}},
            top_k=10000
        )

        ids_to_delete = [match['id'] for match in results['matches']]

        if ids_to_delete:
            self.index.delete(ids=ids_to_delete)
            logger.info(f"Deleted {len(ids_to_delete)} vectors for {filename}")

    def delete_all(self):
        """Delete all vectors from index"""
        logger.warning(f"Deleting all vectors from {self.index_name}")
        self.index.delete(delete_all=True)
