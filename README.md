# LENR RAG系统 - Gemini版本

**为你的7000+文件提供最佳RAG解决方案**

用Google Gemini API构建，无10GB限制，成本最低。

---

## ⚡ 快速开始 (3分钟)

**只需1个API密钥 • $0.50-1/月 • 免费embeddings**

```bash
# 步骤1: 安装依赖 (1分钟)
pip install -r requirements_gemini.txt

# 步骤2: 设置API密钥 (1分钟)
echo "GOOGLE_API_KEY=your-key-here" > .env

# 步骤3: 测试系统 (1分钟)
python examples/test_gemini_smart_rag.py

# 步骤4: 索引你的文件
python index_gemini.py

# 步骤5: 启动Web界面
streamlit run streamlit_gemini.py
```

**获取API密钥:** https://aistudio.google.com/apikey

**完整指南:** `START_GEMINI.md`

---

## 🎯 核心优势

### 解决你的问题

✅ **无10GB限制** - 本地存储，无限空间
✅ **处理7000+文件** - 轻松索引所有文件
✅ **最低成本** - $0.50-1/月，免费embeddings
✅ **优秀质量** - Gemini 2.0 Flash
✅ **简单设置** - 3分钟完成
✅ **易于分享** - 导出/导入数据库

### 为什么选择Gemini

| 功能 | Gemini方案 |
|------|-----------|
| **API密钥数量** | 1个 (只需Google) |
| **每月成本** | $0.50-1 |
| **Embeddings成本** | **免费** ✨ |
| **每次查询成本** | $0.0005 |
| **存储限制** | 无限制 (本地) |
| **质量** | 优秀 (Gemini 2.0) |
| **设置时间** | 3分钟 |
| **索引时间** | 1-2小时 (7000文件) |
| **长上下文** | 2M tokens |

---

## 📦 功能特性

### 支持的文件类型
- PDF (`.pdf`)
- 文本 (`.txt`, `.md`)
- Word (`.docx`)
- Excel (`.xlsx`, `.xls`)

### 核心功能
- ✅ 自动重复检测 (基于SHA256哈希)
- ✅ 进度跟踪 (tqdm进度条)
- ✅ 批量上传 (支持7000+文件)
- ✅ 本地向量数据库 (ChromaDB)
- ✅ 免费embeddings (Gemini API)
- ✅ 优秀的LLM (Gemini 2.0 Flash)
- ✅ 美观的Web界面 (Streamlit)
- ✅ 数据库导出/导入 (分享功能)
- ✅ 成本追踪
- ✅ 多collection管理

---

## 💰 成本明细

### 你的7000个文件

**一次性成本 (索引):**
```
Embeddings: 免费 ✨
总计: $0
```

**每月成本 (1000次查询):**
```
存储: $0 (本地磁盘)
Embeddings: 免费 ✨
Gemini 2.0 Flash: 1000 × $0.0005 = $0.50

总计: $0.50-1/月
```

**每次查询:**
```
Embedding: 免费 ✨
Gemini生成: $0.0005

总计: ~$0.0005/次
```

---

## 🚀 使用方法

### 1. 获取API密钥

访问 https://aistudio.google.com/apikey 创建API密钥。

### 2. 安装和配置

```bash
# 安装依赖
pip install -r requirements_gemini.txt

# 设置API密钥
echo "GOOGLE_API_KEY=your-key-here" > .env
```

### 3. 测试系统

```bash
python examples/test_gemini_smart_rag.py
```

你会看到:
```
✅ Gemini Smart RAG initialized
✅ Created collection: test_docs
✅ 45 chunks indexed
📝 Answer: LENR stands for Low Energy Nuclear Reactions...
📚 Sources: 3
💰 Cost: FREE embeddings + $0.0005 per query
```

### 4. 索引你的文件

```bash
# 将文件放到 my_local_files/ 目录
mkdir -p my_local_files
cp your_files/* my_local_files/

# 运行索引脚本
python index_gemini.py
```

