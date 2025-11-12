#!/bin/bash

# Enterprise RAG Setup Script
# Automated setup for the best RAG system

echo "============================================================"
echo "Enterprise RAG System Setup"
echo "The Best RAG Solution for Your 7000+ Files"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Python version
echo "Step 1: Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 9) else 1)'; then
    echo -e "   ${GREEN}✅ Python version OK${NC}"
else
    echo -e "   ${RED}❌ Python 3.9+ required${NC}"
    exit 1
fi
echo ""

# Step 2: Create virtual environment (optional but recommended)
echo "Step 2: Setting up virtual environment (optional)..."
read -p "   Create virtual environment? (recommended) [Y/n]: " create_venv
if [[ "$create_venv" != "n" && "$create_venv" != "N" ]]; then
    if [ ! -d "venv" ]; then
        echo "   Creating virtual environment..."
        python3 -m venv venv
        echo -e "   ${GREEN}✅ Virtual environment created${NC}"
    else
        echo -e "   ${YELLOW}Virtual environment already exists${NC}"
    fi

    echo "   To activate later, run: source venv/bin/activate"
    source venv/bin/activate 2>/dev/null || . venv/bin/activate
    echo -e "   ${GREEN}✅ Virtual environment activated${NC}"
fi
echo ""

# Step 3: Install dependencies
echo "Step 3: Installing dependencies..."
echo "   This may take 2-5 minutes..."
pip install -r requirements_enterprise.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ All dependencies installed${NC}"
else
    echo -e "   ${RED}❌ Installation failed${NC}"
    exit 1
fi
echo ""

# Step 4: Check for .env file
echo "Step 4: Checking API keys configuration..."
if [ ! -f ".env" ]; then
    echo -e "   ${YELLOW}⚠️  No .env file found${NC}"
    echo "   Creating template .env file..."

    cat > .env << 'EOF'
# Enterprise RAG API Keys
# Get your keys from:
# - OpenAI: https://platform.openai.com/api-keys
# - Pinecone: https://www.pinecone.io/
# - Cohere: https://cohere.com/
# - Anthropic: https://console.anthropic.com/

OPENAI_API_KEY=sk-proj-your-key-here
PINECONE_API_KEY=your-pinecone-key-here
COHERE_API_KEY=your-cohere-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional: Custom index name
# PINECONE_INDEX_NAME=my-custom-index
EOF

    echo -e "   ${GREEN}✅ Template .env created${NC}"
    echo ""
    echo -e "   ${YELLOW}ACTION REQUIRED:${NC}"
    echo "   1. Edit .env file with your API keys"
    echo "   2. Get keys from:"
    echo "      - OpenAI: https://platform.openai.com/api-keys"
    echo "      - Pinecone: https://www.pinecone.io/"
    echo "      - Cohere: https://cohere.com/"
    echo "      - Anthropic: https://console.anthropic.com/"
    echo ""

    read -p "   Press Enter when you've added your API keys..."
else
    echo -e "   ${GREEN}✅ .env file found${NC}"
fi
echo ""

# Step 5: Test the system
echo "Step 5: Testing the system..."
echo "   Running test script..."
python examples/test_enterprise_rag.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
    echo "============================================================"
    echo ""
    echo "Your Enterprise RAG system is ready to use!"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Index your 7000 files:"
    echo "   python index_my_files.py"
    echo ""
    echo "2. Start the web interface:"
    echo "   streamlit run streamlit_enterprise.py"
    echo ""
    echo "3. Or use Python directly:"
    echo "   python"
    echo "   >>> from src.rag.enterprise_rag import EnterpriseRAG"
    echo "   >>> rag = EnterpriseRAG(index_name='my-7000-files')"
    echo "   >>> result = rag.query('Your question')"
    echo ""
    echo "Documentation:"
    echo "   - Quick Start: ENTERPRISE_QUICK_START.md"
    echo "   - Full Guide: ENTERPRISE_GUIDE.md"
    echo ""
    echo "🚀 Enjoy the best RAG system!"
    echo ""
else
    echo ""
    echo "============================================================"
    echo -e "${RED}❌ SETUP FAILED${NC}"
    echo "============================================================"
    echo ""
    echo "Please check:"
    echo "1. API keys in .env are correct"
    echo "2. All dependencies installed correctly"
    echo "3. Internet connection is working"
    echo ""
    echo "For help, see ENTERPRISE_GUIDE.md"
    echo ""
    exit 1
fi
