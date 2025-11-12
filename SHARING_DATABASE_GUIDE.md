# 分享和部署RAG数据库完整指南
# Complete Guide to Sharing and Deploying RAG Database

解决你的两个问题：
1. ✅ Google Cloud 10GB限制 - 有7000个文件无法全部上传
2. ✅ 如何分享建好的数据库

---

## 问题分析

### 问题1: Google Cloud 10GB限制

你遇到的错误：
```
'message': 'Corpus has reached the storage limit of 10000000000 bytes.'
'status': 'RESOURCE_EXHAUSTED'
```

**原因:** Google Cloud File Search有10GB硬限制

**解决方案:** 使用本地RAG系统 - 无限制！

### 问题2: 如何分享数据库

需要能够：
- 导出整个数据库（包含所有7000个文件的索引）
- 分享给其他人使用
- 部署到Snowflake或其他平台

---

## 完整解决方案

## 方案A: 本地RAG - 索引所有7000个文件

### Step 1: 安装本地RAG

```bash
# 安装依赖
pip install -r requirements_local.txt
```

### Step 2: 批量索引7000个文件

创建索引脚本 `index_all_files.py`:

```python
from pathlib import Path
from src.rag.local_rag import LocalRAG
from tqdm import tqdm

# 初始化
rag = LocalRAG(
    persist_directory="./large_rag_db",  # 本地数据库路径
    embedding_model="all-MiniLM-L6-v2"  # 快速模型
)

# 创建collection
rag.create_collection("all_documents")

# 你的7000个文件路径
files_folder = Path("my_local_files/research")

# 获取所有文件
all_files = list(files_folder.rglob("*"))
supported_extensions = {'.pdf', '.txt', '.md', '.docx', '.xlsx', '.xls'}
files_to_index = [
    f for f in all_files
    if f.is_file() and f.suffix.lower() in supported_extensions
]

print(f"Found {len(files_to_index)} files to index")

# 批量索引
successful = 0
failed = 0

for file in tqdm(files_to_index, desc="Indexing"):
    try:
        chunks = rag.upload_file(
            file,
            collection_name="all_documents",
            metadata={"category": file.parent.name}
        )
        successful += 1
    except Exception as e:
        print(f"Failed: {file.name} - {e}")
        failed += 1

print(f"\n✅ Indexing complete!")
print(f"   Successful: {successful}")
print(f"   Failed: {failed}")

# 显示统计
stats = rag.get_stats()
print(f"\n📊 Database stats:")
print(f"   Total documents: {stats['total_documents']}")
print(f"   Database size: {stats['database_size_mb']:.2f} MB")
```

运行:
```bash
python index_all_files.py
```

**预计时间:** 7000个文件 ≈ 2-4小时（取决于文件大小和CPU）

### Step 3: 测试数据库

```python
from src.rag.local_rag import LocalRAG

rag = LocalRAG(persist_directory="./large_rag_db")

result = rag.query(
    "Your question here",
    collection_name="all_documents",
    n_results=10
)

print(result['answer'])
```

---

## 方案B: 导出和分享数据库

### 1. 导出数据库

```bash
# 导出为单个压缩文件
python database_manager.py export ./large_rag_db my_rag_7000_files.tar.gz
```

输出:
```
Exporting database from ./large_rag_db...
✅ Database exported successfully!
   File: my_rag_7000_files.tar.gz
   Size: 1234.56 MB

📦 Database ready for sharing!
```

### 2. 分享方式

#### 选项1: 文件分享平台

**上传到:**
- Google Drive
- Dropbox
- WeTransfer
- 百度网盘
- OneDrive

```bash
# 例子：上传到Google Drive
# 1. 访问 drive.google.com
# 2. 上传 my_rag_7000_files.tar.gz
# 3. 获取分享链接
# 4. 分享给其他人
```

#### 选项2: 云存储服务

**AWS S3:**
```bash
# 上传到S3
aws s3 cp my_rag_7000_files.tar.gz s3://your-bucket/

# 生成预签名URL（有效期7天）
aws s3 presign s3://your-bucket/my_rag_7000_files.tar.gz --expires-in 604800
```

**Google Cloud Storage:**
```bash
# 上传到GCS
gsutil cp my_rag_7000_files.tar.gz gs://your-bucket/

# 公开链接
gsutil acl ch -u AllUsers:R gs://your-bucket/my_rag_7000_files.tar.gz
```

#### 选项3: GitHub Releases (如果<2GB)

