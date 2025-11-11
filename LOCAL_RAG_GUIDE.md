# 本地RAG系统使用指南
# Local RAG System Guide

完全本地化的RAG系统，无云存储限制，所有数据存在本地。
Fully local RAG system with no cloud limits, all data stored locally.

---

## 优势 / Advantages

### ✅ 相比Google Cloud方案的优势:

1. **无存储限制** - 只受本地硬盘限制，不是10GB
   - No storage limit - only limited by your hard drive, not 10GB

2. **完全本地** - 所有数据、embeddings、索引都在本地
   - Fully local - all data, embeddings, indexes stored locally

3. **隐私保护** - 数据不上传到Google Cloud
   - Privacy - data never uploaded to cloud

4. **更快** - 本地搜索比API调用快
   - Faster - local search faster than API calls

5. **离线工作** - 不需要网络连接（除了生成答案时）
   - Offline capable - no internet needed (except for answer generation)

6. **免费** - 不需要付费API调用存储
   - Free - no paid API calls for storage

---

## 架构 / Architecture

```
你的文件 (Your Files)
    ↓
本地文本提取 (Local Text Extraction)
    ↓
本地Embedding模型 (Local Embedding Model)
    ↓
ChromaDB本地向量数据库 (ChromaDB Local Vector Database)
    ↓
本地搜索 (Local Search)
    ↓
Gemini API生成答案 (Optional: Gemini API for Answer Generation)
```

**关键区别 / Key Difference:**
- Google方案: 文件上传到云端 → 云端embedding → 云端存储
- 本地方案: 文件在本地 → 本地embedding → 本地存储

---

## 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements_local.txt
```

这会安装:
- `chromadb` - 本地向量数据库
- `sentence-transformers` - 本地embedding模型
- `torch` - PyTorch后端
- 其他依赖

### 2. 基本使用 / Basic Usage

```python
from src.rag.local_rag import LocalRAG

# 初始化（不需要API key也可以用）
rag = LocalRAG(
    api_key="your_api_key",  # 可选，只用于生成答案
    persist_directory="./my_rag_db"  # 本地数据库路径
)

# 创建collection
rag.create_collection("my_docs")

# 上传文件
rag.upload_file(
    "document.pdf",
    collection_name="my_docs",
    metadata={"category": "research"}
)

# 查询
result = rag.query(
    "What is LENR?",
    collection_name="my_docs"
)

print(result['answer'])
print(f"Found {result['n_sources']} sources")
```

### 3. 批量上传 / Batch Upload

```python
from pathlib import Path

# 上传整个文件夹
folder = Path("my_documents")
for file in folder.rglob("*.pdf"):
    print(f"Uploading {file.name}...")
    rag.upload_file(file, "my_docs")
```

---

## Web界面 / Web UI

运行本地RAG的Streamlit界面:

```bash
streamlit run web_ui/app_local.py
```

功能:
- ✅ 创建collections
- ✅ 上传文件（PDF, Excel, TXT, DOCX等）
- ✅ 查询和搜索
- ✅ 查看sources
- ✅ 查看数据库统计

---

## 自动索引 / Auto-Indexing

使用本地auto-indexer:

```bash
# 初始化
python auto_index_local.py init

# 同步
python auto_index_local.py sync

# 监控模式
python auto_index_local.py watch 60
```

---

## Snowflake部署 / Snowflake Deployment

### 准备部署文件

1. **创建`streamlit_app.py`** (Snowflake入口文件)

```python
# streamlit_app.py
import streamlit as st
from src.rag.local_rag import LocalRAG

st.set_page_config(page_title="本地RAG系统", page_icon="🔬")

# 初始化
@st.cache_resource
def init_rag():
    return LocalRAG(
        persist_directory="/tmp/chroma_db"  # Snowflake临时目录
    )

rag = init_rag()

# UI代码...
```

2. **创建`environment.yml`**

```yaml
name: local_rag
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - pip:
      - streamlit>=1.29.0
      - chromadb>=0.4.24
      - sentence-transformers>=2.3.0
      - torch>=2.1.0
      - pymupdf>=1.23.0
      - pandas>=2.0.0
      - openpyxl>=3.1.0
```

3. **上传到Snowflake**

```bash
# 在Snowflake Streamlit中:
# 1. 创建新的Streamlit App
# 2. 上传streamlit_app.py
# 3. 上传src/文件夹
# 4. 上传environment.yml
# 5. 部署
```

### Snowflake限制

⚠️ **注意事项:**

1. **临时存储** - Snowflake的文件系统是临时的
   - 每次重启app，数据库会丢失
   - 需要实现持久化方案（见下文）

2. **内存限制** - 根据Snowflake plan有限制
   - 选择合适的embedding模型大小

3. **CPU限制** - Embedding生成可能较慢
   - 考虑预先生成embeddings

### 持久化方案 / Persistence Solutions

#### 方案1: Snowflake Stage存储

```python
import snowflake.connector

