# Quick Start Guide - Demo Files Ready!

## 🎯 You Now Have Demo Files Ready to Use!

I've created sample research documents and data files in the `demo_data/` directory that you can use immediately to test the RAG system.

## 📁 What's Included

### Text Documents (Ready to Use!)
- **lenr_overview_2024.txt** - Comprehensive LENR overview with citations
- **experimental_methods.txt** - Detailed experimental procedures
- **theoretical_models.txt** - Various theoretical frameworks
- **recent_developments.txt** - Latest research findings (2020-2024)

### Excel Files (Need to Generate)
Run this command to create the Excel files:
```bash
python demo_data/create_sample_files.py
```

This creates:
- **experimental_results.xlsx** - Lab experiment data with results
- **temperature_pressure_data.xlsx** - Time series measurements
- **materials_database.xlsx** - Materials properties and characteristics
- **publication_timeline.xlsx** - Research publication history

## 🚀 Getting Started (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs everything needed including:
- Google Gemini API client
- Streamlit for web UI
- Pandas/OpenPyxl for Excel
- PDF viewing tools

### Step 2: Set Your API Key

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_key_here
```

Get your free API key at: https://aistudio.google.com/app/apikey

### Step 3A: Use the Web Interface (Recommended)

```bash
streamlit run web_ui/app.py
```

Then:
1. **Create a Store** in the sidebar
2. **Upload Documents** from `demo_data/` folder
3. **Ask Questions** like:
   - "What are the main experimental methods in LENR?"
   - "Who discovered cold fusion and when?"
   - "What were the highest experiment yields?"
   - "Compare the different theoretical models"

### Step 3B: Or Use Python Scripts

```python
from src.rag.gemini_rag import GeminiRAG

# Initialize
rag = GeminiRAG()
store = rag.create_store("my-demo-store")

# Upload documents
rag.upload_file("demo_data/lenr_overview_2024.txt", store)
rag.upload_file("demo_data/experimental_methods.txt", store)

# Upload Excel (after generating)
rag.upload_excel("demo_data/experimental_results.xlsx", store)

# Query
response = rag.query(
    "What experimental methods are used in LENR research?",
    store
)

print(response["answer"])
for i, citation in enumerate(response["citations"], 1):
    print(f"[{i}] {citation['title']}")
```

## 💡 Sample Questions to Try

### General Research Questions
- "What is LENR and how does it work?"
- "Who were the pioneer researchers in cold fusion?"
- "What are the current challenges in LENR research?"
- "Explain the Fleischmann-Pons experiment"

### Experimental Questions
- "What are the three main experimental methods?"
- "What materials are used as cathodes?"
- "How is excess heat measured?"
- "What safety precautions are necessary?"

### Theoretical Questions
- "What is the lattice-assisted nuclear reaction model?"
- "Compare the Widom-Larsen theory to other models"
- "Why don't LENR experiments produce dangerous radiation?"
- "What role does electron screening play?"

### Data Questions (from Excel files)
- "What was the highest excess heat recorded?"
- "Which researcher conducted the most experiments?"
- "How does temperature affect reaction yield?"
- "What is the average experiment duration?"
- "Which materials are most cost-effective?"

### Recent Developments
- "What improvements in reproducibility have occurred?"
- "What commercial products are being developed?"
- "Which countries are investing in LENR research?"
- "What are potential applications for LENR?"

## 🎨 Features You'll See

### Interactive Citations
- Numbered references like **[1], [2], [3]**
- Click to jump to full source details
- View excerpts from original documents
- See metadata (author, date, category)

### Source Preview
- Expandable full text excerpts
- Highlighted relevant passages
- Document titles and locations
- Direct links to open files

### Query History
- See previous questions
- Review past answers
- Access historical citations
- Export results

## 📊 What the Demo Data Contains

### LENR Overview (11 KB)
- Introduction to LENR
- Historical timeline (1989-2024)
- Key researchers and discoveries
- 8 peer-reviewed references

### Experimental Methods (12 KB)
- Electrolysis procedures
- Gas loading techniques
- Calorimetry methods
- Safety protocols
- Materials specifications

### Theoretical Models (12 KB)
- Lattice-assisted reactions
- Electron screening
- Neutron exchange models
- Widom-Larsen theory
- Model comparisons

### Recent Developments (13 KB)
- 2020-2024 progress
- Commercialization efforts
- International collaborations
- Investment trends
- Future outlook

### Excel Data (Generated)
- 10 experiments with detailed parameters
- Temperature and pressure time series
- Materials database with 8 entries
- Publication timeline spanning 35 years

## 🔧 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "GOOGLE_API_KEY not found"
Make sure you created `.env` file with your API key

### Excel files don't exist
Run: `python demo_data/create_sample_files.py`

### Web UI won't start
Check that Streamlit is installed: `pip install streamlit`

## 📚 Next Steps

1. **Try the examples** with the demo data
2. **Add your own files** to the system
3. **Experiment with queries** to see citations
4. **Adjust settings** (temperature, model) for different results
5. **Explore the code** in `src/` to understand how it works

## 🌟 Pro Tips

1. **Lower temperature** (0.1-0.3) for factual queries
2. **Higher temperature** (0.7-0.9) for creative analysis
3. **Use specific questions** for better citations
4. **Upload related documents together** for better context
5. **Check citations** to verify answer accuracy

## 📖 More Information

- **Web UI Guide**: `web_ui/README.md`
- **Full Documentation**: `README.md`
- **Usage Details**: `USAGE.md`
- **Demo Data Info**: `demo_data/README.md`

## 🎉 Ready to Go!

You now have everything needed to test a full RAG system with:
- ✅ Sample research documents
- ✅ Excel data files
- ✅ Interactive web interface
- ✅ Citation tracking
- ✅ Complete documentation

Start with: `streamlit run web_ui/app.py`

Happy querying! 🚀