```bash
# 1. 创建GitHub Release
# 2. 上传 my_rag_7000_files.tar.gz 作为asset
# 3. 用户可以直接下载
```

### 3. 接收者如何使用

接收者收到 `my_rag_7000_files.tar.gz` 后:

```bash
# 1. 下载文件

# 2. 导入数据库
python database_manager.py import my_rag_7000_files.tar.gz ./my_rag_db

# 3. 运行Streamlit
python -m streamlit run streamlit_app.py

# 4. 在UI中选择collection并开始查询
```

---

## 方案C: 部署到Snowflake（带数据库）

### Snowflake部署策略

#### 策略1: 使用Snowflake Stage存储数据库

```python
# snowflake_persistence.py
import snowflake.connector
import tarfile
from pathlib import Path

def upload_database_to_stage(db_path, stage_name):
    """上传数据库到Snowflake Stage"""

    # 1. 压缩数据库
    archive = "rag_db.tar.gz"
    with tarfile.open(archive, 'w:gz') as tar:
        tar.add(db_path, arcname='chroma_db')

    # 2. 连接Snowflake
    conn = snowflake.connector.connect(
        user='your_user',
        password='your_password',
        account='your_account'
    )

    # 3. 上传到Stage
    cursor = conn.cursor()
    cursor.execute(f"PUT file://{archive} @{stage_name}/")

    print(f"✅ Database uploaded to Snowflake Stage: {stage_name}")

def download_database_from_stage(stage_name, target_path):
    """从Snowflake Stage下载数据库"""

    conn = snowflake.connector.connect(
        user='your_user',
        password='your_password',
        account='your_account'
    )

    cursor = conn.cursor()
    cursor.execute(f"GET @{stage_name}/rag_db.tar.gz file:///tmp/")

    # 解压
    with tarfile.open('/tmp/rag_db.tar.gz', 'r:gz') as tar:
        tar.extractall(target_path)

    print(f"✅ Database downloaded to {target_path}")
```

在 `streamlit_app.py` 中使用:

```python
import streamlit as st
from snowflake_persistence import download_database_from_stage

@st.cache_resource
def init_rag():
    """Initialize RAG with Snowflake persistence"""

    # 从Snowflake Stage下载数据库
    if not Path("/tmp/chroma_db").exists():
        with st.spinner("Loading database from Snowflake..."):
            download_database_from_stage("MY_STAGE", "/tmp")

    return LocalRAG(persist_directory="/tmp/chroma_db")
```

#### 策略2: 使用Snowflake Table存储Embeddings

```python
# snowflake_table_persistence.py
import snowflake.connector
import numpy as np

def save_embeddings_to_table(rag, collection_name):
    """保存embeddings到Snowflake表"""

    collection = rag.chroma_client.get_collection(collection_name)

    # 获取所有数据
    data = collection.get(include=['embeddings', 'documents', 'metadatas'])

    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rag_embeddings (
            id STRING,
            document STRING,
            embedding ARRAY,
            metadata VARIANT
        )
    """)

    # 插入数据
    for id, doc, emb, meta in zip(
        data['ids'],
        data['documents'],
        data['embeddings'],
        data['metadatas']
    ):
        cursor.execute("""
            INSERT INTO rag_embeddings VALUES (%s, %s, %s, %s)
        """, (id, doc, emb, json.dumps(meta)))

    print(f"✅ Saved {len(data['ids'])} embeddings to Snowflake")

def load_embeddings_from_table():
    """从Snowflake表加载embeddings"""

    conn = snowflake.connector.connect(...)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rag_embeddings")
    rows = cursor.fetchall()

    # 重建ChromaDB
    # ...
```

---

## 性能对比

| 方案 | 存储限制 | 索引时间(7000文件) | 查询速度 | 分享难度 |
|------|---------|-------------------|---------|---------|
| Google Cloud | ❌ 10GB | N/A (无法完成) | 快 | 不适用 |
| 本地RAG | ✅ 无限制 | 2-4小时 | 很快 | 简单 |
| 本地RAG + 导出 | ✅ 无限制 | 2-4小时 | 很快 | 很简单 |
| Snowflake + Stage | ✅ 无限制 | 2-4小时 | 快 | 中等 |

---

## 实际操作步骤

### 完整工作流程（推荐）

#### 1. 本地索引所有7000个文件

