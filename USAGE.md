# Usage Guide

This guide provides detailed instructions for using the LENR Google RAG system.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [API Reference](#api-reference)
6. [Examples](#examples)

## Installation

### Prerequisites

- Python 3.9 or higher
- Google API key (get one at https://aistudio.google.com/app/apikey)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd LENR-Google

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
DEFAULT_MODEL=gemini-2.5-flash
DEFAULT_STORE_NAME=my-documents
```

### Configuration Options

- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `DEFAULT_MODEL`: Default model to use (gemini-2.5-flash or gemini-2.5-pro)
- `DEFAULT_STORE_NAME`: Default name for file search stores
- `MAX_FILE_SIZE_MB`: Maximum file size in MB (default: 100)

## Basic Usage

### 1. Initialize the RAG System

```python
from src.rag.gemini_rag import GeminiRAG

# Initialize with API key from environment
rag = GeminiRAG()

# Or provide API key explicitly
rag = GeminiRAG(api_key="your_api_key")
```

### 2. Create a File Search Store

A file search store is a container for your documents and their embeddings.

```python
store_name = rag.create_store("my-research-papers")
print(f"Created store: {store_name}")
```

### 3. Upload Documents

```python
# Upload a single file
rag.upload_file(
    file_path="document.pdf",
    store_name=store_name
)

# Upload with metadata
rag.upload_file(
    file_path="research_paper.pdf",
    store_name=store_name,
    metadata={
        "author": "John Doe",
        "year": "2024",
        "category": "LENR",
        "peer_reviewed": "yes"
    }
)
```

### 4. Query Your Documents

```python
response = rag.query(
    question="What are the main findings about LENR?",
    store_name=store_name
)

print("Answer:", response["answer"])
print("Number of sources:", len(response["citations"]))
```

## Advanced Features

### Batch Upload

Upload multiple documents at once:

```python
files = [
    "paper1.pdf",
    "paper2.pdf",
    "paper3.txt"
]

# Simple batch upload
operations = rag.batch_upload(files, store_name)

# With custom metadata function
def generate_metadata(file_path):
    from pathlib import Path
    return {
        "filename": Path(file_path).name,
        "category": "research"
    }

operations = rag.batch_upload(
    files,
    store_name,
    metadata_fn=generate_metadata
)
```

### Custom Chunking Configuration

Control how documents are split into chunks:

```python
rag.upload_file(
    file_path="long_document.pdf",
    store_name=store_name,
    chunking_config={
        "max_tokens_per_chunk": 512,   # Smaller chunks
        "max_overlap_tokens": 128       # More overlap
    }
)
```

Benefits of custom chunking:
- **Smaller chunks**: More precise citations, better for specific facts
- **Larger chunks**: More context, better for understanding relationships
- **More overlap**: Better continuity across chunk boundaries

### Query Parameters

Fine-tune query behavior:

```python
response = rag.query(
    question="Explain the theory behind LENR",
    store_name=store_name,
    model="gemini-2.5-pro",          # Use more powerful model
    temperature=0.3,                  # Lower = more focused
    max_output_tokens=4096            # Longer responses
)
```

Temperature guide:
- `0.0-0.3`: Precise, factual responses
- `0.4-0.7`: Balanced creativity and accuracy
- `0.8-1.0`: More creative, diverse responses

### Working with Citations

Extract and use citation information:

```python
response = rag.query("What experimental methods exist?", store_name)

# Print all citations
for i, citation in enumerate(response["citations"], 1):
    print(f"\n[{i}] {citation.get('title', 'Untitled')}")
    print(f"    URI: {citation.get('uri', 'N/A')}")
    print(f"    Excerpt: {citation.get('text', '')[:100]}...")

# Access grounding metadata
if response["grounding_metadata"]:
    print("Grounding confidence:", response["grounding_metadata"])
```

### Store Management

```python
# List all stores
stores = rag.list_stores()
for store in stores:
    print(f"{store['display_name']}: {store['name']}")

# Get store details
store_info = rag.get_store(store_name)
print(f"Created: {store_info['create_time']}")
print(f"Updated: {store_info['update_time']}")

# Delete a store
rag.delete_store(store_name)
```

## API Reference

### GeminiRAG Class

#### Constructor

```python
GeminiRAG(api_key: Optional[str] = None, default_model: str = "gemini-2.5-flash")
```

#### Methods

##### create_store
```python
create_store(display_name: str) -> str
```
Create a new file search store.

##### list_stores
```python
list_stores() -> List[Dict[str, Any]]
```
List all available stores.

##### get_store
```python
get_store(store_name: str) -> Dict[str, Any]
```
Get information about a specific store.

##### upload_file
```python
upload_file(
    file_path: Union[str, Path],
    store_name: str,
    metadata: Optional[Dict[str, str]] = None,
    chunking_config: Optional[Dict[str, int]] = None
) -> str
```
Upload and index a file.

##### query
```python
query(
    question: str,
    store_name: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_output_tokens: int = 2048
) -> Dict[str, Any]
```
Query the RAG system.

##### delete_store
```python
delete_store(store_name: str) -> bool
```
Delete a store and all its contents.

##### batch_upload
```python
batch_upload(
    file_paths: List[Union[str, Path]],
    store_name: str,
    metadata_fn: Optional[callable] = None
) -> List[str]
```
Upload multiple files.

## Examples

See the `examples/` directory for complete working examples:

- `basic_usage.py`: Simple document upload and query
- `advanced_usage.py`: Metadata, chunking, and advanced features
- `batch_upload.py`: Batch processing of multiple documents

### Running Examples

```bash
# Set your API key
export GOOGLE_API_KEY=your_key_here

# Run basic example
python examples/basic_usage.py

# Run advanced example
python examples/advanced_usage.py

# Run batch upload example
python examples/batch_upload.py
```

## Supported File Types

- PDF (`.pdf`)
- Text (`.txt`)
- Markdown (`.md`)
- HTML (`.html`)
- Word Documents (`.docx`)

Maximum file size: 100 MB per document

## Pricing

- **Storage**: Free (1 GB free tier, up to 1 TB with paid tiers)
- **Indexing embeddings**: $0.15 per 1M tokens
- **Query embeddings**: Free
- **Model inference**: Standard Gemini API pricing

## Best Practices

1. **Organize with metadata**: Use consistent metadata keys for easy filtering
2. **Choose chunk size wisely**: Balance between precision and context
3. **Use appropriate models**: Flash for speed, Pro for complex reasoning
4. **Monitor API usage**: Track your indexing costs
5. **Clean up unused stores**: Delete stores you no longer need

## Troubleshooting

### API Key Not Found
```
ValueError: GOOGLE_API_KEY not found in environment
```
Solution: Set the `GOOGLE_API_KEY` environment variable or pass it to the constructor.

### File Too Large
```
ValueError: File too large: 150.00 MB (max 100 MB)
```
Solution: Split large files or compress them before uploading.

### Model Not Available
```
Error: Model not found
```
Solution: Use `gemini-2.5-flash` or `gemini-2.5-pro` only.

## Getting Help

- Check the [README.md](README.md) for overview and quick start
- Review example scripts in `examples/`
- Open an issue on GitHub for bugs or questions