这会:
- 自动查找所有支持的文件
- 显示进度条
- 跳过重复文件
- 保存到本地数据库
- 完全免费 (embeddings免费)

### 5. 查询数据

#### 方式A: Web界面 (推荐)

```bash
streamlit run streamlit_gemini.py
```

然后访问 http://localhost:8501

#### 方式B: Python脚本

```python
from src.rag.gemini_smart_rag import GeminiSmartRAG

# 初始化
rag = GeminiSmartRAG()

# 查询
result = rag.query("你的问题", collection_name="my_docs")

# 显示结果
print(result['answer'])
print(f"来源: {result['n_sources']}")
```

---

## 📤 分享数据库

### 导出数据库

```bash
python database_manager.py export ./gemini_smart_rag_db my_database.tar.gz
```

### 分享

上传 `my_database.tar.gz` 到:
- Google Drive
- 百度网盘
- Dropbox
- 阿里云盘

### 导入数据库 (接收者)

```bash
# 安装依赖
pip install -r requirements_gemini.txt

# 导入数据库
python database_manager.py import my_database.tar.gz ./gemini_smart_rag_db

# 启动
streamlit run streamlit_gemini.py
```

---

## 🏗️ 技术架构

```
用户问题
    ↓
Gemini Embeddings (FREE)
    ↓ [768-dim向量]
ChromaDB (本地向量搜索)
    ↓ [Top 5相关块]
Gemini 2.0 Flash ($0.0005/query)
    ↓
答案 + 引用来源
```

---

## 📂 项目结构

```
.
├── src/rag/
│   ├── gemini_smart_rag.py      # Gemini RAG实现
│   ├── local_rag.py              # 本地RAG (备用)
│   └── gemini_rag.py             # 原始Gemini RAG
├── examples/
│   └── test_gemini_smart_rag.py # 测试脚本
├── streamlit_gemini.py           # Web界面
├── index_gemini.py               # 索引脚本
├── database_manager.py           # 数据库管理
├── requirements_gemini.txt       # 依赖
└── START_GEMINI.md               # 完整指南
```

---

## 🔧 常见问题

### 问: 7000个文件需要多久？

**答:** 约1-2小时
- 取决于文件大小和CPU速度
- 使用进度条可以看到进度
- Embeddings是免费的！

### 问: 数据库会有多大？

**答:** 约原始文件的30-40%
- 7000个PDF (7GB) → 数据库约2-3GB
- 压缩后 `.tar.gz` → 约1GB

### 问: 可以在Snowflake部署吗？

**答:** 可以！
1. 上传 `streamlit_gemini.py` 和 `src/` 文件夹
2. 添加 `GOOGLE_API_KEY` 密钥
3. 部署即可

### 问: 支持中文吗？

**答:** 完全支持！
- Gemini支持中文查询
- 可以索引中文文档
- 界面也可以显示中文

---

## 📚 文档

- **START_GEMINI.md** - 完整中文指南
- **database_manager.py** - 数据库导出/导入工具
- **Google AI Studio** - https://aistudio.google.com/

---

## 🎉 总结

你得到的最佳方案:

✅ **解决10GB限制** - 本地存储无限
✅ **处理7000+文件** - 轻松索引
✅ **最低成本** - $0.50-1/月，免费embeddings
✅ **优秀质量** - Gemini 2.0 Flash
✅ **简单设置** - 只需3分钟，1个API密钥
✅ **易于分享** - 导出/导入数据库
✅ **长上下文** - 2M tokens支持

**立即开始:**

```bash
pip install -r requirements_gemini.txt
echo "GOOGLE_API_KEY=your-key" > .env
python examples/test_gemini_smart_rag.py
python index_gemini.py
streamlit run streamlit_gemini.py
```

💎 **简单。强大。最便宜。用Gemini！**
