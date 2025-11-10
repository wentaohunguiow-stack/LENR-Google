"""Tests for Gemini RAG implementation."""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.rag.gemini_rag import GeminiRAG


class TestGeminiRAG:
    """Test suite for GeminiRAG class."""

    @pytest.fixture
    def mock_api_key(self, monkeypatch):
        """Set mock API key."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-123")

    @pytest.fixture
    def rag_instance(self, mock_api_key):
        """Create a GeminiRAG instance for testing."""
        with patch('google.genai.Client'):
            return GeminiRAG(api_key="test-api-key")

    def test_initialization_with_api_key(self):
        """Test RAG initialization with explicit API key."""
        with patch('google.genai.Client') as mock_client:
            rag = GeminiRAG(api_key="test-key")
            assert rag.api_key == "test-key"
            assert rag.default_model == "gemini-2.5-flash"
            mock_client.assert_called_once_with(api_key="test-key")

    def test_initialization_without_api_key(self, monkeypatch):
        """Test that initialization fails without API key."""
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

        with pytest.raises(ValueError, match="Google API key required"):
            GeminiRAG()

    def test_initialization_from_env(self, mock_api_key):
        """Test RAG initialization from environment variable."""
        with patch('google.genai.Client'):
            rag = GeminiRAG()
            assert rag.api_key == "test-api-key-123"

    def test_create_store(self, rag_instance):
        """Test file search store creation."""
        mock_store = Mock()
        mock_store.name = "test-store-123"

        rag_instance.client.file_search_stores.create = Mock(return_value=mock_store)

        store_name = rag_instance.create_store("test-store")

        assert store_name == "test-store-123"
        rag_instance.client.file_search_stores.create.assert_called_once_with(
            config={'display_name': 'test-store'}
        )

    def test_list_stores(self, rag_instance):
        """Test listing file search stores."""
        mock_stores = [
            Mock(
                name="store1",
                display_name="Store 1",
                create_time="2024-01-01",
                update_time="2024-01-02"
            ),
            Mock(
                name="store2",
                display_name="Store 2",
                create_time="2024-01-03",
                update_time="2024-01-04"
            )
        ]

        rag_instance.client.file_search_stores.list = Mock(return_value=mock_stores)

        stores = rag_instance.list_stores()

        assert len(stores) == 2
        assert stores[0]['name'] == "store1"
        assert stores[0]['display_name'] == "Store 1"
        assert stores[1]['name'] == "store2"

    def test_get_store(self, rag_instance):
        """Test getting store information."""
        mock_store = Mock(
            name="store123",
            display_name="Test Store",
            create_time="2024-01-01",
            update_time="2024-01-02"
        )

        rag_instance.client.file_search_stores.get = Mock(return_value=mock_store)

        store_info = rag_instance.get_store("store123")

        assert store_info['name'] == "store123"
        assert store_info['display_name'] == "Test Store"

    def test_upload_file_not_found(self, rag_instance):
        """Test upload fails with non-existent file."""
        with pytest.raises(FileNotFoundError):
            rag_instance.upload_file("nonexistent.txt", "store123")

    def test_upload_file_too_large(self, rag_instance, tmp_path):
        """Test upload fails with file > 100 MB."""
        large_file = tmp_path / "large.txt"
        # Create a file larger than 100 MB (create sparse file for speed)
        with open(large_file, 'wb') as f:
            f.seek(101 * 1024 * 1024)  # 101 MB
            f.write(b'\0')

        with pytest.raises(ValueError, match="File too large"):
            rag_instance.upload_file(large_file, "store123")

    def test_upload_file_success(self, rag_instance, tmp_path):
        """Test successful file upload."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        mock_operation = Mock()
        mock_operation.name = "operation-123"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        operation_name = rag_instance.upload_file(
            test_file,
            "store123",
            metadata={"key": "value"}
        )

        assert operation_name == "operation-123"
        rag_instance.client.file_search_stores.upload_to_file_search_store.assert_called_once()

    def test_query(self, rag_instance):
        """Test querying the RAG system."""
        mock_response = Mock()
        mock_response.text = "This is the answer"
        mock_response.candidates = [Mock(grounding_metadata=None)]

        rag_instance.client.models.generate_content = Mock(return_value=mock_response)

        result = rag_instance.query("Test question?", "store123")

        assert result['answer'] == "This is the answer"
        assert result['model'] == "gemini-2.5-flash"
        assert isinstance(result['citations'], list)

    def test_query_with_custom_model(self, rag_instance):
        """Test query with custom model."""
        mock_response = Mock()
        mock_response.text = "Answer"
        mock_response.candidates = [Mock(grounding_metadata=None)]

        rag_instance.client.models.generate_content = Mock(return_value=mock_response)

        result = rag_instance.query(
            "Question?",
            "store123",
            model="gemini-2.5-pro"
        )

        assert result['model'] == "gemini-2.5-pro"

    def test_delete_store(self, rag_instance):
        """Test deleting a store."""
        rag_instance.client.file_search_stores.delete = Mock()

        result = rag_instance.delete_store("store123")

        assert result is True
        rag_instance.client.file_search_stores.delete.assert_called_once_with(
            name="store123"
        )

    def test_batch_upload(self, rag_instance, tmp_path):
        """Test batch uploading multiple files."""
        files = []
        for i in range(3):
            f = tmp_path / f"file{i}.txt"
            f.write_text(f"Content {i}")
            files.append(f)

        mock_operation = Mock()
        mock_operation.name = "operation"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        operations = rag_instance.batch_upload(files, "store123")

        assert len(operations) == 3
        assert rag_instance.client.file_search_stores.upload_to_file_search_store.call_count == 3

    def test_batch_upload_with_metadata_fn(self, rag_instance, tmp_path):
        """Test batch upload with metadata function."""
        files = []
        for i in range(2):
            f = tmp_path / f"doc{i}.txt"
            f.write_text(f"Content {i}")
            files.append(f)

        def metadata_fn(file_path):
            return {"index": str(Path(file_path).stem[-1])}

        mock_operation = Mock()
        mock_operation.name = "operation"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        operations = rag_instance.batch_upload(
            files,
            "store123",
            metadata_fn=metadata_fn
        )

        assert len(operations) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
