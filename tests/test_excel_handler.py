"""Tests for Excel handler utility."""

import pytest
from pathlib import Path
import pandas as pd

from src.utils.excel_handler import ExcelHandler


class TestExcelHandler:
    """Test suite for ExcelHandler class."""

    @pytest.fixture
    def sample_excel_file(self, tmp_path):
        """Create a sample Excel file for testing."""
        file_path = tmp_path / "test_data.xlsx"

        # Create sample data
        data = {
            "Name": ["Alice", "Bob", "Carol"],
            "Age": [25, 30, 28],
            "City": ["New York", "London", "Tokyo"]
        }
        df = pd.DataFrame(data)

        # Write to Excel with multiple sheets
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            df.to_excel(writer, sheet_name="Sheet2", index=False)

        return file_path

    def test_excel_to_markdown(self, sample_excel_file):
        """Test converting Excel to Markdown."""
        markdown = ExcelHandler.excel_to_markdown(sample_excel_file)

        assert "# Excel File:" in markdown
        assert "## Sheet: Sheet1" in markdown
        assert "Alice" in markdown
        assert "Bob" in markdown
        assert "**Rows:**" in markdown

    def test_excel_to_structured_text(self, sample_excel_file):
        """Test converting Excel to structured text."""
        text = ExcelHandler.excel_to_structured_text(sample_excel_file)

        assert "EXCEL FILE:" in text
        assert "SHEET: Sheet1" in text
        assert "Total Records:" in text
        assert "Name: Alice" in text
        assert "Age: 25" in text

    def test_excel_to_json(self, sample_excel_file):
        """Test converting Excel to JSON."""
        import json

        json_str = ExcelHandler.excel_to_json(sample_excel_file)
        data = json.loads(json_str)

        assert "filename" in data
        assert "sheets" in data
        assert "Sheet1" in data["sheets"]
        assert len(data["sheets"]["Sheet1"]) == 3
        assert data["sheets"]["Sheet1"][0]["Name"] == "Alice"

    def test_excel_to_csv_per_sheet(self, sample_excel_file, tmp_path):
        """Test converting Excel sheets to CSV files."""
        csv_files = ExcelHandler.excel_to_csv_per_sheet(
            sample_excel_file,
            output_dir=tmp_path
        )

        assert len(csv_files) == 2
        assert all(f.exists() for f in csv_files)
        assert all(f.suffix == '.csv' for f in csv_files)

        # Verify CSV content
        df = pd.read_csv(csv_files[0])
        assert len(df) == 3
        assert "Name" in df.columns

    def test_get_excel_summary(self, sample_excel_file):
        """Test getting Excel file summary."""
        summary = ExcelHandler.get_excel_summary(sample_excel_file)

        assert summary["sheet_count"] == 2
        assert "Sheet1" in summary["sheet_names"]
        assert "Sheet2" in summary["sheet_names"]
        assert len(summary["sheets"]) == 2
        assert summary["sheets"][0]["rows"] == 3
        assert summary["sheets"][0]["columns"] == 3

    def test_prepare_excel_for_rag_markdown(self, sample_excel_file, tmp_path):
        """Test preparing Excel for RAG in markdown format."""
        output_path = ExcelHandler.prepare_excel_for_rag(
            sample_excel_file,
            output_dir=tmp_path,
            format="markdown"
        )

        assert output_path.exists()
        assert output_path.suffix == ".md"

        content = output_path.read_text()
        assert "# Excel File:" in content
        assert "Alice" in content

    def test_prepare_excel_for_rag_text(self, sample_excel_file, tmp_path):
        """Test preparing Excel for RAG in text format."""
        output_path = ExcelHandler.prepare_excel_for_rag(
            sample_excel_file,
            output_dir=tmp_path,
            format="text"
        )

        assert output_path.exists()
        assert output_path.suffix == ".txt"

        content = output_path.read_text()
        assert "EXCEL FILE:" in content

    def test_prepare_excel_for_rag_json(self, sample_excel_file, tmp_path):
        """Test preparing Excel for RAG in JSON format."""
        output_path = ExcelHandler.prepare_excel_for_rag(
            sample_excel_file,
            output_dir=tmp_path,
            format="json"
        )

        assert output_path.exists()
        assert output_path.suffix == ".json"

        import json
        with open(output_path) as f:
            data = json.load(f)

        assert "sheets" in data

    def test_prepare_excel_for_rag_invalid_format(self, sample_excel_file, tmp_path):
        """Test error handling for invalid format."""
        with pytest.raises(ValueError, match="Unsupported format"):
            ExcelHandler.prepare_excel_for_rag(
                sample_excel_file,
                output_dir=tmp_path,
                format="invalid"
            )

    def test_excel_to_markdown_specific_sheets(self, sample_excel_file):
        """Test converting only specific sheets to markdown."""
        markdown = ExcelHandler.excel_to_markdown(
            sample_excel_file,
            include_sheet_names=["Sheet1"]
        )

        assert "## Sheet: Sheet1" in markdown
        assert "## Sheet: Sheet2" not in markdown

    def test_excel_to_structured_text_with_row_limit(self, sample_excel_file):
        """Test structured text conversion with row limit."""
        text = ExcelHandler.excel_to_structured_text(
            sample_excel_file,
            max_rows_per_sheet=2
        )

        # Should only include first 2 records
        assert "Record 1:" in text
        assert "Record 2:" in text
        # Record 3 might be present as total records count, but not detailed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
