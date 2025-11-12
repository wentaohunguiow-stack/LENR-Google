# LENR RAG System

**Best RAG solution for your 7000+ files**

---

## ⚡ Quick Start - Smart RAG (Recommended)

**Only 1 API key • $3-5/month • 3 minutes setup**

```bash
# Step 1: Install
pip install -r requirements_smart.txt

# Step 2: Set API key
echo "OPENAI_API_KEY=your-key" > .env

# Step 3: Test
python examples/test_smart_rag.py

# Step 4: Index files
python index_smart.py

# Step 5: Start UI
streamlit run streamlit_smart.py
```

**Get API key:** https://platform.openai.com/api-keys

**Read full guide:** `START_HERE.md`

---

## Why Smart RAG?

| Feature | Smart RAG |
|---------|-----------|
| **Simplicity** | ✅ Only 1 API key needed |
| **Cost** | ✅ $3-5/month (10x cheaper than enterprise) |
| **Quality** | ✅ GPT-4 Turbo (excellent) |
| **Storage** | ✅ Unlimited (local disk) |
| **Setup** | ✅ 3 minutes |
| **Files** | ✅ Handles 7000+ files easily |
| **Sharing** | ✅ Export/import database |

---

## Comparison

### Smart RAG (Recommended)
- **Cost:** $3-5/month
- **API Keys:** 1 (OpenAI only)
- **Setup:** 3 minutes
- **Quality:** Excellent (GPT-4)
- **Best for:** Most users ✅

### Enterprise RAG
- **Cost:** $15/month
- **API Keys:** 4 (OpenAI, Pinecone, Cohere, Anthropic)
- **Setup:** 30 minutes
- **Quality:** Excellent (Claude 3.5)
- **Best for:** Large teams, need Claude

### Local RAG
- **Cost:** $0-1/month
- **API Keys:** 0-1 (optional Gemini)
- **Setup:** 10 minutes
- **Quality:** Good
- **Best for:** Privacy-focused users

---

## What You Get

### For Your 7000 Files:
- ✅ **No 10GB limit** - Store unlimited files locally
- ✅ **Best quality** - GPT-4 Turbo answers
- ✅ **Low cost** - Only $3-5/month
- ✅ **Simple** - Just 1 API key
- ✅ **Fast** - Local storage, fast search
- ✅ **Shareable** - Export/import database files
- ✅ **Snowflake ready** - Deploy in minutes

### Features:
- Duplicate detection (automatic)
- Progress tracking
- Multiple file types (PDF, TXT, DOCX, XLSX)
- Beautiful web interface
- Cost tracking
- Export/import for sharing

---

## Documentation

- **START_HERE.md** - Complete setup guide for Smart RAG
- **ENTERPRISE_GUIDE.md** - Enterprise RAG (if you need 4-service setup)
- **LOCAL_RAG_GUIDE.md** - Local RAG (if you need 100% free)
- **COMPARE_ALL_SOLUTIONS.md** - Detailed comparison

---

## Quick Command Reference

```bash
# Smart RAG (Recommended)
pip install -r requirements_smart.txt
python examples/test_smart_rag.py
python index_smart.py
streamlit run streamlit_smart.py

# Enterprise RAG
pip install -r requirements_enterprise.txt
python examples/test_enterprise_rag.py
streamlit run streamlit_enterprise.py

# Local RAG
pip install -r requirements_local.txt
python examples/test_local_rag.py
streamlit run streamlit_app.py
```

---

## Cost Breakdown

### Smart RAG (Recommended):
- **One-time:** ~$0.70 (indexing 7000 files)
- **Monthly:** ~$3-5 (1000 queries)
- **Per query:** ~$0.003

### Enterprise RAG:
- **One-time:** ~$5-10
- **Monthly:** ~$15
- **Per query:** ~$0.01

### Local RAG:
- **One-time:** $0
- **Monthly:** $0-1
- **Per query:** ~$0.001 (if using Gemini)

---

## Features Comparison

| Feature | Smart RAG | Enterprise RAG | Local RAG |
|---------|-----------|----------------|-----------|
| **Storage Limit** | Unlimited | Unlimited | Unlimited |
| **API Keys** | 1 | 4 | 0-1 |
| **Setup Time** | 3 min | 30 min | 10 min |
| **Cost/Month** | $3-5 | $15 | $0-1 |
| **Quality** | Excellent | Excellent | Good |
| **LLM** | GPT-4 | Claude 3.5 | Gemini |
| **Embeddings** | OpenAI 1536d | OpenAI 3072d | Local 384d |
| **Sharing** | Export file | Share keys | Export file |
| **Best For** | Most users | Large teams | Privacy |

---

## Support

### API Keys:
- **OpenAI:** https://platform.openai.com/api-keys
- **Pinecone:** https://www.pinecone.io/
- **Cohere:** https://cohere.com/
- **Anthropic:** https://console.anthropic.com/

### Documentation:
- OpenAI: https://platform.openai.com/docs
- Pinecone: https://docs.pinecone.io/
- Cohere: https://docs.cohere.com/
- Anthropic: https://docs.anthropic.com/

---

## Project Structure

```
.
├── src/rag/
│   ├── smart_rag.py           # Smart RAG (recommended)
│   ├── enterprise_rag.py      # Enterprise RAG
│   ├── local_rag.py           # Local RAG
│   └── gemini_rag.py          # Original Gemini RAG
├── examples/
│   ├── test_smart_rag.py      # Test Smart RAG
│   ├── test_enterprise_rag.py # Test Enterprise RAG
│   └── test_local_rag.py      # Test Local RAG
├── streamlit_smart.py         # Smart RAG UI
├── streamlit_enterprise.py    # Enterprise RAG UI
├── streamlit_app.py           # Local RAG UI
├── index_smart.py             # Index files (Smart RAG)
├── index_my_files.py          # Index files (Enterprise RAG)
├── database_manager.py        # Export/import databases
├── requirements_smart.txt     # Smart RAG deps
├── requirements_enterprise.txt # Enterprise RAG deps
├── requirements_local.txt     # Local RAG deps
└── START_HERE.md              # Main guide
```

---

## Next Steps

### Recommended: Smart RAG

```bash
# Read this first
cat START_HERE.md

# Quick setup
pip install -r requirements_smart.txt
echo "OPENAI_API_KEY=your-key" > .env
python examples/test_smart_rag.py
```

### For Enterprise Teams:

```bash
cat ENTERPRISE_GUIDE.md
pip install -r requirements_enterprise.txt
./setup_enterprise.sh
```

### For Privacy-Focused:

```bash
cat LOCAL_RAG_GUIDE.md
pip install -r requirements_local.txt
python examples/test_local_rag.py
```

---

## Summary

**Smart RAG is the best choice for your 7000+ files:**

✅ Solves the 10GB Google Cloud limit
✅ Only 1 API key (super simple)
✅ $3-5/month (very affordable)
✅ GPT-4 quality (excellent answers)
✅ 3-minute setup (fastest)
✅ Unlimited storage (local disk)
✅ Easy sharing (export/import)

**Get started now:**

```bash
pip install -r requirements_smart.txt
python examples/test_smart_rag.py
```

🚀 **Simple. Powerful. Affordable.**
