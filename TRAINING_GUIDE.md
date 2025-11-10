# How to Train Your RAG System

Guide to adding knowledge and optimizing your LENR RAG system.

---

## Understanding "Training" in RAG

**Important:** This RAG system uses Google's Gemini API - you **cannot** fine-tune the underlying AI model itself. Instead, "training" means:

1. **Adding documents** to teach the system about your domain
2. **Organizing knowledge** into searchable stores
3. **Optimizing retrieval** through good document structure
4. **Testing queries** to improve results

The system automatically creates embeddings when you upload documents.

---

## Table of Contents

1. [Quick Start: Add Your First Documents](#quick-start-add-your-first-documents)
2. [Document Preparation](#document-preparation)
3. [Uploading Documents](#uploading-documents)
4. [How the System Learns](#how-the-system-learns)
5. [Organizing Your Knowledge Base](#organizing-your-knowledge-base)
6. [Testing and Validation](#testing-and-validation)
7. [Optimization Tips](#optimization-tips)
8. [Advanced Techniques](#advanced-techniques)

---

## Quick Start: Add Your First Documents

### Method 1: Web UI (Easiest)

```bash
# 1. Start the interface
streamlit run web_ui/app.py

# 2. In the sidebar:
#    - Create a store: "my-knowledge-base"
#    - Click "Upload Documents"
#    - Select your PDF/Excel/TXT files
#    - Click "Upload to Store"

# 3. Wait for upload to complete
#    You'll see: "✅ Uploaded: filename"

# 4. Test it!
#    Ask: "What topics are covered in my documents?"
```

### Method 2: Python Script

```python
from src.rag.gemini_rag import GeminiRAG
from pathlib import Path

# Initialize
rag = GeminiRAG()

# Create knowledge base
store = rag.create_store("my-knowledge-base")

# Add documents
documents = [
    "path/to/research_paper.pdf",
    "path/to/data_analysis.xlsx",
    "path/to/notes.txt"
]

for doc in documents:
    print(f"Adding {Path(doc).name}...")

    if doc.endswith('.xlsx'):
        rag.upload_excel(
            doc,
            store,
            metadata={"category": "data"}
        )
    else:
        rag.upload_file(
            doc,
            store,
            metadata={"category": "research"}
        )

print("✓ Knowledge base created!")

# Test it
response = rag.query("What information do I have?", store)
print(response["answer"])
```

---

## Document Preparation

### Best Document Formats

**Highly Recommended:**
- ✅ **PDF** - Research papers, reports, manuals
- ✅ **Excel** - Data tables, experimental results
- ✅ **Text** - Notes, transcripts, plain documentation
- ✅ **Markdown** - Well-structured technical docs

**Also Supported:**
- 📄 Word documents (.docx)
- 📄 HTML files

### Preparing Documents for Best Results

#### 1. Structure Your Documents

**Good structure:**
```
Title: Clear and Descriptive
Author: Dr. Smith, 2024

Abstract/Summary
---------------
Brief overview of content...

Section 1: Introduction
-----------------------
Detailed content with clear headers...

Section 2: Methods
------------------
Step-by-step procedures...

References
----------
[1] Source citation...
```

**Why this helps:**
- Clear sections help retrieval
- Headers make context obvious
- Structure improves citation accuracy

#### 2. Clean Your Data

**Before uploading:**

```bash
# Remove password protection from PDFs
# Use tools like: qpdf, pdftk

# Clean Excel files:
- Remove empty rows/columns
- Add descriptive sheet names
- Include a summary/readme sheet
- Use consistent column headers

# Text files:
- Use UTF-8 encoding
- Remove special characters if causing issues
- Add section markers (###, ---, etc.)
```

#### 3. Add Metadata

Metadata helps organize and filter your knowledge:

```python
# Research paper
rag.upload_file(
    "paper.pdf",
    store,
    metadata={
        "type": "research_paper",
        "author": "Dr. Smith",
        "year": "2024",
        "journal": "Nature",
        "peer_reviewed": "yes",
        "topic": "LENR",
        "experiment_type": "electrolysis"
    }
)

# Excel data
rag.upload_excel(
    "results.xlsx",
    store,
    metadata={
        "type": "experimental_data",
        "date": "2024-01-15",
        "researcher": "Lab Team A",
        "project": "Project Alpha"
    }
)
```

#### 4. Break Up Large Documents

**If you have a 500-page manual:**

```python
# Option 1: Split by chapter (better)
chapters = [
    "manual_chapter1_intro.pdf",
    "manual_chapter2_methods.pdf",
    "manual_chapter3_results.pdf"
]

for chapter in chapters:
    rag.upload_file(chapter, store)

# Option 2: Upload whole thing (works, but less precise citations)
rag.upload_file("manual_complete.pdf", store)
```

**Recommendation:** Keep files under 50 MB each for best performance.

---

## Uploading Documents

### Batch Upload All Documents

```python
from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("complete-knowledge-base")

# Define your document directory
docs_dir = Path("my_documents")

# Upload all supported files
for file_path in docs_dir.rglob("*"):
    if not file_path.is_file():
        continue

    suffix = file_path.suffix.lower()

    try:
        if suffix in ['.xlsx', '.xls']:
            print(f"Uploading Excel: {file_path.name}")
            rag.upload_excel(file_path, store)

        elif suffix in ['.pdf', '.txt', '.md', '.docx', '.html']:
            print(f"Uploading document: {file_path.name}")
            rag.upload_file(file_path, store)

        else:
            print(f"Skipping unsupported: {file_path.name}")

    except Exception as e:
        print(f"Error with {file_path.name}: {e}")

print("\n✓ All documents uploaded!")
```

### Upload with Automatic Metadata

```python
def extract_metadata_from_filename(file_path):
    """Extract metadata from filename pattern."""
    # Example: "Smith_2024_LENR_Research.pdf"
    parts = Path(file_path).stem.split('_')

    metadata = {}

    if len(parts) >= 2:
        metadata['author'] = parts[0]
        metadata['year'] = parts[1]

    if len(parts) >= 3:
        metadata['topic'] = parts[2]

    if len(parts) >= 4:
        metadata['type'] = parts[3]

    return metadata

# Use it
files = Path("papers").glob("*.pdf")

for file in files:
    metadata = extract_metadata_from_filename(file)
    rag.upload_file(file, store, metadata=metadata)
```

---

## How the System Learns

### The Embedding Process

When you upload a document:

```
1. Upload Document (PDF/Excel/TXT)
        ↓
2. Document Processing
   - Extract text
   - Split into chunks (~2000 tokens)
   - Clean and normalize
        ↓
3. Create Embeddings
   - Google's embedding model
   - Converts text to vectors
   - Captures semantic meaning
        ↓
4. Store in File Search Store
   - Indexed for fast retrieval
   - Stored indefinitely
   - Searchable via queries
        ↓
5. Ready for Queries!
```

### What Happens During a Query

```
1. User asks question
        ↓
2. Question is embedded
   - Same embedding model
   - Creates query vector
        ↓
3. Semantic Search
   - Finds similar vectors
   - Retrieves top matches
   - Ranks by relevance
        ↓
4. Context Assembly
   - Top chunks sent to Gemini
   - Model generates answer
   - Includes citations
        ↓
5. Return Answer + Sources
```

### Important Notes

**You DO NOT control:**
- ❌ The embedding model (Google's proprietary)
- ❌ The chunk size (automatic)
- ❌ The base AI model weights (no fine-tuning)

**You DO control:**
- ✅ What documents to add
- ✅ How to structure them
- ✅ Metadata for organization
- ✅ Query parameters (temperature, model)

---

## Organizing Your Knowledge Base

### Strategy 1: Single Store (Simple)

**Best for:** Small projects, personal research

```python
# One store for everything
store = rag.create_store("all-my-documents")

# Upload everything
rag.upload_file("paper1.pdf", store, metadata={"type": "paper"})
rag.upload_file("data1.xlsx", store, metadata={"type": "data"})
rag.upload_file("notes.txt", store, metadata={"type": "notes"})
```

**Pros:** Simple, everything searchable together
**Cons:** May return less relevant results as it grows

### Strategy 2: Multiple Stores by Topic

**Best for:** Multiple projects, different domains

```python
# Create topic-specific stores
lenr_store = rag.create_store("lenr-research")
fusion_store = rag.create_store("fusion-research")
data_store = rag.create_store("experimental-data")

# Upload to appropriate stores
rag.upload_file("lenr_paper.pdf", lenr_store)
rag.upload_file("fusion_paper.pdf", fusion_store)
rag.upload_excel("results.xlsx", data_store)

# Query specific stores
lenr_answer = rag.query("LENR mechanisms?", lenr_store)
fusion_answer = rag.query("Fusion temperature?", fusion_store)
```

**Pros:** Focused results, better organization
**Cons:** More stores to manage

### Strategy 3: Hierarchical Organization

**Best for:** Large knowledge bases

```python
# Main categories
literature_store = rag.create_store("literature-reviews")
experiments_store = rag.create_store("experimental-data")
theory_store = rag.create_store("theoretical-models")

# Use metadata for sub-categories
rag.upload_file(
    "paper.pdf",
    literature_store,
    metadata={
        "subcategory": "electrolysis",
        "decade": "2020s",
        "institution": "MIT"
    }
)
```

### Recommended Structure

```
Your Knowledge Base
│
├── research-papers/          (Store 1)
│   ├── paper1.pdf           (metadata: author, year, topic)
│   ├── paper2.pdf
│   └── paper3.pdf
│
├── experimental-data/        (Store 2)
│   ├── results_2024.xlsx    (metadata: date, experiment_type)
│   ├── measurements.xlsx
│   └── analysis.xlsx
│
├── reference-materials/      (Store 3)
│   ├── handbook.pdf         (metadata: type=reference)
│   ├── standards.pdf
│   └── protocols.txt
│
└── meeting-notes/           (Store 4)
    ├── notes_jan.txt        (metadata: date, attendees)
    └── notes_feb.txt
```

---

## Testing and Validation

### 1. Start with Known Questions

After uploading documents, test with questions you **know** the answer to:

```python
# Test questions about content you uploaded
test_questions = [
    "What is the main topic discussed?",
    "Who are the authors mentioned?",
    "What experiments were conducted?",
    "What were the key findings?"
]

for question in test_questions:
    response = rag.query(question, store)
    print(f"\nQ: {question}")
    print(f"A: {response['answer']}")
    print(f"Citations: {len(response['citations'])}")

    # Check if answer makes sense
    # Verify citations point to right sources
```

### 2. Verify Citations

```python
response = rag.query("What is the experimental procedure?", store)

print("Answer:", response['answer'])
print("\nVerifying citations:")

for i, citation in enumerate(response['citations'], 1):
    print(f"\n[{i}] {citation.get('title')}")
    print(f"    Excerpt: {citation.get('text', '')[:100]}...")

    # Read excerpt - does it support the answer?
    # Is the source relevant?
```

### 3. Test Different Query Styles

```python
# Same question, different ways
questions = [
    "What is LENR?",                          # Direct
    "Explain Low-Energy Nuclear Reactions",   # Formal
    "Tell me about cold fusion",              # Colloquial
    "Define LENR and its principles"          # Detailed
]

for q in questions:
    response = rag.query(q, store, temperature=0.3)
    print(f"\nQ: {q}")
    print(f"A: {response['answer'][:150]}...")
```

### 4. Measure Coverage

```python
# Test what your system knows
coverage_tests = [
    "List all topics covered in the documents",
    "What time periods are discussed?",
    "What researchers are mentioned?",
    "What experimental methods are described?",
    "What data is available?"
]

for test in coverage_tests:
    response = rag.query(test, store)
    print(f"\n{test}")
    print(f"→ {response['answer']}")
```

---

## Optimization Tips

### 1. Document Quality Over Quantity

```python
# ❌ Bad: Upload everything
rag.upload_file("random_notes.txt", store)  # Unstructured
rag.upload_file("email_dump.txt", store)    # Noisy
rag.upload_file("draft_v1.pdf", store)      # Outdated

# ✅ Good: Upload curated, quality documents
rag.upload_file("final_report_2024.pdf", store)      # Final version
rag.upload_file("peer_reviewed_paper.pdf", store)    # Quality source
rag.upload_file("official_data.xlsx", store)         # Authoritative
```

### 2. Use Descriptive Filenames

```python
# ❌ Bad filenames
"doc1.pdf"
"data.xlsx"
"file.txt"

# ✅ Good filenames
"Smith_2024_LENR_Electrolysis_Methods.pdf"
"Experiment_Results_Jan2024_Team_A.xlsx"
"Meeting_Notes_Budget_Discussion_2024-01-15.txt"
```

### 3. Temperature Settings

```python
# Factual queries - low temperature
response = rag.query(
    "What was the exact temperature in experiment 5?",
    store,
    temperature=0.1  # Precise, factual
)

# Analytical queries - medium temperature
response = rag.query(
    "Compare the different experimental approaches",
    store,
    temperature=0.5  # Balanced
)

# Creative queries - higher temperature
response = rag.query(
    "What are potential future research directions?",
    store,
    temperature=0.8  # Creative, exploratory
)
```

### 4. Excel File Optimization

```python
# ✅ Best: Structured data with clear headers
rag.upload_excel(
    "results.xlsx",
    store,
    conversion_format="markdown",  # Preserves table structure
    metadata={"data_type": "experimental_results"}
)

# Add a summary sheet to your Excel files:
# Sheet 1: "Summary" - Overview of data
# Sheet 2: "Raw Data" - Detailed measurements
# Sheet 3: "Analysis" - Calculations and insights
```

### 5. Regular Updates

```python
# Keep knowledge base current
def update_knowledge_base(store_name):
    """Add new documents to existing store."""

    # List new files
    new_files = Path("new_documents").glob("*.*")

    for file in new_files:
        # Upload new document
        if file.suffix == '.xlsx':
            rag.upload_excel(file, store_name)
        else:
            rag.upload_file(file, store_name)

        # Move to processed folder
        file.rename(f"processed/{file.name}")

    print("✓ Knowledge base updated")

# Run monthly/weekly
update_knowledge_base("my-knowledge-base")
```

---

## Advanced Techniques

### 1. Domain-Specific Chunking

For Excel files with specific structure:

```python
# Different formats for different use cases
rag.upload_excel(
    "data_table.xlsx",
    store,
    conversion_format="markdown",  # Best for tables
    chunking_config={
        "max_tokens_per_chunk": 512,
        "max_overlap_tokens": 128
    }
)

rag.upload_excel(
    "narrative_data.xlsx",
    store,
    conversion_format="text"  # Better for text-heavy cells
)
```

### 2. Metadata-Based Filtering

```python
# Upload with rich metadata
papers = [
    ("paper1.pdf", {"year": "2024", "method": "electrolysis"}),
    ("paper2.pdf", {"year": "2023", "method": "gas_loading"}),
    ("paper3.pdf", {"year": "2024", "method": "plasma"})
]

for file, meta in papers:
    rag.upload_file(file, store, metadata=meta)

# Query with context
response = rag.query(
    "What are recent electrolysis results?",
    store
)
# System will use metadata to find relevant docs
```

### 3. Multi-Store Synthesis

```python
# Query across multiple stores
stores = {
    "literature": rag.create_store("lit-review"),
    "experiments": rag.create_store("exp-data"),
    "theory": rag.create_store("theory")
}

# Upload to each
rag.upload_file("papers.pdf", stores["literature"])
rag.upload_excel("data.xlsx", stores["experiments"])
rag.upload_file("models.pdf", stores["theory"])

# Query each and synthesize
lit_answer = rag.query("What does literature say?", stores["literature"])
exp_answer = rag.query("What does data show?", stores["experiments"])
theory_answer = rag.query("What does theory predict?", stores["theory"])

print("Literature:", lit_answer['answer'])
print("Experiments:", exp_answer['answer'])
print("Theory:", theory_answer['answer'])
```

### 4. Automated Quality Checks

```python
def quality_check_upload(file_path, store_name):
    """Upload with validation."""

    # Check file size
    size_mb = Path(file_path).stat().st_size / (1024*1024)
    if size_mb > 90:  # Leave margin below 100MB limit
        print(f"⚠️ Warning: {file_path} is {size_mb:.1f}MB")
        return False

    # Upload
    try:
        if file_path.endswith('.xlsx'):
            rag.upload_excel(file_path, store_name)
        else:
            rag.upload_file(file_path, store_name)

        # Test with a query
        response = rag.query(
            f"What is in {Path(file_path).stem}?",
            store_name
        )

        if response['citations']:
            print(f"✓ {Path(file_path).name} uploaded and verified")
            return True
        else:
            print(f"⚠️ {Path(file_path).name} uploaded but no citations")
            return False

    except Exception as e:
        print(f"❌ Error with {Path(file_path).name}: {e}")
        return False
```

---

## Monitoring Your Knowledge Base

### Track What You've Added

```python
# List all stores
stores = rag.list_stores()

print("Your Knowledge Bases:")
for store in stores:
    print(f"\n📚 {store['display_name']}")
    print(f"   Created: {store['create_time']}")
    print(f"   Updated: {store['update_time']}")
```

### Test Coverage

```python
def test_knowledge_coverage(store_name):
    """Test what the system knows."""

    tests = {
        "Topics": "List all main topics in the knowledge base",
        "Time Range": "What time period is covered?",
        "Authors": "Who are the key researchers mentioned?",
        "Methods": "What methodologies are described?",
        "Data Types": "What types of data are available?"
    }

    print(f"\nKnowledge Coverage for: {store_name}\n")

    for category, question in tests.items():
        response = rag.query(question, store_name)
        print(f"{category}:")
        print(f"  {response['answer'][:200]}...\n")
```

---

## Best Practices Summary

### ✅ DO:
- Upload high-quality, authoritative documents
- Use clear, descriptive filenames
- Add detailed metadata
- Test with known questions
- Verify citations
- Organize into logical stores
- Keep documents updated
- Structure documents with clear sections

### ❌ DON'T:
- Upload duplicates
- Use vague filenames ("doc1.pdf")
- Upload drafts or outdated versions
- Exceed 100MB per file
- Skip metadata
- Mix unrelated topics in one store
- Upload without testing

---

## Troubleshooting

### "No relevant citations found"

**Problem:** System can't find information

**Solutions:**
1. Check document actually contains that information
2. Try rephrasing your question
3. Check if documents uploaded successfully
4. Verify content is searchable (not scanned image PDFs)

### "Low quality answers"

**Problem:** Answers are generic or wrong

**Solutions:**
1. Upload more authoritative sources
2. Add documents with more detail
3. Use lower temperature (0.1-0.3)
4. Check that uploaded documents are relevant

### "Slow uploads"

**Problem:** Takes long time to upload

**Solutions:**
1. Check file size (< 100MB)
2. Check internet connection
3. Upload during off-peak hours
4. Consider splitting large files

---

## Next Steps

1. **Start small** - Upload 5-10 key documents
2. **Test thoroughly** - Ask questions you know answers to
3. **Expand gradually** - Add more as you validate
4. **Organize** - Create logical stores and metadata
5. **Monitor** - Regularly test and update

---

**Remember:** You're not "training" an AI model - you're building a searchable knowledge base. The better organized and higher quality your documents, the better your results!

---

For more help:
- **Usage Guide:** `HOW_TO_USE.md`
- **Quick Start:** `QUICK_START.md`
- **API Docs:** `USAGE.md`
