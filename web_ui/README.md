# Interactive Web UI with Citations

A Streamlit-based web interface for the LENR RAG system featuring interactive, clickable citations similar to OpenEvidence.

## Features

- 🔍 **Interactive Search**: Ask questions about your uploaded documents
- 📚 **Clickable Citations**: References with numbered citations in the text
- 📄 **Source Preview**: View excerpts from source documents
- 📊 **Document Management**: Upload and organize documents in stores
- 💾 **Query History**: Keep track of previous searches
- 🎨 **Clean Interface**: Modern, responsive design

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install web UI dependencies specifically
pip install streamlit pymupdf markdown
```

## Quick Start

1. **Set up your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

2. **Run the web interface:**
   ```bash
   streamlit run web_ui/app.py
   ```

3. **Access the interface:**
   - Opens automatically in your browser at `http://localhost:8501`

## Usage

### 1. Create or Select a Store

- Use the sidebar to create a new document store or select an existing one
- Stores organize your documents into separate collections

### 2. Upload Documents

- Click "📤 Upload Documents" in the sidebar
- Supports: PDF, TXT, MD, DOCX, XLSX, XLS
- Files are automatically indexed for semantic search

### 3. Ask Questions

- Type your question in the main text area
- Click "🔍 Search" to query your documents
- Get answers with numbered citations

### 4. Explore Citations

- Citations appear as **[1], [2], [3]** in the answer
- Click on citation numbers to jump to the reference
- View full excerpts by expanding reference items
- Access source documents through provided links

## Interface Sections

### Sidebar

- **Document Store**: Create/select stores
- **Upload Documents**: Add files to the current store
- **Query Settings**: Adjust model and temperature

### Main Area

- **Query Input**: Ask your questions here
- **Answer**: Generated response with inline citations
- **References**: Detailed list of sources with:
  - Citation number
  - Document title
  - Excerpt preview
  - Metadata (author, date, etc.)
  - Link to source

### Query History

- View previous queries
- Access past answers and citations
- Clear history with one click

## Citation Features

### Numbered References

Answers include numbered citations like research papers:
```
LENR experiments typically operate at room temperature [1].
Various methods have been explored [2-4].
```

### Interactive References

Each reference includes:
- **Number**: [1], [2], [3]...
- **Title**: Document or source name
- **Preview**: Text excerpt (first 300 characters)
- **Full Text**: Expandable full excerpt
- **Metadata**: File info, categories, dates
- **Source Link**: Click to open original document

### Citation Navigation

- Click citation numbers to scroll to reference
- References are highlighted when selected
- Back navigation to return to text

## Query Types

### Document Questions

```
What are the main findings about LENR?
Who conducted early experiments in this field?
What experimental methods are described?
```

### Excel Data Questions

```
What were the total sales in Q1?
Which experiment had the highest yield?
Compare the performance across regions.
```

### Analytical Questions

```
Summarize the key conclusions from all papers
Compare different theoretical models
What are the research trends over time?
```

## Advanced Features

### Model Selection

- **gemini-2.5-flash**: Fast, efficient (recommended)
- **gemini-2.5-pro**: More powerful, detailed analysis

### Temperature Control

- **0.0-0.3**: Precise, factual (good for data queries)
- **0.4-0.7**: Balanced creativity and accuracy
- **0.8-1.0**: More creative, exploratory

### Metadata Filtering

Upload documents with metadata:
- Category
- Date/Year
- Author
- Topic
- Custom tags

## Tips for Best Results

1. **Be Specific**: "What were the sales for Product A in March?" vs. "Tell me about sales"

2. **Use Context**: Reference specific documents or time periods

3. **Multiple Queries**: Ask follow-up questions to drill deeper

4. **Check Citations**: Always review the source excerpts to verify answers

5. **Organize Stores**: Use separate stores for different topics/projects

## Troubleshooting

### "RAG system not initialized"
- Check that GOOGLE_API_KEY is set in .env
- Verify API key is valid at https://aistudio.google.com/app/apikey

### "No stores found"
- Create a new store using the sidebar
- Check that you're connected to the API

### Upload errors
- Verify file format is supported
- Check file size (max 100 MB)
- Ensure store is selected

### No citations in response
- The model may not have found relevant sources
- Try rephrasing your question
- Upload more relevant documents

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Submit query
- `Esc`: Clear focus
- `Ctrl/Cmd + K`: Focus search

## Customization

### Styling

Edit CSS in `web_ui/app.py`:
```python
st.markdown("""
<style>
    .citation-link { ... }
    .reference-item { ... }
</style>
""", unsafe_allow_html=True)
```

### Layout

Modify page configuration:
```python
st.set_page_config(
    page_title="Your Title",
    layout="wide",  # or "centered"
    ...
)
```

## Deployment

### Local Network

```bash
streamlit run web_ui/app.py --server.address 0.0.0.0 --server.port 8501
```

### Streamlit Cloud

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add GOOGLE_API_KEY to secrets
4. Deploy!

### Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "web_ui/app.py"]
```

## Examples

See `examples/` directory for:
- `basic_usage.py`: Command-line RAG usage
- `excel_usage.py`: Excel file integration
- `web_ui/app.py`: This interactive interface

## Architecture

```
User Query
    ↓
Streamlit Interface
    ↓
GeminiRAG
    ↓
Google File Search API
    ↓
Citation Formatter
    ↓
Interactive Display
```

## Support

- GitHub Issues: Report bugs or request features
- Documentation: See main README.md and USAGE.md
- API Docs: Google Gemini API documentation

## License

MIT License - See LICENSE file
