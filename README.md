# LENR RAG System - Gemini Edition

**Best RAG solution for your 7000+ files**

Built with Google Gemini API. No 10GB limit. Lowest cost.

---

## ⚡ Quick Start (3 Minutes)

**Only 1 API key • $0.50-1/month • FREE embeddings**

```bash
# Step 1: Install dependencies (1 minute)
pip install -r requirements_gemini.txt

# Step 2: Set API key (1 minute)
echo "GOOGLE_API_KEY=your-key-here" > .env

# Step 3: Test system (1 minute)
python examples/test_gemini_smart_rag.py

# Step 4: Index your files
python index_gemini.py

# Step 5: Start web interface
streamlit run streamlit_gemini.py
```

**Get API key:** https://aistudio.google.com/apikey

**Full guide:** `START_GEMINI.md`

---

## 🎯 Key Advantages

### Solves Your Problems

✅ **No 10GB limit** - Local storage, unlimited space
✅ **Handles 7000+ files** - Index all files easily
✅ **Lowest cost** - $0.50-1/month, FREE embeddings
✅ **Excellent quality** - Gemini 2.0 Flash
✅ **Simple setup** - 3 minutes
✅ **Easy sharing** - Export/import database

### Why Choose Gemini

| Feature | Gemini Solution |
|---------|----------------|
| **API Keys** | 1 (Google only) |
| **Monthly Cost** | $0.50-1 |
| **Embeddings Cost** | **FREE** ✨ |
| **Per Query Cost** | $0.0005 |
| **Storage Limit** | Unlimited (local) |
| **Quality** | Excellent (Gemini 2.0) |
| **Setup Time** | 3 minutes |
| **Indexing Time** | 1-2 hours (7000 files) |
| **Long Context** | 2M tokens |

---

## 📦 Features

### Supported File Types
- PDF (`.pdf`)
- Text (`.txt`, `.md`)
- Word (`.docx`)
- Excel (`.xlsx`, `.xls`)

### Core Features
- ✅ Automatic duplicate detection (SHA256 hash-based)
- ✅ Progress tracking (tqdm progress bars)
- ✅ Batch upload (supports 7000+ files)
- ✅ Local vector database (ChromaDB)
- ✅ FREE embeddings (Gemini API)
- ✅ Excellent LLM (Gemini 2.0 Flash)
- ✅ Beautiful web interface (Streamlit)
- ✅ Database export/import (sharing)
- ✅ Cost tracking
- ✅ Multi-collection management

---

## 💰 Cost Breakdown

### Your 7000 Files

**One-time cost (indexing):**
```
Embeddings: FREE ✨
Total: $0
```

**Monthly cost (1000 queries):**
```
Storage: $0 (local disk)
Embeddings: FREE ✨
Gemini 2.0 Flash: 1000 × $0.0005 = $0.50

Total: $0.50-1/month
```

**Per query:**
```
Embedding: FREE ✨
Gemini generation: $0.0005

Total: ~$0.0005/query
```

---

## 🚀 Usage

### 1. Get API Key

Visit https://aistudio.google.com/apikey to create an API key.

### 2. Install and Configure

```bash
# Install dependencies
pip install -r requirements_gemini.txt

# Set API key
echo "GOOGLE_API_KEY=your-key-here" > .env
```

### 3. Test System

```bash
python examples/test_gemini_smart_rag.py
```

You'll see:
```
✅ Gemini Smart RAG initialized
✅ Created collection: test_docs
✅ 45 chunks indexed
📝 Answer: LENR stands for Low Energy Nuclear Reactions...
📚 Sources: 3
💰 Cost: FREE embeddings + $0.0005 per query
```

### 4. Index Your Files

```bash
# Put files in directory
mkdir -p my_local_files
cp your_files/* my_local_files/

# Run indexing script
python index_gemini.py
```

This will:
- Automatically find all supported files
- Show progress bar
- Skip duplicate files
- Save to local database
- Completely free (FREE embeddings)

### 5. Query Data

#### Option A: Web Interface (Recommended)

