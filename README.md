# LENR Google RAG System

A Retrieval-Augmented Generation (RAG) system built with Google's Gemini API file search capabilities.

## Features

- **Interactive Web UI**: OpenEvidence-style interface with clickable citations
- **File Search Store Management**: Create and manage document stores with semantic search
- **Document Upload**: Upload and index documents (PDF, TXT, DOCX, Excel, etc.)
- **Excel Integration**: Automatic conversion and indexing of Excel spreadsheets (.xlsx, .xls)
- **Intelligent Retrieval**: Semantic search using Google's embeddings
- **RAG Queries**: Ask questions and get contextual answers from your documents
- **Interactive Citations**: Numbered references with source previews and document links
- **Metadata Support**: Add custom metadata for filtering and organization

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd LENR-Google

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

## Quick Start

### Basic Usage

```python
from src.rag.gemini_rag import GeminiRAG

# Initialize the RAG system
rag = GeminiRAG(api_key="your_api_key")

# Create a file search store
store_name = rag.create_store("my-documents")

# Upload documents
rag.upload_file(
    file_path="path/to/document.pdf",
    store_name=store_name,
    metadata={"category": "research", "year": "2024"}
)

# Query the documents
response = rag.query(
    question="What are the key findings?",
    store_name=store_name
)

print(response["answer"])
print("Sources:", response["citations"])
```

### Excel Integration

```python
# Upload Excel files (automatically converted to searchable format)
rag.upload_excel(
    file_path="sales_data.xlsx",
    store_name=store_name,
    metadata={"type": "sales", "quarter": "Q1"},
    conversion_format="markdown"  # or "text", "json"
)

# Query Excel data with optimized settings
response = rag.query_excel_data(
    question="What were the total sales in Q1?",
    store_name=store_name
)

print(response["answer"])
```

## Web Interface with Interactive Citations

Launch the interactive web UI for an OpenEvidence-style experience:

```bash
streamlit run web_ui/app.py
```

Features:
- 🔍 **Interactive Search**: Ask questions with real-time results
- 📚 **Clickable Citations**: Numbered references like academic papers
- 📄 **Source Preview**: View excerpts from cited documents
- 📊 **Document Management**: Upload and organize files
- 💾 **Query History**: Track previous searches

See `web_ui/README.md` for detailed instructions.

## Usage Examples

See the `examples/` directory for detailed usage examples:

- `basic_usage.py`: Simple document upload and query
- `advanced_usage.py`: Metadata filtering and chunking configuration
- `batch_upload.py`: Upload multiple documents at once
- `excel_usage.py`: Excel file integration and querying
- `citation_demo.py`: Interactive citation features demonstration

## Architecture

```
User Query
    ↓
Gemini File Search Store
    ↓
Semantic Search (Embeddings)
    ↓
Relevant Document Chunks
    ↓
Gemini 2.5 Model
    ↓
Contextual Answer + Citations
```

## Supported File Types

- PDF (`.pdf`)
- Text (`.txt`)
- Word Documents (`.docx`)
- Markdown (`.md`)
- HTML (`.html`)
- **Excel Spreadsheets (`.xlsx`, `.xls`)** - Automatically converted to searchable format

Maximum file size: 100 MB per document

### Excel File Support

Excel files are automatically converted to an optimal format for RAG:
- **Markdown format**: Preserves table structure (recommended for most use cases)
- **Text format**: Human-readable with clear descriptions
- **JSON format**: Structured data representation

The system extracts all sheets, preserves column headers, and maintains data relationships for accurate querying.

## API Documentation

### GeminiRAG Class

#### Methods

- `create_store(display_name: str) -> str`: Create a new file search store
- `list_stores() -> List[Dict]`: List all available stores
- `upload_file(file_path: str, store_name: str, metadata: Dict = None) -> str`: Upload a document
- `upload_excel(file_path: str, store_name: str, metadata: Dict = None, conversion_format: str = "markdown") -> str`: Upload Excel file
- `query(question: str, store_name: str, model: str = "gemini-2.5-flash") -> Dict`: Query documents
- `query_excel_data(question: str, store_name: str) -> Dict`: Query Excel data with optimized settings
- `delete_store(store_name: str) -> bool`: Delete a store

## Pricing

- **Storage**: Free (1 GB free tier)
- **Indexing**: $0.15 per 1M tokens
- **Query embeddings**: Free
- **Model inference**: Standard Gemini pricing

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## License

MIT License