def save_to_stage(local_db_path):
    """保存数据库到Snowflake Stage"""
    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()
    cursor.execute(f"PUT file://{local_db_path}/* @my_stage/chroma_db/")

def load_from_stage(local_db_path):
    """从Snowflake Stage加载"""
    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()
    cursor.execute(f"GET @my_stage/chroma_db/* file://{local_db_path}/")
```

#### 方案2: Snowflake Table存储

```python
def save_embeddings_to_table(collection_data):
    """保存到Snowflake表"""
    # 将vectors保存到Snowflake Vector列
    conn = snowflake.connector.connect(...)
    # INSERT INTO embeddings_table ...

def load_embeddings_from_table():
    """从表加载"""
    # SELECT * FROM embeddings_table
```

#### 方案3: 外部存储

```python
# 使用S3/Azure Blob等
import boto3

def save_to_s3(local_db_path, bucket, key):
    s3 = boto3.client('s3')
    # Upload chroma_db to S3

def load_from_s3(local_db_path, bucket, key):
    # Download from S3
```

---

## 对比 / Comparison

| 特性 | Google Cloud RAG | 本地RAG Local RAG |
|------|-----------------|-------------------|
| 存储限制 | 10GB | 无限制（硬盘大小）|
| 数据位置 | Google Cloud | 本地机器 |
| 隐私 | 数据上传云端 | 数据保持本地 |
| 速度 | API调用延迟 | 本地搜索快 |
| 成本 | API调用费用 | 免费（本地计算）|
| 网络需求 | 需要网络 | 仅生成答案需要 |
| Snowflake部署 | 简单 | 需要持久化方案 |
| 适合场景 | 小数据集，云端协作 | 大数据集，本地处理 |

---

## 性能优化 / Performance Optimization

### 1. 选择更小的Embedding模型

```python
# 默认: all-MiniLM-L6-v2 (80MB, 快速)
rag = LocalRAG(embedding_model="all-MiniLM-L6-v2")

# 更小: paraphrase-MiniLM-L3-v2 (60MB, 更快)
rag = LocalRAG(embedding_model="paraphrase-MiniLM-L3-v2")

# 更好: all-mpnet-base-v2 (400MB, 更准确)
rag = LocalRAG(embedding_model="all-mpnet-base-v2")
```

### 2. 调整Chunk大小

```python
# 更小的chunks = 更精确，但更多存储
rag.upload_file("doc.pdf", "my_docs", chunk_size=500, chunk_overlap=100)

# 更大的chunks = 更多上下文，但可能不精确
rag.upload_file("doc.pdf", "my_docs", chunk_size=2000, chunk_overlap=400)
```

### 3. 批量处理

```python
# 批量上传避免重复加载模型
files = list(Path("docs").glob("*.pdf"))
for f in files:
    rag.upload_file(f, "my_docs")
```

---

## 常见问题 / FAQ

### Q: 需要GPU吗？
A: 不需要，但有GPU会更快。CPU也完全可以用。

### Q: 支持中文吗？
A: 支持！使用multilingual模型:
```python
rag = LocalRAG(embedding_model="paraphrase-multilingual-MiniLM-L12-v2")
```

### Q: 数据库文件在哪里？
A: 在`persist_directory`指定的目录，默认`./chroma_db/`

### Q: 如何备份数据？
A: 直接复制`chroma_db/`文件夹:
```bash
cp -r chroma_db/ backup_chroma_db/
```

### Q: 可以不用Gemini API吗？
A: 可以！不传API key即可:
```python
rag = LocalRAG(api_key=None)
result = rag.query("question", "my_docs", use_gemini=False)
```

### Q: Snowflake上数据会丢失吗？
A: 是的，需要实现持久化方案（见上文）

---

## 下一步 / Next Steps

1. **测试本地RAG:**
   ```bash
   python examples/test_local_rag.py
   ```

2. **运行Web UI:**
   ```bash
   streamlit run web_ui/app_local.py
   ```

3. **准备Snowflake部署:**
   - 阅读Snowflake部署章节
   - 选择持久化方案
   - 测试部署

---

## 支持 / Support

- **文档:** 查看其他.md文件
- **示例:** 查看examples/文件夹
- **问题:** 查看troubleshooting章节

---

**选择建议 / Recommendation:**

- **数据 < 10GB, 需要云端协作** → 使用Google Cloud RAG
- **数据 > 10GB, 本地处理** → 使用Local RAG
- **部署到Snowflake** → 使用Local RAG + 持久化方案
