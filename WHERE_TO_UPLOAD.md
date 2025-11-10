# Where to Upload Your Files

Simple guide showing exactly where to put and upload your files.

---

## Quick Answer

You have **2 options**:

### Option 1: Upload Through Web Interface (Easiest) ⭐

**No need to move files anywhere!** Just:

1. **Start the web app:**
   ```bash
   streamlit run web_ui/app.py
   ```

2. **In the sidebar, click "📤 Upload Documents"**

3. **Click "Browse files"** - this opens a file picker

4. **Navigate to YOUR files** anywhere on your computer:
   - Desktop
   - Documents folder
   - Downloads
   - Any folder you have files in

5. **Select files and click "Upload to Store"**

The system copies them and indexes them automatically!

### Option 2: Use Python Script

Put your files **anywhere** you want, then reference them:

```python
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("my-store")

# Upload from ANY location
rag.upload_file("/Users/yourname/Desktop/research.pdf", store)
rag.upload_file("/Users/yourname/Documents/data.xlsx", store)
rag.upload_file("C:/Users/yourname/Downloads/paper.pdf", store)  # Windows
```

---

## File Organization (Optional)

If you want to organize files in the project:

```
LENR-Google/
│
├── my_documents/          ← Create this folder for YOUR files
│   ├── research/
│   │   ├── paper1.pdf
│   │   └── paper2.pdf
│   ├── data/
│   │   ├── experiments.xlsx
│   │   └── results.xlsx
│   └── notes/
│       └── meeting_notes.txt
│
├── demo_data/             ← Demo files (already included)
│   ├── lenr_overview_2024.txt
│   └── experimental_methods.txt
│
└── web_ui/
    └── app.py
```

**Create your own folder:**

```bash
# Create a folder for your documents
mkdir my_documents

# Put your files there
cp /path/to/your/file.pdf my_documents/

# Or organize by topic
mkdir my_documents/research
mkdir my_documents/data
```

---

## Step-by-Step: Upload Using Web UI

### Step 1: Start the App

```bash
cd /path/to/LENR-Google
streamlit run web_ui/app.py
```

Browser opens to `http://localhost:8501`

### Step 2: Create a Store

In the **sidebar** (left side):

```
┌─────────────────────────┐
│  🔬 LENR RAG System     │
│  Interactive Citations  │
│                         │
│  ✅ System Ready        │
│  ─────────────────      │
│  Document Store         │
│  ➕ Create New Store    │  ← Click this
│  └─> Enter name         │
│      [my-research]      │  ← Type name
│      [Create]           │  ← Click
└─────────────────────────┘
```

### Step 3: Upload Files

Still in the **sidebar**:

```
┌─────────────────────────┐
│  📤 Upload Documents    │  ← Click to expand
│  └─> Choose files       │
│      [Browse files]     │  ← Click this
│                         │
│  File picker opens:     │
│  Navigate to your files │
│  Select one or more     │
│  Click Open             │
│                         │
│  [Upload to Store]      │  ← Click to upload
└─────────────────────────┘
```

### Step 4: Wait for Upload

You'll see:
```
Uploading...
✅ Uploaded: your_file.pdf
✅ Uploaded: your_data.xlsx
```

### Step 5: Query!

In the **main area** (right side):

```
┌─────────────────────────────────────┐
│  Ask your question:                 │
│  ┌─────────────────────────────┐   │
│  │ What topics are covered?    │   │
│  └─────────────────────────────┘   │
│  [🔍 Search]                        │
└─────────────────────────────────────┘
```

---

## Upload Using Python

### Example 1: Upload Files From Anywhere

```python
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("my-documents")

# Upload from Desktop
rag.upload_file(
    "/Users/yourname/Desktop/research_paper.pdf",
    store
)

# Upload from Downloads
rag.upload_excel(
    "/Users/yourname/Downloads/data.xlsx",
    store
)

# Upload from Documents
rag.upload_file(
    "/Users/yourname/Documents/notes.txt",
    store
)

print("✓ All files uploaded!")
```

### Example 2: Upload Entire Folder

```python
from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("folder-upload")

# Point to YOUR folder
my_folder = Path("/Users/yourname/Desktop/ResearchPapers")

# Upload all PDFs
for pdf_file in my_folder.glob("*.pdf"):
    print(f"Uploading {pdf_file.name}...")
    rag.upload_file(pdf_file, store)

# Upload all Excel files
for excel_file in my_folder.glob("*.xlsx"):
    print(f"Uploading {excel_file.name}...")
    rag.upload_excel(excel_file, store)

print("✓ Folder uploaded!")
```

### Example 3: Upload From Project Folder

If you created `my_documents/` in the project:

```python
from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("project-docs")

# Upload from project folder
project_docs = Path("my_documents")

for file in project_docs.rglob("*"):
    if file.is_file():
        if file.suffix == '.xlsx':
            rag.upload_excel(file, store)
        elif file.suffix in ['.pdf', '.txt', '.md']:
            rag.upload_file(file, store)

print("✓ Project documents uploaded!")
```

---

## Where Files Are Stored

### Your Original Files

**Stay where they are!**

- Web UI: Reads from wherever you selected them
- Python: Reads from the path you specify
- Your files are **NOT moved or deleted**

### In the RAG System

