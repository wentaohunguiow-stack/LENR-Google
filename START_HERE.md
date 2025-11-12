# Start Here - Smart RAG System

**The Best RAG Solution - Simple, Powerful, Affordable**

Only **1 API key** needed. Handles **7000+ files**. Costs **$3-5/month**.

---

## Why This is Better

| Feature | Smart RAG | Enterprise RAG |
|---------|-----------|----------------|
| **API Keys** | 1 (OpenAI only) | 4 (OpenAI, Pinecone, Cohere, Anthropic) |
| **Setup Time** | 3 minutes | 30 minutes |
| **Cost/Month** | $3-5 | $15 |
| **Storage** | Unlimited (local) | Unlimited (cloud) |
| **Quality** | Excellent (GPT-4) | Excellent (Claude 3.5) |
| **Sharing** | Export file | Share keys |
| **Complexity** | Very simple | Complex |

**Smart RAG = Best balance of everything**

---

## 3-Step Setup (3 Minutes)

### Step 1: Get OpenAI API Key (1 minute)

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-...`)

**Cost**: ~$3-5/month for 1000 queries

### Step 2: Install (1 minute)

```bash
pip install -r requirements_smart.txt
```

### Step 3: Set API Key (1 minute)

```bash
# Create .env file
echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
```

**Done! That's it!**

---

## Test It Works

```bash
python examples/test_smart_rag.py
```

Expected output:
```
============================================================
Smart RAG System Test
============================================================

1. Initializing Smart RAG...
   ✅ Smart RAG initialized
   Model: gpt-4-turbo-preview
   Embeddings: text-embedding-3-small

2. Creating collection...
   ✅ Created collection: test_docs

3. Uploading demo files...
   ✅ 45 chunks indexed

4. Database statistics:
   Collections: 1
   Total documents: 45
   Database size: 0.23 MB

5. Testing query...
   Q: What is LENR?

   📝 Answer:
   LENR stands for Low Energy Nuclear Reactions...

   📚 Sources: 3

✅ Smart RAG Test Complete!
```

---

## Index Your 7000 Files

### Quick Way:

```bash
python index_smart.py
```

This script will:
1. Find all your files in `my_local_files/`
2. Index them automatically (1-2 hours for 7000 files)
3. Show progress bar
4. Skip duplicates automatically

### Custom Script:

```python
from src.rag.smart_rag import SmartRAG
from pathlib import Path

# Initialize
rag = SmartRAG()
rag.create_collection("my_docs")

# Index all files
files = list(Path("my_local_files").rglob("*"))
stats = rag.batch_upload(files, "my_docs", show_progress=True)

print(f"Indexed {stats['successful']} files!")
```

---

## Query Your Data

### Web Interface (Easy):

```bash
streamlit run streamlit_smart.py
```

Open http://localhost:8501

### Python Script:

```python
from src.rag.smart_rag import SmartRAG

rag = SmartRAG()
result = rag.query("Your question", collection_name="my_docs")
print(result['answer'])
```

---

## Share Your Database

### Export:

```bash
python database_manager.py export ./smart_rag_db my_database.tar.gz
```

### Share:
- Upload `my_database.tar.gz` to Google Drive, Dropbox, etc.
- Share link with your team

### Import (Team Member):

```bash
pip install -r requirements_smart.txt
python database_manager.py import my_database.tar.gz ./smart_rag_db
streamlit run streamlit_smart.py
```

---

## Deploy to Snowflake

1. **Upload files to Snowflake Streamlit:**
   - `streamlit_smart.py`
   - `src/` folder
   - `requirements_smart.txt`

2. **Add secret in Snowflake:**
   ```toml
   OPENAI_API_KEY = "sk-proj-..."
   ```

3. **Deploy!**

---

## Cost Breakdown

### One-Time (7000 files):
```
Indexing embeddings:
  7000 files × 5000 tokens × $0.02/1M tokens = $0.70

Total: Less than $1
```

### Monthly (1000 queries):
```
Storage: $0 (local disk)
Query embeddings: 1000 × $0.00002 = $0.02
GPT-4 answers: 1000 × $0.003 = $3.00

Total: ~$3-5/month
```

### Per Query:
```
Embedding: $0.00002
GPT-4: $0.003

Total: ~$0.003 per query
```

**10x cheaper than enterprise RAG, same quality!**

---

## Features

✅ **Only 1 API key** - OpenAI only, super simple
✅ **Unlimited files** - No 10GB limit, store locally
✅ **High quality** - GPT-4 Turbo, 1536-dim embeddings
✅ **Very low cost** - $3-5/month vs $15/month
✅ **Easy setup** - 3 minutes vs 30 minutes
✅ **Easy sharing** - Export/import database files
✅ **Fast indexing** - Local processing with progress bar
✅ **Duplicate detection** - Automatic, hash-based
✅ **Snowflake ready** - Deploy in minutes

---

## Comparison

### Smart RAG (Recommended):
- **Cost**: $3-5/month
- **Setup**: 3 minutes
- **API keys**: 1
- **Quality**: Excellent
- **Best for**: Most users

### Enterprise RAG:
- **Cost**: $15/month
- **Setup**: 30 minutes
- **API keys**: 4
- **Quality**: Excellent
- **Best for**: Large teams needing Claude 3.5

### Local RAG:
- **Cost**: $0-1/month
- **Setup**: 10 minutes
- **API keys**: 0-1
- **Quality**: Good
- **Best for**: Privacy-focused users

---

## Quick Command Reference

```bash
# Setup
pip install -r requirements_smart.txt
echo "OPENAI_API_KEY=your-key" > .env

# Test
python examples/test_smart_rag.py

# Index files
python index_smart.py

# Start web UI
streamlit run streamlit_smart.py

# Export database
python database_manager.py export ./smart_rag_db backup.tar.gz

# Import database
python database_manager.py import backup.tar.gz ./smart_rag_db
```

---

## Troubleshooting

### "No module named 'openai'"
```bash
pip install -r requirements_smart.txt
```

### "OpenAI API key not found"
```bash
echo "OPENAI_API_KEY=your-key" > .env
```

### "Collection not found"
```python
from src.rag.smart_rag import SmartRAG
rag = SmartRAG()
rag.create_collection("my_docs")
```

---

## Support

- **Full Guide**: `SMART_RAG_GUIDE.md`
- **OpenAI Docs**: https://platform.openai.com/docs
- **API Keys**: https://platform.openai.com/api-keys

---

## Summary

**You get:**
- 🎯 Simplest setup (3 minutes, 1 API key)
- 💰 Lowest cost ($3-5/month)
- 🚀 Excellent quality (GPT-4 Turbo)
- 📦 Easy sharing (export/import)
- ⚡ Fast performance (local processing)
- 🔧 Easy maintenance (single dependency)

**This is the best solution for your 7000+ files.**

---

## Ready?

```bash
# 1. Get API key from: https://platform.openai.com/api-keys
# 2. Run:
pip install -r requirements_smart.txt
echo "OPENAI_API_KEY=your-key-here" > .env
python examples/test_smart_rag.py

# 3. Index your files:
python index_smart.py

# 4. Start using:
streamlit run streamlit_smart.py
```

🚀 **Simple. Powerful. Affordable.**