```bash
# 创建索引脚本
cat > index_all.py << 'EOF'
from pathlib import Path
from src.rag.local_rag import LocalRAG
import time

start_time = time.time()

rag = LocalRAG(persist_directory="./rag_7000_files")
rag.create_collection("all_docs")

files = list(Path("my_local_files").rglob("*"))
supported = ['.pdf', '.txt', '.md', '.docx', '.xlsx']
to_index = [f for f in files if f.suffix.lower() in supported]

print(f"Indexing {len(to_index)} files...")

for i, file in enumerate(to_index, 1):
    try:
        rag.upload_file(file, "all_docs")
        if i % 100 == 0:
            print(f"Progress: {i}/{len(to_index)}")
    except Exception as e:
        print(f"Error {file.name}: {e}")

elapsed = time.time() - start_time
print(f"\nDone! Time: {elapsed/3600:.1f} hours")
print(f"Database: ./rag_7000_files")
EOF

# 运行索引
python index_all.py
```

#### 2. 导出数据库

```bash
python database_manager.py export ./rag_7000_files shared_rag_7000.tar.gz
```

#### 3. 上传分享

```bash
# 选项A: 上传到Google Drive
# 手动上传 shared_rag_7000.tar.gz

# 选项B: 上传到AWS S3
aws s3 cp shared_rag_7000.tar.gz s3://my-bucket/
aws s3 presign s3://my-bucket/shared_rag_7000.tar.gz --expires-in 604800

# 选项C: 上传到Snowflake Stage
# （见上面Snowflake策略）
```

#### 4. 其他人使用

分享这个说明给接收者:

```markdown
# 使用共享的RAG数据库

1. 下载数据库文件: shared_rag_7000.tar.gz
2. 安装依赖: pip install -r requirements_local.txt
3. 导入数据库: python database_manager.py import shared_rag_7000.tar.gz ./my_db
4. 运行应用: python -m streamlit run streamlit_app.py
5. 开始查询!
```

---

## 数据库维护

### 更新数据库

```python
# add_new_files.py
from src.rag.local_rag import LocalRAG
from pathlib import Path

rag = LocalRAG(persist_directory="./rag_7000_files")

# 添加新文件
new_files = Path("new_documents").glob("*.pdf")
for file in new_files:
    rag.upload_file(file, "all_docs")
    print(f"Added: {file.name}")

# 重新导出
# python database_manager.py export ./rag_7000_files updated_rag.tar.gz
```

### 合并多个数据库

```python
from database_manager import RAGDatabaseManager

manager = RAGDatabaseManager()

# 合并多个数据库
manager.merge_databases(
    db_paths=["./db1", "./db2", "./db3"],
    target_db_path="./merged_db",
    new_collection_name="combined"
)
```

---

## 常见问题

### Q: 7000个文件要多久？

A: 取决于：
- 文件大小: 平均每文件1MB = 7GB总数据
- CPU速度: 现代CPU约2-4小时
- 硬盘速度: SSD更快

**估算:**
- Fast CPU + SSD: 2小时
- Normal CPU: 3-4小时
- Slow CPU: 5-6小时

### Q: 数据库有多大？

A: 大约是原始文件的30-50%:
- 7000个PDF (7GB) → 数据库约2-3GB
- 压缩后 `.tar.gz` → 约1-1.5GB

### Q: 分享需要多久？

A: 取决于网速:
- 上传1.5GB到Google Drive (100Mbps) ≈ 2-3分钟
- 下载1.5GB (100Mbps) ≈ 2-3分钟

### Q: Snowflake免费版有限制吗？

A: Snowflake有存储和计算限制，但对于RAG数据库（几GB）通常足够。

### Q: 可以增量更新吗？

A: 可以！只需：
```bash
# 添加新文件到现有数据库
rag = LocalRAG(persist_directory="./rag_7000_files")
rag.upload_file("new_file.pdf", "all_docs")

# 重新导出
python database_manager.py export ./rag_7000_files updated.tar.gz
```

---

## 总结

### 你的问题解决了！

1. ✅ **Google 10GB限制**
   - 使用本地RAG
   - 可以索引所有7000个文件
   - 无存储限制

2. ✅ **分享数据库**
   - 导出为单个文件
   - 上传到云存储
   - 其他人轻松导入使用

### 推荐流程

```bash
# 1. 索引所有文件（一次性）
python index_all.py  # 2-4小时

# 2. 导出数据库
python database_manager.py export ./rag_7000_files shared.tar.gz

# 3. 分享
# 上传到Google Drive/S3/等

# 4. 接收者使用
python database_manager.py import shared.tar.gz ./my_db
python -m streamlit run streamlit_app.py
```

### 下一步

开始索引你的7000个文件:

```bash
pip install -r requirements_local.txt
python index_all.py
```

全部完成! 🎉
