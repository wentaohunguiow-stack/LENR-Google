# 本地RAG完整安装指南
# Complete Local RAG Setup Guide

一步步解决所有问题 / Step-by-step solution for all issues

---

## 问题诊断 / Problem Diagnosis

常见问题:
1. ❌ 依赖包缺失
2. ❌ Google Cloud有10GB限制
3. ❌ Indexing失败
4. ❌ Import错误

## 完整解决方案 / Complete Solution

### Step 1: 安装本地RAG依赖

```bash
# 确保在项目目录
cd LENR-Google-claude-gemini-file-search-docs-011CUzqZmQcNRQCJLJmqNczS

# 安装本地RAG依赖（包含所有需要的包）
pip install -r requirements_local.txt

# 这会安装:
# - ChromaDB (本地向量数据库)
# - sentence-transformers (本地embedding)
# - PyPDF2, python-docx (文档处理)
# - torch (PyTorch后端)
# - streamlit (Web UI)
# - google-genai (可选,用于生成答案)
```

### Step 2: 测试本地RAG

```bash
# 运行测试脚本
python examples/test_local_rag.py
```

**期望输出:**
```
============================================================
本地RAG测试 / Local RAG Test
============================================================

1. 初始化LocalRAG...
✅ Local RAG initialized

2. 创建collection...
✅ Created collection: test_docs

3. 上传demo文件...
   上传: lenr_overview_2024.txt
   ✅ 45 chunks indexed
   上传: experimental_methods.txt
   ✅ 38 chunks indexed

4. 数据库统计:
   Collections: 1
   Total documents: 83
   Database size: 0.52 MB

5. 测试查询...
   Q: What is LENR?
   A: LENR stands for Low Energy Nuclear Reactions...
   Sources: 3

✅ 测试完成！
```

### Step 3: 运行Web UI

```bash
# 运行本地RAG的Streamlit界面
python -m streamlit run streamlit_app.py
```

浏览器打开: `http://localhost:8501`

---

## 详细功能测试 / Detailed Function Test

### 测试1: 创建Collection

```python
from src.rag.local_rag import LocalRAG

# 初始化
rag = LocalRAG(persist_directory="./my_rag_db")

# 创建collection
rag.create_collection("test_collection")
print("✅ Collection created")
```

### 测试2: 上传单个文件

```python
# 上传PDF
chunks = rag.upload_file(
    "document.pdf",
    collection_name="test_collection"
)
print(f"✅ Uploaded: {chunks} chunks")
```

### 测试3: 批量上传

```python
from pathlib import Path

# 上传文件夹中所有文件
folder = Path("my_documents")
for file in folder.rglob("*.*"):
    if file.suffix in ['.pdf', '.txt', '.xlsx', '.docx']:
        print(f"Uploading {file.name}...")
        chunks = rag.upload_file(file, "test_collection")
        print(f"✅ {chunks} chunks")
```

### 测试4: 查询

```python
# 查询
result = rag.query(
    "What is LENR?",
    collection_name="test_collection",
    n_results=5
)

print("Answer:", result['answer'])
print(f"Sources: {result['n_sources']}")

# 查看sources
for source in result['sources']:
    print(f"- {source['filename']}: {source['text'][:100]}...")
```

### 测试5: 查看统计

```python
stats = rag.get_stats()
print(f"Collections: {stats['collections']}")
print(f"Total docs: {stats['total_documents']}")
print(f"DB size: {stats['database_size_mb']:.2f} MB")
```

---

## 问题排查 / Troubleshooting

### 问题1: ImportError: No module named 'chromadb'

**解决:**
```bash
pip install chromadb>=0.4.24
```

### 问题2: ImportError: No module named 'sentence_transformers'

**解决:**
```bash
pip install sentence-transformers>=2.3.0
```

### 问题3: ImportError: No module named 'PyPDF2'

**解决:**
```bash
pip install PyPDF2>=3.0.0
```

### 问题4: ImportError: No module named 'docx'

**解决:**
```bash
pip install python-docx>=1.1.0
```

### 问题5: Torch安装失败

**解决 (CPU版本):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**解决 (GPU版本 - 如果有CUDA):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### 问题6: 下载embedding模型慢

**解决:**
第一次运行会下载模型 (~80MB)，耐心等待或使用国内镜像:

```bash
# 设置HuggingFace镜像
export HF_ENDPOINT=https://hf-mirror.com
```

### 问题7: Memory error

**解决:**
使用更小的embedding模型:

```python
rag = LocalRAG(embedding_model="paraphrase-MiniLM-L3-v2")  # 更小
```

### 问题8: ChromaDB database locked

