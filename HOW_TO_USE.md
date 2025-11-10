# How to Use the LENR RAG System

Complete guide for using your RAG system with interactive citations.

---

## Table of Contents

1. [First-Time Setup](#first-time-setup)
2. [Using the Web Interface](#using-the-web-interface)
3. [Using Python Scripts](#using-python-scripts)
4. [Uploading Your Own Documents](#uploading-your-own-documents)
5. [Asking Questions](#asking-questions)
6. [Understanding Citations](#understanding-citations)
7. [Common Workflows](#common-workflows)
8. [Tips & Best Practices](#tips--best-practices)
9. [Troubleshooting](#troubleshooting)

---

## First-Time Setup

### Step 1: Install Python Requirements

Open terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This installs:
- Google Gemini API client
- Streamlit (web interface)
- Pandas & OpenPyxl (Excel support)
- PDF viewing tools
- Other dependencies

**Wait for installation to complete** (may take 1-2 minutes).

### Step 2: Get Google API Key

1. Visit https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### Step 3: Configure API Key

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit the file
nano .env   # or use any text editor
```

Add your API key:
```
GOOGLE_API_KEY=AIzaSyYourActualKeyHere
```

Save and close the file.

### Step 4: Generate Demo Excel Files (Optional)

```bash
python demo_data/create_sample_files.py
```

This creates 4 sample Excel files in `demo_data/`.

### ✅ Setup Complete!

You're ready to use the system.

---

## Using the Web Interface

The web interface provides the easiest way to use the RAG system with interactive citations.

### Starting the Web Interface

```bash
streamlit run web_ui/app.py
```

Your browser will automatically open to `http://localhost:8501`

If it doesn't open automatically, manually visit that URL.

### Interface Overview

```
┌─────────────────────────────────────────────────────┐
│  Sidebar (Left)          │  Main Area (Right)       │
│  ─────────────────       │  ──────────────────      │
│  • System Status         │  • Ask Questions         │
│  • Select/Create Store   │  • View Answers          │
│  • Upload Documents      │  • See Citations         │
│  • Query Settings        │  • Browse History        │
└─────────────────────────────────────────────────────┘
```

### Workflow: Your First Query

#### 1. Create a Document Store

**In the sidebar:**
- Click "➕ Create New Store"
- Enter a name: `my-first-store`
- Click "Create"
- ✅ You'll see "Using: my-first-store"

**What is a store?**
A store is like a folder for your documents. It keeps them organized and searchable.

#### 2. Upload Documents

**In the sidebar:**
- Click "📤 Upload Documents" to expand
- Click "Browse files"
- Navigate to `demo_data/`
- Select one or more files:
  - `lenr_overview_2024.txt`
  - `experimental_methods.txt`
  - Or any of your own files
- Click "Upload to Store"
- Wait for "✅ Uploaded: filename" messages

**Supported file types:**
- PDF (`.pdf`)
- Text (`.txt`)
- Markdown (`.md`)
- Word (`.docx`)
- Excel (`.xlsx`, `.xls`)

#### 3. Ask Your First Question

**In the main area:**

Type a question in the text box:
```
What are the main experimental methods used in LENR research?
```

Click **🔍 Search**

**Wait 5-15 seconds** for the system to:
- Search your documents
- Find relevant passages
- Generate an answer with citations

#### 4. View the Answer with Citations

You'll see:

**Answer Section:**
```
Low-Energy Nuclear Reactions (LENR) research employs three primary
experimental methods: electrolytic cells, gas loading, and plasma
methods [1]. The electrolytic approach uses heavy water with palladium
cathodes [2], while gas loading involves high-pressure deuterium...
```

**References Section:**
```
[1] Experimental Methods in LENR Research
    > "The most widely used method, based on the original
       Fleischmann-Pons experiment..."
    Category: research | Year: 2024
    📄 View Source Document

[2] LENR Overview 2024
    > "Palladium cathode (99.99% purity), 1-10 mm diameter..."
    ...
```

#### 5. Explore Citations

**Click on a reference [1]:**
- Scroll automatically to that citation
- See full excerpt text
- Click "View full excerpt" for complete passage
- Click "📄 View Source Document" to open the file

**This is the OpenEvidence-style citation system!**

---

## Using Python Scripts

For automation or custom workflows, use Python directly.

### Basic Example

Create a file `my_query.py`:

```python
from src.rag.gemini_rag import GeminiRAG

# Initialize
rag = GeminiRAG()

# Create store
store_name = rag.create_store("python-demo")
print(f"Created store: {store_name}")

# Upload a document
rag.upload_file(
    file_path="demo_data/lenr_overview_2024.txt",
    store_name=store_name,
    metadata={"category": "research", "year": "2024"}
)
print("Document uploaded")

# Ask a question
response = rag.query(
    question="What is LENR?",
    store_name=store_name
)

# Print answer
print("\nAnswer:")
print(response["answer"])

# Print citations
print(f"\nCitations: {len(response['citations'])}")
for i, citation in enumerate(response['citations'], 1):
    print(f"[{i}] {citation.get('title', 'Untitled')}")
```

Run it:
```bash
python my_query.py
```

### Excel File Example

```python
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store_name = rag.create_store("excel-demo")

# Upload Excel file (automatically converted)
rag.upload_excel(
    file_path="demo_data/experimental_results.xlsx",
    store_name=store_name,
    metadata={"type": "experimental_data"},
    conversion_format="markdown"  # or "text" or "json"
)

# Query Excel data with optimized settings
response = rag.query_excel_data(
    question="What was the highest excess heat recorded?",
    store_name=store_name
)

print(response["answer"])
```

### Batch Upload Example

```python
from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store_name = rag.create_store("batch-demo")

# Upload all text files from a directory
text_files = list(Path("demo_data").glob("*.txt"))

for file in text_files:
    print(f"Uploading {file.name}...")
    rag.upload_file(file, store_name)

print(f"Uploaded {len(text_files)} files")

# Query
response = rag.query(
    "Summarize the key findings across all documents",
    store_name
)
print(response["answer"])
```

---

## Uploading Your Own Documents

### Preparing Your Files

**Best practices:**

1. **Use clear filenames**
   - `project_report_2024.pdf` ✅
   - `document.pdf` ❌

2. **Organize by topic**
   - Put related files in same folder
   - Upload them to the same store

3. **Add metadata**
   - Author, date, category
   - Helps with filtering later

4. **Check file size**
   - Maximum: 100 MB per file
   - Larger files: split into sections

### Uploading Different File Types

#### PDFs

```python
rag.upload_file(
    file_path="path/to/research_paper.pdf",
    store_name=store_name,
    metadata={
        "author": "Dr. Smith",
        "year": "2024",
        "category": "research",
        "peer_reviewed": "yes"
    }
)
```

#### Excel Spreadsheets

```python
rag.upload_excel(
    file_path="path/to/data.xlsx",
    store_name=store_name,
    metadata={
        "dataset": "experimental_results",
        "date": "2024-03-15"
    },
    conversion_format="markdown"  # Best for tables
)
```

**Excel tips:**
- Use markdown format for data tables
- Use text format for readability
- Use JSON for structured data

#### Word Documents

```python
rag.upload_file(
    file_path="path/to/report.docx",
    store_name=store_name,
    metadata={"type": "report", "status": "final"}
)
```

#### Multiple Files at Once

**Via web UI:**
1. Click "Browse files"
2. Select multiple files (Ctrl+Click or Cmd+Click)
3. Click "Upload to Store"

**Via Python:**
```python
files = [
    "doc1.pdf",
    "doc2.xlsx",
    "doc3.txt"
]

for file in files:
    if file.endswith('.xlsx'):
        rag.upload_excel(file, store_name)
    else:
        rag.upload_file(file, store_name)
```

---

## Asking Questions

### Question Types

#### 1. Factual Questions

**Best for:** Specific facts, dates, names

**Temperature:** 0.1 - 0.3 (precise)

Examples:
```
Who discovered cold fusion?
What year was LENR announced?
What is the melting point of palladium?
```

#### 2. Explanatory Questions

**Best for:** Understanding concepts

**Temperature:** 0.3 - 0.5 (balanced)

Examples:
```
How does electrolysis work in LENR experiments?
Explain the lattice-assisted reaction model
What is the difference between hot and cold fusion?
```

#### 3. Comparative Questions

**Best for:** Analyzing differences

**Temperature:** 0.4 - 0.6

Examples:
```
Compare palladium and nickel as cathode materials
What are the pros and cons of electrolysis vs gas loading?
How do different theoretical models explain LENR?
```

#### 4. Analytical Questions

**Best for:** Insights and synthesis

**Temperature:** 0.6 - 0.8 (creative)

Examples:
```
What are the main challenges facing LENR commercialization?
Synthesize the key findings from all experimental papers
What trends emerge in LENR research over the past decade?
```

#### 5. Data Questions (Excel)

**Best for:** Spreadsheet data

**Use:** `query_excel_data()` method

Examples:
```
What was the average experiment duration?
Which researcher had the most successful experiments?
How does temperature correlate with excess heat?
What materials are most cost-effective?
```

### Question Tips

**✅ Good Questions:**
- Specific: "What were the results of the 2024 experiments?"
- Context-rich: "According to the experimental methods paper..."
- Data-focused: "What is the average yield in the database?"

**❌ Avoid:**
- Too vague: "Tell me about science"
- Outside scope: "What's the weather?" (not in your docs)
- Opinion-based: "Which theory is best?" (ask for comparison instead)

### Adjusting Query Settings

**In Web UI (Sidebar):**

**Model:**
- `gemini-2.5-flash` - Fast, efficient (recommended)
- `gemini-2.5-pro` - More powerful, detailed (costs more)

**Temperature:**
```
0.0 ─────────── 1.0
│        │      │
Precise  Mixed  Creative
```

- **0.0-0.3:** Factual, data queries
- **0.4-0.6:** General questions
- **0.7-1.0:** Creative analysis, brainstorming

**In Python:**
```python
response = rag.query(
    question="Your question",
    store_name=store_name,
    model="gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=2048
)
```

---

## Understanding Citations

### Citation Format

Citations appear as numbered references like academic papers:

```
Text with claim [1]. Another fact [2]. Multiple sources [3,4].
```

### Reference Details

Each citation shows:

```
[1] Document Title
    > "Excerpt from the original text where this
       information was found..."

    Metadata: category: research | year: 2024

    📄 View Source Document
```

**Parts:**
1. **Number** - Reference identifier
2. **Title** - Source document name
3. **Excerpt** - Relevant text passage (first 300 chars)
4. **Metadata** - File information you added
5. **Link** - Open the original document

### Using Citations

#### Verify Information

**Always check citations to ensure accuracy:**

1. Click the citation number `[1]`
2. Read the full excerpt
3. Click "View full excerpt" for complete context
4. If available, open source document

#### Follow Citation Chains

If one source references another:
1. Note the related citations
2. Query for those specific sources
3. Build a complete understanding

#### Export Citations

**For reports or papers:**

```python
from src.utils.citation_formatter import CitationFormatter

# Format citations as markdown
markdown = CitationFormatter.create_reference_markdown(
    response['citations']
)

# Save to file
with open('citations.md', 'w') as f:
    f.write(markdown)
```

---

## Common Workflows

### Workflow 1: Research Paper Analysis

**Goal:** Extract key points from multiple papers

```bash
# 1. Start web UI
streamlit run web_ui/app.py

# 2. Create store
Store name: "research-papers"

# 3. Upload papers
- Upload all PDFs from your research folder
- Add metadata: author, year, journal

# 4. Query for synthesis
"Summarize the key findings across all papers"
"What are the common experimental methods?"
"Which papers report the highest yields?"

# 5. Export results
Copy answer and citations to your report
```

### Workflow 2: Data Analysis

**Goal:** Query Excel data about experiments

```python
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("experiment-data")

# Upload experimental data
rag.upload_excel("results.xlsx", store)
rag.upload_excel("measurements.xlsx", store)

# Ask analytical questions
questions = [
    "What was the average yield?",
    "Which experiment had the longest duration?",
    "How does temperature affect the results?",
    "Compare experiments using palladium vs nickel"
]

for q in questions:
    response = rag.query_excel_data(q, store)
    print(f"Q: {q}")
    print(f"A: {response['answer']}\n")
```

### Workflow 3: Literature Review

**Goal:** Organize and search academic literature

```python
from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("literature-review")

# Upload all papers with metadata
papers = Path("literature").glob("*.pdf")

for paper in papers:
    # Extract info from filename: Author_Year_Topic.pdf
    parts = paper.stem.split('_')

    rag.upload_file(
        paper,
        store,
        metadata={
            "author": parts[0],
            "year": parts[1],
            "topic": parts[2]
        }
    )

# Research questions
response = rag.query(
    "What is the consensus on LENR mechanisms across all papers?",
    store,
    temperature=0.5
)

# Save to file
with open('literature_review.txt', 'w') as f:
    f.write(f"Question: {response['answer']}\n\n")
    f.write("Sources:\n")
    for i, cite in enumerate(response['citations'], 1):
        f.write(f"[{i}] {cite['title']}\n")
```

### Workflow 4: Real-Time Research Assistant

**Goal:** Interactive question-answering session

```bash
# Start web UI
streamlit run web_ui/app.py

# Upload your documents
# Then use it like ChatGPT but with citations!

Query 1: "What is LENR?"
- Read answer and citations
- Click to verify sources

Query 2: "How does the experimental setup work?"
- See step-by-step from your docs
- Follow citation to detailed procedure

Query 3: "What were the results in Table 2?"
- Get data from Excel files
- See exact numbers with sources

# Query history is saved for reference
```

---

## Tips & Best Practices

### Getting Better Results

**1. Upload Related Documents Together**
```python
# Good: All LENR papers in one store
store = rag.create_store("lenr-research")
# Upload 10 related papers

# Less effective: One paper per store
```

**2. Use Descriptive Metadata**
```python
# Good
metadata = {
    "author": "Dr. Smith",
    "year": "2024",
    "institution": "MIT",
    "peer_reviewed": "yes",
    "experiment_type": "electrolysis"
}

# Less helpful
metadata = {"file": "doc1"}
```

**3. Ask Follow-Up Questions**
```
First: "What is LENR?"
Then: "What experimental methods are mentioned?"
Then: "What were the results of the electrolysis experiments?"
```

**4. Verify Important Information**
- Always check citations for critical facts
- Compare multiple sources
- Look at original data in Excel files

**5. Organize Stores by Project**
```
my-stores/
  ├── project-alpha/     (specific project docs)
  ├── literature-review/ (academic papers)
  ├── experimental-data/ (Excel files)
  └── reference-docs/    (manuals, guides)
```

### Performance Tips

**Faster Queries:**
- Use `gemini-2.5-flash` model
- Lower temperature for factual questions
- Reduce max_output_tokens if you don't need long answers

**Better Citations:**
- Upload high-quality source documents
- Include documents with clear structure
- Add good metadata for context

**Excel Files:**
- Use markdown format for tabular data
- Add descriptive sheet names
- Include a summary sheet

---

## Troubleshooting

### Common Issues

#### "GOOGLE_API_KEY not found"

**Problem:** API key not configured

**Solution:**
```bash
# Check if .env file exists
ls -la .env

# If not, create it
cp .env.example .env

# Edit and add your key
nano .env
```

#### "Module not found" Errors

**Problem:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt

# If still issues, try upgrading pip
pip install --upgrade pip
pip install -r requirements.txt
```

#### Web UI Won't Start

**Problem:** Streamlit not installed or port in use

**Solution:**
```bash
# Install Streamlit
pip install streamlit

# Try different port
streamlit run web_ui/app.py --server.port 8502
```

#### No Citations in Response

**Problem:** Model didn't find relevant sources

**Solutions:**
1. Rephrase your question to be more specific
2. Check that documents are uploaded
3. Try a different query about content you know is in the docs
4. Verify files uploaded successfully

#### "File too large" Error

**Problem:** File exceeds 100 MB limit

**Solution:**
```bash
# Check file size
ls -lh yourfile.pdf

# Split large PDFs (if on Linux/Mac)
pdftk large.pdf burst output page_%02d.pdf

# Or compress the PDF
```

#### Excel File Not Working

**Problem:** Excel file format issues

**Solution:**
```bash
# Make sure pandas and openpyxl are installed
pip install pandas openpyxl

# Try converting to CSV first
# Open in Excel/Numbers, Save As CSV
# Then upload the CSV file
```

#### Slow Response Times

**Problem:** Large documents or complex queries

**Solutions:**
1. Use `gemini-2.5-flash` instead of pro
2. Upload fewer documents per store
3. Make questions more specific
4. Check your internet connection

### Getting Help

**If issues persist:**

1. Check the logs:
   ```bash
   # Web UI logs appear in terminal
   # Look for error messages
   ```

2. Verify API key is valid:
   - Visit https://aistudio.google.com/app/apikey
   - Check key hasn't expired
   - Try creating a new key

3. Test with demo files:
   ```bash
   python examples/citation_demo.py
   ```

4. Check GitHub issues:
   - See if others have similar problems
   - Search for error messages

---

## Next Steps

Now that you know how to use the system:

1. **Try the demo files** to understand features
2. **Upload your own documents** for real work
3. **Experiment with different query types**
4. **Explore the code** in `src/` to customize
5. **Read the API docs** in `USAGE.md` for advanced features

## Need More Help?

- **Quick Start:** `QUICK_START.md`
- **API Reference:** `USAGE.md`
- **Web UI Guide:** `web_ui/README.md`
- **Demo Data:** `demo_data/README.md`
- **Main README:** `README.md`

---

**Happy researching with interactive citations! 🎉**
