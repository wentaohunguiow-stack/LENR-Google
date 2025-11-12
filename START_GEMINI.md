# Start Here - Gemini Smart RAG

**最好的Gemini方案 - 简单、强大、最便宜**

只需要 **1个Google API密钥**。处理 **7000+文件**。成本 **$0.50-1/月**。

---

## 为什么选择Gemini Smart RAG？

| 功能 | Gemini Smart RAG | OpenAI Smart RAG |
|------|------------------|------------------|
| **API密钥** | 1 (只需Google) | 1 (只需OpenAI) |
| **设置时间** | 3分钟 | 3分钟 |
| **每月成本** | $0.50-1 | $3-5 |
| **Embeddings** | **免费** ✨ | 付费 |
| **质量** | 优秀 (Gemini 2.0) | 优秀 (GPT-4) |
| **存储** | 无限 (本地) | 无限 (本地) |

**Gemini Smart RAG = 最便宜的选择！**

---

## 3步设置 (3分钟)

### 步骤1: 获取Google API密钥 (1分钟)

1. 访问 https://aistudio.google.com/apikey
2. 点击 "Create API key"
3. 复制密钥

**成本**: ~$0.50-1/月 (1000次查询)

### 步骤2: 安装 (1分钟)

```bash
pip install -r requirements_gemini.txt
```

### 步骤3: 设置API密钥 (1分钟)

```bash
# 创建 .env 文件
echo "GOOGLE_API_KEY=your-key-here" > .env
```

**完成！就这么简单！**

---

## 测试是否工作

```bash
python examples/test_gemini_smart_rag.py
```

预期输出:
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

## 索引你的7000个文件

### 快速方式:

```bash
python index_gemini.py
```

这个脚本会:
1. 在 `my_local_files/` 中查找所有文件
2. 自动索引 (7000个文件需要1-2小时)
3. 显示进度条
4. 自动跳过重复文件

### 自定义脚本:

```python
from src.rag.gemini_smart_rag import GeminiSmartRAG
from pathlib import Path

# 初始化
rag = GeminiSmartRAG()
rag.create_collection("my_docs")

# 索引所有文件
files = list(Path("my_local_files").rglob("*"))
stats = rag.batch_upload(files, "my_docs", show_progress=True)

print(f"Indexed {stats['successful']} files!")
```

---

## 查询你的数据

### Web界面 (简单):

```bash
streamlit run streamlit_gemini.py
```

打开 http://localhost:8501

### Python脚本:

```python
from src.rag.gemini_smart_rag import GeminiSmartRAG

rag = GeminiSmartRAG()
result = rag.query("你的问题", collection_name="my_docs")
print(result['answer'])
```

---

## 分享你的数据库

### 导出:

```bash
python database_manager.py export ./gemini_smart_rag_db my_database.tar.gz
```

### 分享:
- 上传 `my_database.tar.gz` 到Google Drive、Dropbox等
- 分享链接给你的团队

### 导入 (团队成员):

```bash
pip install -r requirements_gemini.txt
python database_manager.py import my_database.tar.gz ./gemini_smart_rag_db
streamlit run streamlit_gemini.py
```

---

## 部署到Snowflake

1. **上传文件到Snowflake Streamlit:**
   - `streamlit_gemini.py`
   - `src/` 文件夹
   - `requirements_gemini.txt`

2. **在Snowflake中添加密钥:**
   ```toml
   GOOGLE_API_KEY = "your-key-here"
   ```

3. **部署！**

---

## 成本明细

### 一次性 (7000个文件):
```
索引 embeddings: 免费！✨

总计: $0 (免费！)
```

### 每月 (1000次查询):
```
存储: $0 (本地磁盘)
查询 embeddings: 免费！✨
Gemini 2.0 Flash 回答: 1000 × $0.0005 = $0.50

总计: ~$0.50-1/月
```

### 每次查询:
```
Embedding: 免费！✨
Gemini: $0.0005

总计: ~$0.0005 每次查询
```

**比OpenAI便宜10倍，比Enterprise RAG便宜30倍！**

---

## 功能

✅ **只需1个API密钥** - 只需Google，超简单
✅ **无限文件** - 没有10GB限制，本地存储
✅ **最便宜** - 免费embeddings + 最低查询成本
✅ **优秀质量** - Gemini 2.0 Flash
✅ **简单设置** - 3分钟
✅ **简单分享** - 导出/导入数据库文件
✅ **快速索引** - 本地处理，进度条
✅ **重复检测** - 自动，基于哈希
✅ **Snowflake就绪** - 几分钟内部署
✅ **长上下文** - 2M tokens (超长文档)

---

## 对比

### Gemini Smart RAG (推荐):
- **成本**: $0.50-1/月 (最便宜！)
- **设置**: 3分钟
- **API密钥**: 1
- **质量**: 优秀
- **Embeddings**: 免费 ✨
- **最适合**: 大多数用户

### OpenAI Smart RAG:
- **成本**: $3-5/月
- **设置**: 3分钟
- **API密钥**: 1
- **质量**: 优秀
- **Embeddings**: 付费
- **最适合**: 想用GPT-4的用户

### Enterprise RAG:
- **成本**: $15/月
- **设置**: 30分钟
- **API密钥**: 4
- **质量**: 优秀
- **最适合**: 大团队，需要Claude

### Local RAG:
- **成本**: $0-1/月
- **设置**: 10分钟
- **API密钥**: 0-1
- **质量**: 良好
- **最适合**: 注重隐私的用户

---

## 快速命令参考

```bash
# 设置
pip install -r requirements_gemini.txt
echo "GOOGLE_API_KEY=your-key" > .env

# 测试
python examples/test_gemini_smart_rag.py

# 索引文件
python index_gemini.py

# 启动Web界面
streamlit run streamlit_gemini.py

# 导出数据库
python database_manager.py export ./gemini_smart_rag_db backup.tar.gz

# 导入数据库
python database_manager.py import backup.tar.gz ./gemini_smart_rag_db
```

---

## 故障排除

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

## 支持

- **Google AI Studio**: https://aistudio.google.com/
- **API密钥**: https://aistudio.google.com/apikey
- **文档**: https://ai.google.dev/

---

## 总结

**你得到的:**
- 🎯 最简单设置 (3分钟, 1个API密钥)
- 💰 最低成本 ($0.50-1/月, 免费embeddings)
- 🚀 优秀质量 (Gemini 2.0 Flash)
- 📦 简单分享 (导出/导入)
- ⚡ 快速性能 (本地处理)
- 🔧 简单维护 (单一依赖)

**这是你7000+文件的最便宜解决方案。**

---

## 准备好了吗？

```bash
# 1. 从这里获取API密钥: https://aistudio.google.com/apikey
# 2. 运行:
pip install -r requirements_gemini.txt
echo "GOOGLE_API_KEY=your-key-here" > .env
python examples/test_gemini_smart_rag.py

# 3. 索引你的文件:
python index_gemini.py

# 4. 开始使用:
streamlit run streamlit_gemini.py
```

💎 **简单。强大。最便宜。**
