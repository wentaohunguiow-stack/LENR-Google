# 快速部署指南

3种部署方式，选择最适合你的。

---

## 🚀 方式1: Docker部署 (推荐 - 最简单)

**适合:** 有Docker的服务器或本地机器

### 1行命令部署

```bash
# 确保已设置GOOGLE_API_KEY
export GOOGLE_API_KEY="your-key-here"

# 启动
docker-compose up -d
```

访问: http://localhost:8501

### 停止和管理

```bash
# 停止
docker-compose down

# 查看日志
docker-compose logs -f

# 重启
docker-compose restart
```

---

## 🌐 方式2: VPS直接部署

**适合:** Ubuntu/Debian服务器

### 1行命令部署

```bash
# 上传代码到服务器后运行
./deploy.sh
```

这会自动:
- ✅ 安装所有依赖
- ✅ 创建systemd服务
- ✅ 配置Nginx反向代理
- ✅ 启动应用

### 管理命令

```bash
# 查看状态
sudo systemctl status gemini-rag

# 查看日志
sudo journalctl -u gemini-rag -f

# 重启
sudo systemctl restart gemini-rag
```

---

## ☁️ 方式3: Snowflake Streamlit

**适合:** 不想管理服务器

### 准备文件

```bash
# 运行准备脚本
python deploy_snowflake.py
```

这会创建 `snowflake_deploy/` 目录，包含所有需要的文件。

### 上传到Snowflake

1. 访问: https://app.snowflake.com/
2. 创建新的Streamlit App
3. 上传 `snowflake_deploy/` 中的文件:
   - `streamlit_gemini.py`
   - `src/` 文件夹
   - `environment.yml`
4. 配置Secret:
   ```toml
   GOOGLE_API_KEY = "your-key"
   ```
5. 点击 Deploy

详细说明见: `snowflake_deploy/SNOWFLAKE_README.md`

---

## 📦 预索引数据库

如果你已经在本地索引了7000个文件，可以导出并部署:

```bash
# 1. 导出数据库
python database_manager.py export ./gemini_smart_rag_db db.tar.gz

# 2a. Docker部署 - 直接解压
tar -xzf db.tar.gz

# 2b. VPS部署 - 上传并解压
scp db.tar.gz user@server:/opt/gemini-rag/
ssh user@server "cd /opt/gemini-rag && tar -xzf db.tar.gz"

# 2c. Snowflake - 上传到Stage (见DEPLOY.md)
```

---

## 🔥 最快部署 (本地测试)

```bash
# 1. 设置API密钥
echo "GOOGLE_API_KEY=your-key" > .env

# 2. 安装依赖
pip install -r requirements_gemini.txt

# 3. 启动
streamlit run streamlit_gemini.py
```

---

## 🌍 云平台快速部署

### Google Cloud Run

```bash
# 构建并部署
gcloud run deploy gemini-rag \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your-key
```

### AWS ECS (使用docker-compose)

```bash
# 安装ECS CLI
docker compose --project-name gemini-rag up

# 或使用AWS Copilot
copilot init --app gemini-rag
copilot deploy
```

### Heroku

```bash
# 创建heroku.yml
echo "build:
  docker:
    web: Dockerfile
run:
  web: streamlit run streamlit_gemini.py" > heroku.yml

# 部署
heroku create gemini-rag
heroku stack:set container
git push heroku main
```

---

## ⚡ 性能优化建议

### 1. 使用预索引数据库
避免每次重启都重新索引。

### 2. 增加内存
至少2GB RAM用于7000个文件。

### 3. 使用缓存
在高流量情况下考虑Redis缓存。

---

## 🔧 故障排除

### Docker无法启动

```bash
# 检查日志
docker-compose logs

# 重建镜像
docker-compose build --no-cache
docker-compose up -d
```

### VPS端口被占用

```bash
# 检查8501端口
sudo netstat -tulpn | grep 8501

# 杀死占用进程
sudo kill -9 <PID>
```

### Snowflake内存不足

减小数据集大小或使用更大的Snowflake仓库。

---

## 📊 成本对比

| 方式 | 成本/月 | 优点 | 缺点 |
|------|--------|------|------|
| Docker本地 | $0 | 免费 | 需要电脑一直开机 |
| VPS | $5-10 | 简单可靠 | 需要管理服务器 |
| Snowflake | $25+ | 无需管理 | 成本较高 |
| Cloud Run | $5-15 | 按需付费 | 冷启动慢 |

---

## ✅ 部署检查清单

- [ ] 已获取Google API密钥
- [ ] 已设置环境变量或secrets
- [ ] 已测试API密钥有效
- [ ] (可选) 已准备预索引数据库
- [ ] 已选择部署方式
- [ ] 已完成部署
- [ ] 已测试应用可访问
- [ ] 已测试查询功能

---

## 🎯 推荐方案

| 场景 | 推荐 | 命令 |
|------|------|------|
| 快速测试 | 本地运行 | `streamlit run streamlit_gemini.py` |
| 个人使用 | Docker | `docker-compose up -d` |
| 团队使用 | VPS | `./deploy.sh` |
| 企业使用 | Snowflake | `python deploy_snowflake.py` |

---

## 📞 需要帮助？

查看完整文档:
- **DEPLOY.md** - 详细部署指南
- **START_GEMINI.md** - 系统使用指南
- **README.md** - 项目概览

🚀 **选择方案，立即部署！**