```bash
streamlit run streamlit_gemini.py
```

Then visit http://localhost:8501

#### Option B: Python Script

```python
from src.rag.gemini_smart_rag import GeminiSmartRAG

# Initialize
rag = GeminiSmartRAG()

# Query
result = rag.query("Your question", collection_name="my_docs")

# Display results
print(result['answer'])
print(f"Sources: {result['n_sources']}")
```

---

## 📤 Sharing Database

### Export Database

```bash
python database_manager.py export ./gemini_smart_rag_db my_database.tar.gz
```

### Share

Upload `my_database.tar.gz` to:
- Google Drive
- Dropbox
- Any cloud storage

### Import Database (Recipient)

```bash
# Install dependencies
pip install -r requirements_gemini.txt

# Import database
python database_manager.py import my_database.tar.gz ./gemini_smart_rag_db

# Start
streamlit run streamlit_gemini.py
```

---

## 🚀 Deployment

### Quick Deploy Options

**Docker (Recommended):**
```bash
docker-compose up -d
```

**VPS (Ubuntu/Debian):**
```bash
./deploy.sh
```

**Snowflake Streamlit:**
```bash
python deploy_snowflake.py
```

**Full deployment guide:** `DEPLOY.md`

---

## 🏗️ Architecture

```
User Question
    ↓
Gemini Embeddings (FREE)
    ↓ [768-dim vectors]
ChromaDB (local vector search)
    ↓ [Top 5 relevant chunks]
Gemini 2.0 Flash ($0.0005/query)
    ↓
Answer + Citations
```

---

## 📂 Project Structure

```
.
├── src/rag/
│   ├── gemini_smart_rag.py      # Gemini RAG implementation
│   ├── local_rag.py              # Local RAG (backup)
│   └── gemini_rag.py             # Original Gemini RAG
├── examples/
│   └── test_gemini_smart_rag.py # Test script
├── streamlit_gemini.py           # Web interface
├── index_gemini.py               # Indexing script
├── database_manager.py           # Database management
├── requirements_gemini.txt       # Dependencies
├── Dockerfile                    # Docker image
├── docker-compose.yml            # Docker Compose
├── deploy.sh                     # VPS deployment
└── START_GEMINI.md               # Full guide
```

---

## 🔧 FAQ

### Q: How long for 7000 files?

**A:** About 1-2 hours
- Depends on file size and CPU speed
- Progress bar shows progress
- Embeddings are FREE!

### Q: How big is the database?

**A:** About 30-40% of original files
- 7000 PDFs (7GB) → database ~2-3GB
- Compressed `.tar.gz` → ~1GB

### Q: Can I deploy to Snowflake?

**A:** Yes!
1. Upload `streamlit_gemini.py` and `src/` folder
2. Add `GOOGLE_API_KEY` secret
3. Deploy

### Q: Does it support Chinese?

**A:** Fully supported!
- Gemini supports Chinese queries
- Can index Chinese documents
- Interface can display Chinese

---

## 📚 Documentation

- **START_GEMINI.md** - Complete guide
- **DEPLOY.md** - Deployment guide
- **QUICK_DEPLOY.md** - Quick deployment
- **database_manager.py** - Database export/import
- **Google AI Studio** - https://aistudio.google.com/

---

## 🎉 Summary

Best solution for your needs:

✅ **Solves 10GB limit** - Unlimited local storage
✅ **Handles 7000+ files** - Easy indexing
✅ **Lowest cost** - $0.50-1/month, FREE embeddings
✅ **Excellent quality** - Gemini 2.0 Flash
✅ **Simple setup** - Only 3 minutes, 1 API key
✅ **Easy sharing** - Export/import database
✅ **Long context** - 2M tokens support

**Get started now:**

```bash
pip install -r requirements_gemini.txt
echo "GOOGLE_API_KEY=your-key" > .env
python examples/test_gemini_smart_rag.py
python index_gemini.py
streamlit run streamlit_gemini.py
```

💎 **Simple. Powerful. Cheapest. Use Gemini!**
