# My Local Files

This folder is for YOUR documents that you want to upload to the RAG system.

## Quick Start

1. **Add your files here:**
   ```bash
   # Copy your files to this folder
   cp ~/Desktop/your_file.pdf research/
   cp ~/Documents/data.xlsx data/
   ```

2. **Upload all files to RAG:**
   ```bash
   # From the main directory (LENR-Google/)
   python upload_local_files.py
   ```

3. **Track changes and sync updates:**
   ```bash
   python sync_changes.py init     # First time only
   python sync_changes.py sync     # Upload changes
   ```

## Folder Structure

- **research/** - Research papers, articles, PDFs
- **data/** - Excel files, CSV files, datasets
- **notes/** - Text notes, meeting notes, documentation
- **papers/** - Academic papers, publications

Feel free to create your own subfolders!

## Supported File Types

✅ PDF (`.pdf`)
✅ Excel (`.xlsx`, `.xls`)
✅ Text (`.txt`)
✅ Markdown (`.md`)
✅ Word (`.docx`)
✅ HTML (`.html`)

## Tips

- Files are automatically organized by folder
- Folder names become categories in the RAG system
- Keep files under 100 MB each
- You can have unlimited subfolders
