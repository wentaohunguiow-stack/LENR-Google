# 部署指南 - Gemini Smart RAG

完整的部署方案，支持多种平台。

---

## 🚀 快速部署选项

### 选项1: Snowflake Streamlit (推荐)
- ✅ 无需服务器
- ✅ 自动扩展
- ✅ 内置认证
- ✅ 5分钟部署

### 选项2: Docker (本地/云)
- ✅ 完全控制
- ✅ 易于迁移
- ✅ 支持所有云平台

### 选项3: 直接部署 (VPS/服务器)
- ✅ 最简单
- ✅ 适合个人使用

---

## 选项1: Snowflake Streamlit部署

### 准备工作

1. **Snowflake账号**
   - 访问: https://signup.snowflake.com/
   - 免费试用30天

2. **准备文件**
   ```bash
   # 需要的文件
   streamlit_gemini.py          # 主应用
   src/                         # 源代码文件夹
   requirements_gemini.txt      # 依赖
   ```

### 步骤1: 创建environment.yml

创建 `environment.yml`:

```yaml
name: gemini_rag
channels:
  - snowflake
  - conda-forge
dependencies:
  - python=3.11
  - pip
  - pip:
      - google-genai>=0.3.0
      - chromadb>=0.4.24
      - streamlit>=1.29.0
      - PyPDF2>=3.0.0
      - python-docx>=1.1.0
      - openpyxl>=3.1.0
      - pandas>=2.0.0
      - python-dotenv>=1.0.0
      - tqdm>=4.66.0
```

### 步骤2: 修改streamlit_gemini.py

在文件开头添加Snowflake兼容性:

```python
import os
import streamlit as st

# Snowflake secrets (如果在Snowflake部署)
def get_api_key():
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except:
        return os.getenv("GOOGLE_API_KEY")

# 使用Snowflake临时存储
persist_dir = "/tmp/gemini_smart_rag_db"
```

### 步骤3: 上传到Snowflake

1. **登录Snowflake**
   ```
   https://app.snowflake.com/
   ```

2. **创建Streamlit App**
   - 点击 "Streamlit" → "Create"
   - 选择 "From scratch"

3. **上传文件**
   - 主文件: `streamlit_gemini.py`
   - 上传整个 `src/` 文件夹
   - 上传 `environment.yml`

4. **配置Secrets**
   - 点击 "Settings" → "Secrets"
   - 添加:
   ```toml
   GOOGLE_API_KEY = "your-google-api-key-here"
   ```

5. **部署**
   - 点击 "Deploy"
   - 等待1-2分钟

### 步骤4: 上传预索引的数据库

```python
# 在本地先索引好数据库
python index_gemini.py

# 导出数据库
python database_manager.py export ./gemini_smart_rag_db db.tar.gz

# 创建Snowflake stage
# 在Snowflake中运行:
CREATE STAGE IF NOT EXISTS rag_stage;
PUT file:///path/to/db.tar.gz @rag_stage;

# 在streamlit_gemini.py中添加加载代码
import tarfile
def load_database():
    if not os.path.exists('/tmp/gemini_smart_rag_db'):
        # 从stage下载
        cursor.execute("GET @rag_stage/db.tar.gz file:///tmp/")
        with tarfile.open('/tmp/db.tar.gz', 'r:gz') as tar:
            tar.extractall('/tmp/')
```

---

## 选项2: Docker部署

### 创建Dockerfile

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements_gemini.txt .
RUN pip install --no-cache-dir -r requirements_gemini.txt

# 复制应用
COPY . .