**解决:**
```bash
# 删除锁文件
rm -rf chroma_db/.chroma.lock
```

---

## 完整工作流程 / Complete Workflow

### 方案A: 使用Python脚本

```python
# complete_workflow.py
from pathlib import Path
from src.rag.local_rag import LocalRAG

# 1. 初始化
print("初始化...")
rag = LocalRAG(persist_directory="./my_knowledge_base")

# 2. 创建collection
print("创建collection...")
rag.create_collection("my_docs")

# 3. 批量上传文件
print("上传文件...")
docs_folder = Path("my_local_files")

uploaded_count = 0
for file in docs_folder.rglob("*"):
    if file.suffix in ['.pdf', '.txt', '.md', '.xlsx', '.docx']:
        try:
            chunks = rag.upload_file(file, "my_docs")
            print(f"✅ {file.name}: {chunks} chunks")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ {file.name}: {e}")

print(f"\n上传完成! 总共 {uploaded_count} 个文件")

# 4. 查询测试
print("\n测试查询...")
questions = [
    "总结主要内容",
    "有哪些重要发现?",
    "关键数据是什么?"
]

for q in questions:
    result = rag.query(q, "my_docs", n_results=3)
    print(f"\nQ: {q}")
    print(f"A: {result['answer'][:200]}...")

# 5. 统计
stats = rag.get_stats()
print(f"\n统计信息:")
print(f"- Collections: {stats['collections']}")
print(f"- 文档数: {stats['total_documents']}")
print(f"- 数据库大小: {stats['database_size_mb']:.2f} MB")
```

运行:
```bash
python complete_workflow.py
```

### 方案B: 使用Web UI

```bash
# 启动Web界面
python -m streamlit run streamlit_app.py
```

然后:
1. 侧边栏: 创建collection
2. 📤 Upload tab: 上传文件
3. 💬 Query tab: 提问
4. 查看答案和sources

---

## 性能对比 / Performance Comparison

| 指标 | Google Cloud RAG | 本地RAG |
|------|------------------|---------|
| 存储限制 | 10GB | 无限制 |
| 首次indexing | 上传+云端处理 | 本地处理 |
| 查询速度 | API调用 | 本地搜索(快) |
| 成本 | API费用 | 免费 |
| 隐私 | 数据上传云端 | 数据本地 |
| 网络需求 | 全程需要 | 仅生成答案需要 |

---

## 下一步 / Next Steps

### 1. 生产环境配置

```python
# production_config.py
rag = LocalRAG(
    persist_directory="/data/rag_db",  # 持久化路径
    embedding_model="all-mpnet-base-v2",  # 更好的模型
)
```

### 2. 自动化pipeline

```bash
# 定时任务自动索引新文件
crontab -e

# 每小时检查并索引新文件
0 * * * * cd /path/to/project && python auto_index_local.py sync
```

### 3. Snowflake部署

查看 `LOCAL_RAG_GUIDE.md` 中的Snowflake部署章节

---

## 验证清单 / Verification Checklist

运行这个checklist确保一切正常:

```bash
# ✅ Step 1: 依赖安装
pip list | grep chromadb
pip list | grep sentence-transformers
pip list | grep PyPDF2
pip list | grep python-docx

# ✅ Step 2: 测试import
python -c "from src.rag.local_rag import LocalRAG; print('✅ Import success')"

# ✅ Step 3: 测试初始化
python -c "from src.rag.local_rag import LocalRAG; rag = LocalRAG(); print('✅ Init success')"

# ✅ Step 4: 测试collection
python -c "from src.rag.local_rag import LocalRAG; rag = LocalRAG(); rag.create_collection('test'); print('✅ Collection success')"

# ✅ Step 5: 运行完整测试
python examples/test_local_rag.py

# ✅ Step 6: 启动Web UI
python -m streamlit run streamlit_app.py
```

全部 ✅ = 系统ready!

---

## 获取帮助 / Get Help

如果还有问题:

1. **查看日志:**
   ```bash
   # 开启详细日志
   export LOG_LEVEL=DEBUG
   python examples/test_local_rag.py
   ```

2. **检查数据库:**
   ```bash
   ls -lh chroma_db/
   ```

3. **清除重试:**
   ```bash
   rm -rf chroma_db/
   rm -rf test_chroma_db/
   python examples/test_local_rag.py
   ```

4. **查看系统信息:**
   ```python
   import sys, torch
   print(f"Python: {sys.version}")
   print(f"Torch: {torch.__version__}")
   ```

---

**现在开始使用吧！/ Let's Start!**

```bash
# 一条命令安装并测试
pip install -r requirements_local.txt && python examples/test_local_rag.py
```