Files are uploaded to **Google's servers**:

```
Your Computer                Google Cloud
─────────────                ─────────────
your_file.pdf  ──upload──>  [File Search Store]
                             ├── Embeddings
                             ├── Text chunks
                             └── Metadata
```

Once uploaded:
- Stored indefinitely (until you delete the store)
- Indexed and searchable
- Not deleted even if you delete local file

---

## Common Upload Scenarios

### Scenario 1: Files on Desktop

```python
# Mac/Linux
rag.upload_file("/Users/yourname/Desktop/paper.pdf", store)

# Windows
rag.upload_file("C:/Users/yourname/Desktop/paper.pdf", store)
```

### Scenario 2: Files in Google Drive

**First download to computer, then upload:**

1. Download from Google Drive to your computer
2. Note the download location (usually Downloads folder)
3. Upload to RAG system:

```python
rag.upload_file(
    "/Users/yourname/Downloads/from_google_drive.pdf",
    store
)
```

### Scenario 3: Multiple Files in Folders

```python
# If you have:
# Documents/
#   ├── Research/
#   │   ├── paper1.pdf
#   │   └── paper2.pdf
#   └── Data/
#       └── results.xlsx

from pathlib import Path

docs = Path("/Users/yourname/Documents")

# Upload all PDFs
for pdf in docs.rglob("*.pdf"):
    rag.upload_file(pdf, store)

# Upload all Excel files
for xlsx in docs.rglob("*.xlsx"):
    rag.upload_excel(xlsx, store)
```

### Scenario 4: Using Demo Files First

Test with included demo files:

```python
# Demo files are in: demo_data/
rag.upload_file("demo_data/lenr_overview_2024.txt", store)
rag.upload_file("demo_data/experimental_methods.txt", store)

# Generate and upload demo Excel files
# First run:
# python demo_data/create_sample_files.py

rag.upload_excel("demo_data/experimental_results.xlsx", store)
```

---

## What Gets Uploaded?

### Supported File Types

✅ **Will Upload:**
- PDF (`.pdf`)
- Excel (`.xlsx`, `.xls`)
- Text (`.txt`)
- Markdown (`.md`)
- Word (`.docx`)
- HTML (`.html`)

❌ **Won't Upload:**
- Images alone (`.jpg`, `.png`) - unless embedded in PDF
- Videos (`.mp4`, `.avi`)
- Audio (`.mp3`, `.wav`)
- Executables (`.exe`, `.app`)

### File Size Limit

- **Maximum:** 100 MB per file
- **Recommended:** Keep under 50 MB for best performance

If file is too large:
```bash
# Check file size
ls -lh yourfile.pdf

# If too large, split it or compress it
```

---

## Don't Copy Files to Project (Unless You Want To)

### ❌ NOT Required:

You do **NOT** need to:
- Copy files into the project folder
- Move files from their current location
- Organize files in a specific way

### ✅ Optional:

You **CAN** organize in project if you prefer:

```bash
# Create organized folders (optional)
mkdir -p my_documents/{research,data,notes}

# Copy your files there (optional)
cp ~/Desktop/*.pdf my_documents/research/
cp ~/Downloads/*.xlsx my_documents/data/
```

---

## Quick Reference

### Web UI Upload

```bash
# 1. Start app
streamlit run web_ui/app.py

# 2. In browser:
Sidebar → Create Store → Upload Documents → Browse → Select → Upload
```

### Python Upload

```python
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("my-store")

# Upload ANY file from ANYWHERE
rag.upload_file("/full/path/to/your/file.pdf", store)
```

### Verify Upload Worked

```python
# Query to test
response = rag.query("What documents do I have?", store)
print(response["answer"])
```

---

## Troubleshooting

### "File not found"

**Problem:** Wrong file path

**Solution:** Use full path:
```python
# ❌ Wrong - relative path might not work
rag.upload_file("file.pdf", store)

# ✅ Right - full absolute path
rag.upload_file("/Users/yourname/Desktop/file.pdf", store)

# ✅ Or use pathlib
from pathlib import Path
file_path = Path.home() / "Desktop" / "file.pdf"
rag.upload_file(file_path, store)
```

### "File too large"

**Problem:** File exceeds 100 MB

**Solution:**
```bash
# Check size
ls -lh yourfile.pdf

# If too large, split or compress
# Or upload in sections
```

### "Upload seems stuck"

**Problem:** Large file taking time

**Solution:**
- Wait (can take 30-60 seconds for large files)
- Check internet connection
- Try smaller file first to test

---

## Summary

### Where to Put Your Files

**Anywhere you want!** The system can read from any location.

### How to Upload

**Option 1 (Easiest):**
```bash
streamlit run web_ui/app.py
# Then use "Upload Documents" in sidebar
```

**Option 2 (Python):**
```python
rag.upload_file("/path/to/your/file.pdf", store)
```

### What Happens

Your file → Uploaded to Google → Indexed → Searchable with citations!

---

**Still confused? Try this:**

1. Use demo files first: `python demo_data/create_sample_files.py`
2. Upload demo files through web UI to practice
3. Then upload your own files the same way!

---

For more help:
- **Quick Start:** `QUICK_START.md`
- **How to Use:** `HOW_TO_USE.md`
- **Training Guide:** `TRAINING_GUIDE.md`
