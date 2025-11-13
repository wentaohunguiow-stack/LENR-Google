#!/bin/bash

# Gemini Smart RAG Deployment Script
# For Ubuntu/Debian VPS

set -e

echo "========================================="
echo "Gemini Smart RAG Deployment Script"
echo "========================================="
echo ""

# Color definitions
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check root permissions
if [ "$EUID" -eq 0 ]; then
  echo -e "${RED}Please do not run this script as root${NC}"
  echo "Usage: ./deploy.sh"
  exit 1
fi

# Step 1: Update system
echo -e "${YELLOW}Step 1/8: Updating system...${NC}"
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv nginx curl

# Step 2: Create application directory
echo -e "${YELLOW}Step 2/8: Creating application directory...${NC}"
APP_DIR="/opt/gemini-rag"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Step 3: Copy files
echo -e "${YELLOW}Step 3/8: Copying application files...${NC}"
if [ -d "$APP_DIR" ]; then
    cp -r ./* $APP_DIR/
    cd $APP_DIR
else
    echo -e "${RED}Failed to create application directory${NC}"
    exit 1
fi

# Step 4: Create virtual environment
echo -e "${YELLOW}Step 4/8: Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Step 5: Install dependencies
echo -e "${YELLOW}Step 5/8: Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements_gemini.txt

# Step 6: Configure environment variables
echo -e "${YELLOW}Step 6/8: Configuring environment variables...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}Please enter your Google API key:${NC}"
    read -r GOOGLE_API_KEY
    echo "GOOGLE_API_KEY=$GOOGLE_API_KEY" > .env
    echo -e "${GREEN}✓ Environment variables configured${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Step 7: Create systemd service
echo -e "${YELLOW}Step 7/8: Creating systemd service...${NC}"
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

# Start service
sudo systemctl daemon-reload
sudo systemctl enable gemini-rag
sudo systemctl start gemini-rag

echo -e "${GREEN}✓ Systemd service created and started${NC}"

# Step 8: Configure Nginx
echo -e "${YELLOW}Step 8/8: Configuring Nginx reverse proxy...${NC}"

# Ask for domain name
echo -e "${YELLOW}Please enter your domain name (leave empty to use IP):${NC}"
read -r DOMAIN_NAME

if [ -z "$DOMAIN_NAME" ]; then
    DOMAIN_NAME="_"
    echo -e "${YELLOW}Will use server IP for access${NC}"
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

# Enable site
sudo ln -sf /etc/nginx/sites-available/gemini-rag /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

echo -e "${GREEN}✓ Nginx configured${NC}"

# Completion
echo ""
echo "========================================="
echo -e "${GREEN}✓ Deployment Complete!${NC}"
echo "========================================="
echo ""
echo "Access URL:"
if [ "$DOMAIN_NAME" = "_" ]; then
    SERVER_IP=$(curl -s ifconfig.me)
    echo -e "  ${GREEN}http://$SERVER_IP${NC}"
else
    echo -e "  ${GREEN}http://$DOMAIN_NAME${NC}"
fi
echo ""
echo "Useful commands:"
echo "  Check status: sudo systemctl status gemini-rag"
echo "  View logs:    sudo journalctl -u gemini-rag -f"
echo "  Restart:      sudo systemctl restart gemini-rag"
echo "  Stop:         sudo systemctl stop gemini-rag"
echo ""
echo "Next steps:"
echo "  1. Visit the URL above"
echo "  2. Upload files and index"
echo "  3. Start using!"
echo ""
