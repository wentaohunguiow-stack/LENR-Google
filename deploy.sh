#!/bin/bash

# Gemini Smart RAG部署脚本
# 适用于Ubuntu/Debian VPS

set -e

echo "========================================="
echo "Gemini Smart RAG 部署脚本"
echo "========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查root权限
if [ "$EUID" -eq 0 ]; then
  echo -e "${RED}请不要使用root用户运行此脚本${NC}"
  echo "使用: ./deploy.sh"
  exit 1
fi

# 步骤1: 更新系统
echo -e "${YELLOW}步骤 1/8: 更新系统...${NC}"
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx curl

# 步骤2: 创建应用目录
echo -e "${YELLOW}步骤 2/8: 创建应用目录...${NC}"
APP_DIR="/opt/gemini-rag"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# 步骤3: 复制文件
echo -e "${YELLOW}步骤 3/8: 复制应用文件...${NC}"
if [ -d "$APP_DIR" ]; then
    cp -r ./* $APP_DIR/
    cd $APP_DIR
else
    echo -e "${RED}无法创建应用目录${NC}"
    exit 1
fi

# 步骤4: 创建虚拟环境
echo -e "${YELLOW}步骤 4/8: 创建Python虚拟环境...${NC}"
python3 -m venv venv
source venv/bin/activate

# 步骤5: 安装依赖
echo -e "${YELLOW}步骤 5/8: 安装Python依赖...${NC}"
pip install --upgrade pip
pip install -r requirements_gemini.txt

# 步骤6: 配置环境变量
echo -e "${YELLOW}步骤 6/8: 配置环境变量...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}请输入你的Google API密钥:${NC}"
    read -r GOOGLE_API_KEY
    echo "GOOGLE_API_KEY=$GOOGLE_API_KEY" > .env
    echo -e "${GREEN}✓ 环境变量已配置${NC}"
else
    echo -e "${GREEN}✓ .env文件已存在${NC}"
fi

# 步骤7: 创建systemd服务
echo -e "${YELLOW}步骤 7/8: 创建systemd服务...${NC}"
sudo tee /etc/systemd/system/gemini-rag.service > /dev/null <<EOF
[Unit]
Description=Gemini Smart RAG
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/streamlit run streamlit_gemini.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable gemini-rag
sudo systemctl start gemini-rag

echo -e "${GREEN}✓ Systemd服务已创建并启动${NC}"

# 步骤8: 配置Nginx
echo -e "${YELLOW}步骤 8/8: 配置Nginx反向代理...${NC}"

# 询问域名
echo -e "${YELLOW}请输入你的域名 (留空则使用IP):${NC}"
read -r DOMAIN_NAME

if [ -z "$DOMAIN_NAME" ]; then
    DOMAIN_NAME="_"
    echo -e "${YELLOW}将使用服务器IP访问${NC}"
fi

sudo tee /etc/nginx/sites-available/gemini-rag > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 86400;
    }
}
EOF

# 启用站点
sudo ln -sf /etc/nginx/sites-available/gemini-rag /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

echo -e "${GREEN}✓ Nginx已配置${NC}"

# 完成
echo ""
echo "========================================="
echo -e "${GREEN}✓ 部署完成！${NC}"
echo "========================================="
echo ""
echo "访问地址:"
if [ "$DOMAIN_NAME" = "_" ]; then
    SERVER_IP=$(curl -s ifconfig.me)
    echo -e "  ${GREEN}http://$SERVER_IP${NC}"
else
    echo -e "  ${GREEN}http://$DOMAIN_NAME${NC}"
fi
echo ""
echo "常用命令:"
echo "  查看状态: sudo systemctl status gemini-rag"
echo "  查看日志: sudo journalctl -u gemini-rag -f"
echo "  重启服务: sudo systemctl restart gemini-rag"
echo "  停止服务: sudo systemctl stop gemini-rag"
echo ""
echo "下一步:"
echo "  1. 访问上面的地址"
echo "  2. 上传文件并索引"
echo "  3. 开始使用！"
echo ""