# 暴露端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 启动命令
CMD ["streamlit", "run", "streamlit_gemini.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 创建docker-compose.yml

```yaml
version: '3.8'

services:
  gemini-rag:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - ./gemini_smart_rag_db:/app/gemini_smart_rag_db
      - ./my_local_files:/app/my_local_files
    restart: unless-stopped
```

### 部署步骤

```bash
# 1. 构建镜像
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 访问应用
# http://localhost:8501
```

### 部署到云平台

**AWS ECS:**
```bash
# 推送到ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag gemini-rag:latest <account>.dkr.ecr.us-east-1.amazonaws.com/gemini-rag:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/gemini-rag:latest
```

**Google Cloud Run:**
```bash
# 部署到Cloud Run
gcloud run deploy gemini-rag \
  --image gcr.io/PROJECT_ID/gemini-rag \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your-key
```

**Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name gemini-rag \
  --image myregistry.azurecr.io/gemini-rag:latest \
  --ports 8501 \
  --environment-variables GOOGLE_API_KEY=your-key
```

---

## 选项3: VPS直接部署

### 系统要求
- Linux (Ubuntu 20.04+)
- Python 3.11+
- 2GB+ RAM
- 10GB+ 磁盘

### 部署脚本

创建 `deploy.sh`:

```bash
#!/bin/bash

# 部署Gemini Smart RAG到VPS

echo "开始部署Gemini Smart RAG..."

# 1. 更新系统
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx

# 2. 创建应用目录
sudo mkdir -p /opt/gemini-rag
sudo chown $USER:$USER /opt/gemini-rag
cd /opt/gemini-rag

# 3. 克隆或复制代码
# git clone your-repo .
# 或者
# scp -r local-files/* user@server:/opt/gemini-rag/

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements_gemini.txt

# 6. 设置环境变量
echo "GOOGLE_API_KEY=your-key-here" > .env

# 7. 创建systemd服务
sudo tee /etc/systemd/system/gemini-rag.service > /dev/null <<EOF
[Unit]
Description=Gemini Smart RAG
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/gemini-rag
Environment="PATH=/opt/gemini-rag/venv/bin"
ExecStart=/opt/gemini-rag/venv/bin/streamlit run streamlit_gemini.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 8. 启动服务
sudo systemctl daemon-reload
sudo systemctl enable gemini-rag
sudo systemctl start gemini-rag

# 9. 配置Nginx反向代理
sudo tee /etc/nginx/sites-available/gemini-rag > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/gemini-rag /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "✅ 部署完成！"
echo "访问: http://your-domain.com"
```

### 使用方法

```bash
# 上传脚本到服务器
scp deploy.sh user@your-server:~/

# SSH到服务器
ssh user@your-server

# 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

---

## 生产环境配置

### 1. SSL证书 (Let's Encrypt)

```bash
# 安装certbot
sudo apt-get install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 2. 监控和日志

```bash
# 查看应用日志
sudo journalctl -u gemini-rag -f

# 查看Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# 系统资源监控
htop
```

### 3. 备份策略

```bash
# 创建备份脚本 backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/gemini-rag"

# 备份数据库
tar -czf $BACKUP_DIR/db_$DATE.tar.gz /opt/gemini-rag/gemini_smart_rag_db

# 备份代码
tar -czf $BACKUP_DIR/code_$DATE.tar.gz /opt/gemini-rag --exclude=venv --exclude=gemini_smart_rag_db

# 保留最近7天的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "✅ 备份完成: $DATE"
```

### 4. 设置定时任务

```bash
# 编辑crontab
crontab -e

# 添加每天凌晨2点备份
0 2 * * * /opt/gemini-rag/backup.sh
```

---

## 性能优化

### 1. 使用Redis缓存

```python
# 在streamlit_gemini.py中添加
import redis
import pickle

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached_query(question, collection_name):
    cache_key = f"query:{collection_name}:{question}"

    # 检查缓存
    cached = redis_client.get(cache_key)
    if cached:
        return pickle.loads(cached)

    # 执行查询
    result = rag.query(question, collection_name)

    # 保存缓存 (1小时)
    redis_client.setex(cache_key, 3600, pickle.dumps(result))

    return result
```

### 2. 配置进程数

```bash
# 修改systemd服务，使用gunicorn
ExecStart=/opt/gemini-rag/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8501 app:app
```

### 3. 数据库优化

```python
# 在gemini_smart_rag.py中使用连接池
from chromadb.config import Settings

settings = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=persist_dir,
    anonymized_telemetry=False
)
```

---

## 安全配置

### 1. 环境变量管理

```bash
# 使用.env文件
GOOGLE_API_KEY=your-key-here
ALLOWED_HOSTS=your-domain.com
SECRET_KEY=your-secret-key
```

### 2. 防火墙配置

```bash
# UFW防火墙
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS
sudo ufw enable
```

### 3. 限流配置

```nginx
# 在Nginx中添加限流
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

server {
    location / {
        limit_req zone=one burst=20;
        proxy_pass http://localhost:8501;
    }
}
```

---

## 故障排查

### 常见问题

**问题1: 应用无法启动**
```bash
# 检查日志
sudo journalctl -u gemini-rag -n 50

# 检查端口占用
sudo netstat -tulpn | grep 8501

# 手动测试
cd /opt/gemini-rag
source venv/bin/activate
streamlit run streamlit_gemini.py
```

**问题2: 内存不足**
```bash
# 增加swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**问题3: 数据库连接失败**
```bash
# 检查权限
ls -la /opt/gemini-rag/gemini_smart_rag_db

# 重建数据库
rm -rf gemini_smart_rag_db
python index_gemini.py
```

---

## 成本估算

### Snowflake Streamlit
- **免费试用**: 30天
- **付费**: ~$25/月 (小规模)

### VPS
- **DigitalOcean**: $6/月 (1GB RAM)
- **Vultr**: $6/月 (1GB RAM)
- **Linode**: $5/月 (1GB RAM)

### Docker云平台
- **Google Cloud Run**: 按使用付费 (~$5-10/月)
- **AWS Fargate**: ~$15-30/月
- **Azure Container**: ~$15-30/月

---

## 快速部署命令

### Snowflake
```bash
# 1. 准备文件
python deploy_snowflake.py

# 2. 上传到Snowflake UI
# 按照上面的步骤操作
```

### Docker
```bash
# 1行命令部署
docker-compose up -d
```

### VPS
```bash
# 1行命令部署
curl -sSL https://your-domain.com/deploy.sh | bash
```

---

## 总结

**推荐部署方案:**

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 个人使用 | VPS直接部署 | 简单便宜 |
| 团队使用 | Snowflake | 无需维护 |
| 企业使用 | Docker + 云平台 | 专业可靠 |

**下一步:**
1. 选择部署方案
2. 按照对应步骤操作
3. 访问应用测试

🚀 **祝部署顺利！**
