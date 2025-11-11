# Quick Start - Local RAG System

Complete solution for your requirements. Ready to use in 3 commands!

---

## ✅ What You Get

1. **No 10GB Limit** - Store unlimited data locally
2. **Local Indexing** - All embeddings generated on your machine
3. **Uses Gemini** - Only for answering questions, not storage
4. **English Interface** - All-English UI as requested
5. **Snowflake Ready** - Can deploy to Snowflake Streamlit

---

## 🚀 3-Step Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements_local.txt
```

This installs:
- ChromaDB (local vector database)
- sentence-transformers (local embeddings)
- PyPDF2, python-docx (document processing)
- torch (machine learning backend)
- streamlit (web UI)
- google-genai (optional, for answer generation)

### Step 2: Test It Works

```bash
python examples/test_local_rag.py
```

Expected output:
```
============================================================
Local RAG Test
============================================================

1. Initializing LocalRAG...
✅ Local RAG initialized

2. Creating collection...
✅ Created collection: test_docs

3. Uploading demo files...
   Uploading: lenr_overview_2024.txt
   ✅ 45 chunks indexed

4. Database statistics:
   Collections: 1
   Total documents: 83
   Database size: 0.52 MB

5. Testing queries...
   Q: What is LENR?
   A: LENR stands for Low Energy Nuclear Reactions...
   Sources: 3

✅ Test complete!
```

### Step 3: Run Web UI

```bash
python -m streamlit run streamlit_app.py
```

Open browser: `http://localhost:8501`

---

## 📚 How to Use

### Option A: Web Interface (Easy)

1. **Start app:**
   ```bash
   python -m streamlit run streamlit_app.py
   ```

2. **Create collection** (sidebar)
3. **Upload files** (📤 Upload tab)
4. **Ask questions** (💬 Query tab)

### Option B: Python Script (Advanced)

```python
from src.rag.local_rag import LocalRAG

# Initialize
rag = LocalRAG(persist_directory="./my_rag_db")

# Create collection
rag.create_collection("my_docs")

# Upload file
rag.upload_file("document.pdf", "my_docs")

# Query
result = rag.query("What is the main topic?", "my_docs")
print(result['answer'])
```

---

## 🎯 Key Differences from Google Cloud

| Feature | Google Cloud RAG | Local RAG |
|---------|------------------|-----------|
| Storage Limit | 10GB | Unlimited |
| Data Location | Google Cloud | Your computer |
| Indexing | Cloud API | Local (free) |
| Query | Cloud API | Local search |
| Privacy | Data uploaded | Data stays local |
| Internet | Required | Optional* |
| Cost | API fees | Free |

\* Internet only needed for Gemini answer generation (optional)

---

## 📂 Your Files Stay Local

All data stored in `./chroma_db/` (or your specified directory):

```
chroma_db/
├── chroma.sqlite3    # Vector database
├── embeddings/       # Your embeddings
└── metadata/         # File metadata
```

No data uploaded to cloud!

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'chromadb'"

```bash
pip install -r requirements_local.txt
```

### Issue: Model download slow

First run downloads embedding model (~80MB). Be patient or use mirror:

```bash
export HF_ENDPOINT=https://hf-mirror.com
python examples/test_local_rag.py
```

### Issue: Out of memory

Use smaller model:

```python
rag = LocalRAG(embedding_model="paraphrase-MiniLM-L3-v2")
```

### Complete troubleshooting

See `SETUP_LOCAL_RAG.md` for detailed solutions.

---

## 🚢 Deploy to Snowflake

### 1. Prepare Files

- `streamlit_app.py` (already created, Snowflake-ready)
- `src/` folder
- `requirements_local.txt`

### 2. Create environment.yml

```yaml
name: local_rag
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - pip:
      - streamlit>=1.29.0
      - chromadb>=0.4.24
      - sentence-transformers>=2.3.0
      - torch>=2.1.0
      - PyPDF2>=3.0.0
      - python-docx>=1.1.0
      - pandas>=2.0.0
```

### 3. Upload to Snowflake

1. Go to https://app.snowflake.com/
2. Navigate to Streamlit Apps
3. Create new app
4. Upload `streamlit_app.py` as main file
5. Upload `src/` folder
6. Upload `environment.yml`
7. Deploy!

### 4. Add API Key (Optional)

In Snowflake Streamlit settings:
- Add secret: `GOOGLE_API_KEY`
- Value: Your Gemini API key

See `LOCAL_RAG_GUIDE.md` for persistence solutions.

---

## 📊 Performance Tips

### 1. Faster Embedding

```python
# Smaller model = faster indexing
rag = LocalRAG(embedding_model="paraphrase-MiniLM-L3-v2")
```

### 2. Adjust Chunk Size

```python
# Larger chunks = fewer embeddings = faster
rag.upload_file("doc.pdf", "docs", chunk_size=2000)
```

### 3. Batch Upload

```python
# Upload multiple files at once
from pathlib import Path
for f in Path("docs").glob("*.pdf"):
    rag.upload_file(f, "my_docs")
```

---

## 📖 Documentation

- **SETUP_LOCAL_RAG.md** - Detailed setup and troubleshooting
- **LOCAL_RAG_GUIDE.md** - Complete user guide
- **examples/test_local_rag.py** - Test script with examples

---

## ✨ Next Steps

### 1. Add Your Data

```bash
# Copy your files
cp ~/Desktop/*.pdf my_local_files/
cp ~/Documents/*.xlsx my_local_files/

# Index them
python examples/test_local_rag.py
```

### 2. Query Your Data

```bash
python -m streamlit run streamlit_app.py
```

### 3. Deploy to Snowflake

Follow deployment steps above.

---

## 💡 Example Use Cases

### Research Papers

```python
rag = LocalRAG()
rag.create_collection("research")

# Upload all PDFs
for pdf in Path("papers").glob("*.pdf"):
    rag.upload_file(pdf, "research")

# Query
result = rag.query("What are the key findings?", "research")
```

### Excel Data Analysis

```python
# Upload Excel files
for xlsx in Path("data").glob("*.xlsx"):
    rag.upload_file(xlsx, "research")

# Ask about data
result = rag.query("What is the average temperature?", "research")
```

### Documentation Search

```python
# Upload all docs
for doc in Path("docs").glob("*"):
    rag.upload_file(doc, "docs")

# Search
result = rag.query("How to configure X?", "docs")
```

---

## 🎉 You're Ready!

Everything is set up. Just run:

```bash
pip install -r requirements_local.txt
python -m streamlit run streamlit_app.py
```

Enjoy your unlimited local RAG system! 🚀
