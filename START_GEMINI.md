# Start Here - Gemini Smart RAG

**Best Gemini Solution - Simple, Powerful, Cheapest**

Only **1 Google API key** needed. Handles **7000+ files**. Costs **$0.50-1/month**.

---

## Why Choose Gemini Smart RAG?

| Feature | Gemini Smart RAG | OpenAI Smart RAG |
|---------|------------------|------------------|
| **API Keys** | 1 (Google only) | 1 (OpenAI only) |
| **Setup Time** | 3 minutes | 3 minutes |
| **Monthly Cost** | $0.50-1 | $3-5 |
| **Embeddings** | **FREE** ✨ | Paid |
| **Quality** | Excellent (Gemini 2.0) | Excellent (GPT-4) |
| **Storage** | Unlimited (local) | Unlimited (local) |

**Gemini Smart RAG = Cheapest option!**

---

## 3-Step Setup (3 Minutes)

### Step 1: Get Google API Key (1 minute)

1. Visit https://aistudio.google.com/apikey
2. Click "Create API key"
3. Copy the key

**Cost**: ~$0.50-1/month (1000 queries)

### Step 2: Install (1 minute)

```bash
pip install -r requirements_gemini.txt
```

### Step 3: Set API Key (1 minute)

```bash
# Create .env file
echo "GOOGLE_API_KEY=your-key-here" > .env
```

**Done! That's it!**

---

## Test It Works

```bash
python examples/test_gemini_smart_rag.py
```

Expected output:
```
============================================================
Gemini Smart RAG System Test
============================================================

1. Initializing Gemini Smart RAG...
   ✅ Gemini Smart RAG initialized
   Model: gemini-2.0-flash-exp
   Embeddings: models/text-embedding-004

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

6. Cost estimate:
   Embeddings: FREE (Gemini API)
   Per query: ~$0.0005
   1000 queries: ~$0.50/month

✅ Gemini Smart RAG Test Complete!
```

---

## Index Your 7000 Files

### Quick Way:

```bash
python index_gemini.py
```

This script will:
1. Find all files in `my_local_files/`
2. Index them automatically (1-2 hours for 7000 files)
3. Show progress bar
4. Skip duplicates automatically

### Custom Script:

```python
from src.rag.gemini_smart_rag import GeminiSmartRAG
from pathlib import Path

# Initialize
rag = GeminiSmartRAG()
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
streamlit run streamlit_gemini.py
```

Open http://localhost:8501

### Python Script:

```python
from src.rag.gemini_smart_rag import GeminiSmartRAG

rag = GeminiSmartRAG()
result = rag.query("Your question", collection_name="my_docs")
print(result['answer'])
```

---

## Share Your Database

### Export:

```bash
python database_manager.py export ./gemini_smart_rag_db my_database.tar.gz
```

### Share:
- Upload `my_database.tar.gz` to Google Drive, Dropbox, etc.
- Share link with your team

### Import (Team Member):

```bash
pip install -r requirements_gemini.txt
python database_manager.py import my_database.tar.gz ./gemini_smart_rag_db
streamlit run streamlit_gemini.py
```

---

## Deploy to Snowflake

1. **Upload files to Snowflake Streamlit:**
   - `streamlit_gemini.py`
   - `src/` folder
   - `requirements_gemini.txt`

2. **Add secret in Snowflake:**
   ```toml
   GOOGLE_API_KEY = "your-key-here"
   ```

3. **Deploy!**

---

## Cost Breakdown

### One-Time (7000 files):
```
Indexing embeddings: FREE ✨

Total: $0 (FREE!)
```

### Monthly (1000 queries):
```
Storage: $0 (local disk)
Query embeddings: FREE ✨
Gemini 2.0 Flash answers: 1000 × $0.0005 = $0.50

Total: ~$0.50-1/month
```

### Per Query:
```
Embedding: FREE ✨
Gemini: $0.0005

Total: ~$0.0005 per query
```

**10x cheaper than OpenAI, 30x cheaper than Enterprise RAG!**

---

## Features

✅ **Only 1 API key** - Google only, super simple
✅ **Unlimited files** - No 10GB limit, store locally
✅ **Cheapest** - FREE embeddings + lowest query cost
✅ **Excellent quality** - Gemini 2.0 Flash
✅ **Simple setup** - 3 minutes
✅ **Easy sharing** - Export/import database files
✅ **Fast indexing** - Local processing with progress bar
✅ **Duplicate detection** - Automatic, hash-based
✅ **Snowflake ready** - Deploy in minutes
✅ **Long context** - 2M tokens (very long documents)

---

## Comparison

### Gemini Smart RAG (Recommended):
- **Cost**: $0.50-1/month (cheapest!)
- **Setup**: 3 minutes
- **API keys**: 1
- **Quality**: Excellent
- **Embeddings**: FREE ✨
- **Best for**: Most users

### OpenAI Smart RAG:
- **Cost**: $3-5/month
- **Setup**: 3 minutes
- **API keys**: 1
- **Quality**: Excellent
- **Embeddings**: Paid
- **Best for**: Users who prefer GPT-4

### Enterprise RAG:
- **Cost**: $15/month
- **Setup**: 30 minutes
- **API keys**: 4
- **Quality**: Excellent
- **Best for**: Large teams, need Claude

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
pip install -r requirements_gemini.txt
echo "GOOGLE_API_KEY=your-key" > .env

# Test
python examples/test_gemini_smart_rag.py

# Index files
python index_gemini.py

# Start web UI
streamlit run streamlit_gemini.py

# Export database
python database_manager.py export ./gemini_smart_rag_db backup.tar.gz

# Import database
python database_manager.py import backup.tar.gz ./gemini_smart_rag_db
```

---

## Deployment

### Docker:
```bash
docker-compose up -d
```

### VPS:
```bash
./deploy.sh
```

### Snowflake:
```bash
python deploy_snowflake.py
```

**Full deployment guide:** `DEPLOY.md`

---

## Troubleshooting

### "No module named 'google.genai'"
```bash
pip install -r requirements_gemini.txt
```

### "Google API key not found"
```bash
echo "GOOGLE_API_KEY=your-key" > .env
```

### "Collection not found"
```python
from src.rag.gemini_smart_rag import GeminiSmartRAG
rag = GeminiSmartRAG()
rag.create_collection("my_docs")
```

---

## Support

- **Google AI Studio**: https://aistudio.google.com/
- **API Keys**: https://aistudio.google.com/apikey
- **Documentation**: https://ai.google.dev/

---

## Summary

**You get:**
- 🎯 Simplest setup (3 minutes, 1 API key)
- 💰 Lowest cost ($0.50-1/month, FREE embeddings)
- 🚀 Excellent quality (Gemini 2.0 Flash)
- 📦 Easy sharing (export/import)
- ⚡ Fast performance (local processing)
- 🔧 Easy maintenance (single dependency)

**This is the cheapest solution for your 7000+ files.**

---

## Ready?

```bash
# 1. Get API key from: https://aistudio.google.com/apikey
# 2. Run:
pip install -r requirements_gemini.txt
echo "GOOGLE_API_KEY=your-key-here" > .env
python examples/test_gemini_smart_rag.py

# 3. Index your files:
python index_gemini.py

# 4. Start using:
streamlit run streamlit_gemini.py
```

💎 **Simple. Powerful. Cheapest.**
