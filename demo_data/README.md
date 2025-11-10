# Demo Data Files

This directory contains sample documents and Excel files for testing the RAG system.

## Contents

### Research Papers (Text Format)
- `lenr_overview_2024.txt` - Comprehensive LENR overview
- `experimental_methods.txt` - Detailed experimental procedures
- `theoretical_models.txt` - Various theoretical frameworks
- `recent_developments.txt` - Latest research findings

### Excel Data Files
- `experimental_results.xlsx` - Laboratory experiment data
- `temperature_pressure_data.xlsx` - Environmental condition measurements
- `materials_database.xlsx` - Materials and their properties
- `publication_timeline.xlsx` - Research publication history

## How to Use

### Option 1: Web UI Upload

1. Launch the web interface:
   ```bash
   streamlit run web_ui/app.py
   ```

2. In the sidebar:
   - Create or select a store
   - Click "📤 Upload Documents"
   - Select files from this `demo_data` directory
   - Click "Upload to Store"

3. Query examples:
   - "What are the main experimental methods?"
   - "What were the highest yields in the experiments?"
   - "Who were the pioneer researchers in LENR?"
   - "What materials are commonly used?"

### Option 2: Python Script

```python
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("demo-store")

# Upload text documents
rag.upload_file("demo_data/lenr_overview_2024.txt", store)
rag.upload_file("demo_data/experimental_methods.txt", store)

# Upload Excel files
rag.upload_excel("demo_data/experimental_results.xlsx", store)
rag.upload_excel("demo_data/temperature_pressure_data.xlsx", store)

# Query
response = rag.query("What experimental methods are used?", store)
print(response["answer"])
```

### Option 3: Batch Upload

```python
from pathlib import Path

files = list(Path("demo_data").glob("*.txt"))
excel_files = list(Path("demo_data").glob("*.xlsx"))

# Upload all text files
for file in files:
    rag.upload_file(file, store)

# Upload all Excel files
for file in excel_files:
    rag.upload_excel(file, store)
```

## Sample Queries

Once uploaded, try these questions:

### General Research Questions
- "What is LENR and how does it work?"
- "Who discovered cold fusion?"
- "What are the current challenges in LENR research?"

### Experimental Questions
- "What experimental methods are most commonly used?"
- "What temperature ranges are typical for LENR experiments?"
- "Which materials show the best results?"

### Data-Specific Questions (from Excel)
- "What was the highest reaction yield recorded?"
- "How does temperature affect the reaction rate?"
- "Which experiment had the longest duration?"
- "Compare the results across different materials"

### Citation-Focused Questions
- "Cite sources for the Fleischmann-Pons experiment"
- "What publications discuss palladium electrodes?"
- "Find all references to deuterium loading"

## File Descriptions

### lenr_overview_2024.txt
Comprehensive overview covering history, principles, and current status of LENR research.

### experimental_methods.txt
Detailed descriptions of experimental procedures including electrolysis, gas loading, and plasma methods.

### theoretical_models.txt
Discussion of various theoretical frameworks proposed to explain LENR phenomena.

### recent_developments.txt
Latest findings and developments in the field from recent years.

### experimental_results.xlsx
Contains:
- Experiment ID, Date, Researcher
- Materials used, Conditions
- Measurements and Yields
- Observations

### temperature_pressure_data.xlsx
Environmental condition data:
- Time series measurements
- Temperature and pressure readings
- Correlation with reaction rates

### materials_database.xlsx
Material properties:
- Material names and compositions
- Physical properties
- Performance in LENR experiments
- Cost and availability

### publication_timeline.xlsx
Research history:
- Publication dates
- Authors and institutions
- Key findings
- Citation counts

## Adding Your Own Files

Simply add your files to this directory and upload them using the web UI or Python scripts. The system supports:

- **Documents**: PDF, TXT, MD, DOCX, HTML
- **Spreadsheets**: XLSX, XLS
- **Maximum size**: 100 MB per file

## Tips

1. **Organize by topic**: Upload related documents together
2. **Use metadata**: Add categories, dates, authors when uploading
3. **Test queries**: Start with simple questions, then get more specific
4. **Check citations**: Review the source excerpts to verify accuracy
5. **Experiment**: Try different temperature settings for different query types
