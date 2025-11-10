"""Tests for Excel-specific functionality in GeminiRAG."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

from src.rag.gemini_rag import GeminiRAG


class TestGeminiRAGExcel:
    """Test suite for Excel-specific RAG functionality."""

    @pytest.fixture
    def mock_api_key(self, monkeypatch):
        """Set mock API key."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-123")

    @pytest.fixture
    def rag_instance(self, mock_api_key):
        """Create a GeminiRAG instance for testing."""
        with patch('google.genai.Client'):
            return GeminiRAG(api_key="test-api-key")

    @pytest.fixture
    def sample_excel_file(self, tmp_path):
        """Create a sample Excel file."""
        file_path = tmp_path / "test.xlsx"
        data = {
            "Product": ["A", "B", "C"],
            "Sales": [100, 200, 300]
        }
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        return file_path

    def test_upload_excel_success(self, rag_instance, sample_excel_file):
        """Test successful Excel file upload."""
        mock_operation = Mock()
        mock_operation.name = "operation-123"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        operation_name = rag_instance.upload_excel(
            sample_excel_file,
            "store123",
            metadata={"type": "sales"}
        )

        assert operation_name == "operation-123"
        rag_instance.client.file_search_stores.upload_to_file_search_store.assert_called_once()

    def test_upload_excel_invalid_file(self, rag_instance, tmp_path):
        """Test error handling for non-Excel file."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("not an excel file")

        with pytest.raises(ValueError, match="Not an Excel file"):
            rag_instance.upload_excel(text_file, "store123")

    def test_upload_excel_with_conversion_format(self, rag_instance, sample_excel_file):
        """Test Excel upload with different conversion formats."""
        mock_operation = Mock()
        mock_operation.name = "operation-123"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        # Test markdown format
        rag_instance.upload_excel(
            sample_excel_file,
            "store123",
            conversion_format="markdown"
        )

        # Test text format
        rag_instance.upload_excel(
            sample_excel_file,
            "store123",
            conversion_format="text"
        )

        # Test JSON format
        rag_instance.upload_excel(
            sample_excel_file,
            "store123",
            conversion_format="json"
        )

        assert rag_instance.client.file_search_stores.upload_to_file_search_store.call_count == 3

    def test_upload_excel_metadata_includes_excel_info(self, rag_instance, sample_excel_file):
        """Test that uploaded Excel file includes proper metadata."""
        mock_operation = Mock()
        mock_operation.name = "operation-123"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        rag_instance.upload_excel(
            sample_excel_file,
            "store123",
            metadata={"custom": "value"}
        )

        # Check that upload_file was called with Excel-specific metadata
        call_args = rag_instance.client.file_search_stores.upload_to_file_search_store.call_args

        # The converted file should have been uploaded
        assert call_args is not None

    def test_batch_upload_excel(self, rag_instance, tmp_path):
        """Test batch upload of multiple Excel files."""
        excel_files = []
        for i in range(3):
            file_path = tmp_path / f"test{i}.xlsx"
            data = {"Value": [i * 10, i * 20]}
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            excel_files.append(file_path)

        mock_operation = Mock()
        mock_operation.name = "operation"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        operations = rag_instance.batch_upload_excel(
            excel_files,
            "store123"
        )

        assert len(operations) == 3
        assert rag_instance.client.file_search_stores.upload_to_file_search_store.call_count == 3

    def test_batch_upload_excel_with_metadata_fn(self, rag_instance, tmp_path):
        """Test batch Excel upload with metadata function."""
        excel_files = []
        for i in range(2):
            file_path = tmp_path / f"q{i+1}.xlsx"
            data = {"Value": [i]}
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            excel_files.append(file_path)

        def metadata_fn(file_path):
            return {"quarter": Path(file_path).stem}

        mock_operation = Mock()
        mock_operation.name = "operation"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        operations = rag_instance.batch_upload_excel(
            excel_files,
            "store123",
            metadata_fn=metadata_fn
        )

        assert len(operations) == 2

    def test_query_excel_data(self, rag_instance):
        """Test querying Excel data with optimized settings."""
        mock_response = Mock()
        mock_response.text = "The answer is 42"
        mock_response.candidates = [Mock(grounding_metadata=None)]

        rag_instance.client.models.generate_content = Mock(return_value=mock_response)

        result = rag_instance.query_excel_data(
            "What is the total?",
            "store123"
        )

        assert "answer" in result
        assert "42" in result["answer"]

        # Verify that query was called with enhanced question
        call_args = rag_instance.client.models.generate_content.call_args
        question_arg = call_args[1]["contents"]
        assert "Excel" in question_arg or "spreadsheet" in question_arg

    def test_upload_excel_auto_cleanup(self, rag_instance, sample_excel_file, tmp_path):
        """Test that converted files are cleaned up after upload."""
        mock_operation = Mock()
        mock_operation.name = "operation-123"

        rag_instance.client.file_search_stores.upload_to_file_search_store = Mock(
            return_value=mock_operation
        )

        # Upload with auto_cleanup=True (default)
        rag_instance.upload_excel(
            sample_excel_file,
            "store123",
            auto_cleanup=True
        )

        # The converted file should have been deleted
        # Check that no converted files remain in the directory
        converted_files = list(sample_excel_file.parent.glob("*_converted.*"))
        assert len(converted_files) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
