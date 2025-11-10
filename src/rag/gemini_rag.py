"""Google Gemini RAG implementation with file search."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import google.genai as genai
from google.genai import types

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class GeminiRAG:
    """
    RAG system using Google Gemini API with file search capabilities.

    This class provides a complete RAG implementation using Gemini's built-in
    file search functionality for document indexing and retrieval.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = "gemini-2.5-flash"
    ):
        """
        Initialize the Gemini RAG system.

        Args:
            api_key: Google API key. If not provided, reads from GOOGLE_API_KEY env var
            default_model: Default Gemini model to use (gemini-2.5-flash or gemini-2.5-pro)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Google API key required. Set GOOGLE_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.default_model = default_model
        self.client = genai.Client(api_key=self.api_key)
        logger.info("Gemini RAG system initialized")

    def create_store(self, display_name: str) -> str:
        """
        Create a new file search store for document embeddings.

        Args:
            display_name: Human-readable name for the store

        Returns:
            The resource name of the created store

        Example:
            >>> rag = GeminiRAG()
            >>> store_name = rag.create_store("research-papers")
        """
        try:
            file_search_store = self.client.file_search_stores.create(
                config={'display_name': display_name}
            )
            logger.info(f"Created file search store: {file_search_store.name}")
            return file_search_store.name
        except Exception as e:
            logger.error(f"Failed to create store: {e}")
            raise

    def list_stores(self) -> List[Dict[str, Any]]:
        """
        List all available file search stores.

        Returns:
            List of store information dictionaries

        Example:
            >>> rag = GeminiRAG()
            >>> stores = rag.list_stores()
            >>> for store in stores:
            ...     print(f"{store['name']}: {store['display_name']}")
        """
        try:
            stores = []
            for store in self.client.file_search_stores.list():
                stores.append({
                    'name': store.name,
                    'display_name': store.display_name,
                    'create_time': store.create_time,
                    'update_time': store.update_time,
                })
            logger.info(f"Found {len(stores)} file search stores")
            return stores
        except Exception as e:
            logger.error(f"Failed to list stores: {e}")
            raise

    def get_store(self, store_name: str) -> Dict[str, Any]:
        """
        Get information about a specific file search store.

        Args:
            store_name: Resource name of the store

        Returns:
            Store information dictionary
        """
        try:
            store = self.client.file_search_stores.get(name=store_name)
            return {
                'name': store.name,
                'display_name': store.display_name,
                'create_time': store.create_time,
                'update_time': store.update_time,
            }
        except Exception as e:
            logger.error(f"Failed to get store {store_name}: {e}")
            raise

    def upload_file(
        self,
        file_path: Union[str, Path],
        store_name: str,
        metadata: Optional[Dict[str, str]] = None,
        chunking_config: Optional[Dict[str, int]] = None
    ) -> str:
        """
        Upload and index a file to a file search store.

        Args:
            file_path: Path to the file to upload
            store_name: Resource name of the target store
            metadata: Optional metadata key-value pairs for filtering
            chunking_config: Optional chunking configuration with keys:
                - max_tokens_per_chunk: Max tokens per chunk (default: 2048)
                - max_overlap_tokens: Overlap between chunks (default: 512)

        Returns:
            Operation name for tracking the upload

        Example:
            >>> rag = GeminiRAG()
            >>> store_name = rag.create_store("docs")
            >>> rag.upload_file(
            ...     "paper.pdf",
            ...     store_name,
            ...     metadata={"category": "research", "year": "2024"}
            ... )
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check file size (100 MB limit)
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > 100:
            raise ValueError(f"File too large: {file_size_mb:.2f} MB (max 100 MB)")

        try:
            # Build upload config
            config = {}
            if metadata:
                config['metadata'] = metadata
            if chunking_config:
                config['chunking_config'] = chunking_config

            # Upload and import to file search store
            logger.info(f"Uploading {file_path.name} to {store_name}")
            operation = self.client.file_search_stores.upload_to_file_search_store(
                file=str(file_path),
                file_search_store_name=store_name,
                config=config if config else None
            )

            logger.info(f"File uploaded successfully: {operation.name}")
            return operation.name
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {e}")
            raise

    def query(
        self,
        question: str,
        store_name: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Query the RAG system with a question.

        Args:
            question: The question to ask
            store_name: Resource name of the file search store to query
            model: Model to use (defaults to self.default_model)
            temperature: Sampling temperature (0.0 to 1.0)
            max_output_tokens: Maximum tokens in response

        Returns:
            Dictionary containing:
                - answer: Generated answer text
                - citations: List of source citations with metadata
                - grounding_metadata: Detailed grounding information

        Example:
            >>> rag = GeminiRAG()
            >>> response = rag.query(
            ...     "What are the main findings?",
            ...     store_name="research-papers"
            ... )
            >>> print(response["answer"])
            >>> print("Sources:", response["citations"])
        """
        model_name = model or self.default_model

        try:
            logger.info(f"Querying {store_name} with model {model_name}")

            # Generate content with file search
            response = self.client.models.generate_content(
                model=model_name,
                contents=question,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(
                        file_search=types.FileSearchToolConfig(
                            file_search_store_names=[store_name]
                        )
                    )],
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                )
            )

            # Extract answer text
            answer = response.text if hasattr(response, 'text') else str(response)

            # Extract citations and grounding metadata
            citations = []
            grounding_metadata = None

            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]

                # Get grounding metadata
                if hasattr(candidate, 'grounding_metadata'):
                    grounding_metadata = candidate.grounding_metadata

                    # Extract citation information
                    if hasattr(grounding_metadata, 'grounding_chunks'):
                        for chunk in grounding_metadata.grounding_chunks:
                            citation = {
                                'text': getattr(chunk, 'text', ''),
                            }
                            if hasattr(chunk, 'retrieved_context'):
                                ctx = chunk.retrieved_context
                                citation.update({
                                    'uri': getattr(ctx, 'uri', ''),
                                    'title': getattr(ctx, 'title', ''),
                                })
                            citations.append(citation)

            result = {
                'answer': answer,
                'citations': citations,
                'grounding_metadata': grounding_metadata,
                'model': model_name,
            }

            logger.info(f"Query completed with {len(citations)} citations")
            return result

        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    def delete_store(self, store_name: str) -> bool:
        """
        Delete a file search store and all its contents.

        Args:
            store_name: Resource name of the store to delete

        Returns:
            True if deletion was successful

        Example:
            >>> rag = GeminiRAG()
            >>> rag.delete_store("old-store-name")
        """
        try:
            self.client.file_search_stores.delete(name=store_name)
            logger.info(f"Deleted store: {store_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete store {store_name}: {e}")
            raise

    def batch_upload(
        self,
        file_paths: List[Union[str, Path]],
        store_name: str,
        metadata_fn: Optional[callable] = None
    ) -> List[str]:
        """
        Upload multiple files to a store.

        Args:
            file_paths: List of file paths to upload
            store_name: Target store resource name
            metadata_fn: Optional function to generate metadata for each file.
                         Takes file path as input, returns metadata dict.

        Returns:
            List of operation names for each upload

        Example:
            >>> rag = GeminiRAG()
            >>> store_name = rag.create_store("batch-docs")
            >>> files = ["doc1.pdf", "doc2.txt", "doc3.pdf"]
            >>> operations = rag.batch_upload(files, store_name)
        """
        operations = []
        for file_path in file_paths:
            try:
                metadata = metadata_fn(file_path) if metadata_fn else None
                operation = self.upload_file(file_path, store_name, metadata)
                operations.append(operation)
            except Exception as e:
                logger.error(f"Failed to upload {file_path}: {e}")
                # Continue with other files

        logger.info(f"Batch uploaded {len(operations)}/{len(file_paths)} files")
        return operations
