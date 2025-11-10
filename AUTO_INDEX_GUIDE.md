# Auto-Index Folder - Quick Guide

Automatically upload and sync your local files to the RAG system!

---

## What It Does

The `auto_index_folder.py` script automatically:
- Scans the `my_local_files/` folder
- Uploads all your documents to the RAG system
- Tracks changes and only uploads new/modified files
- Can run continuously to auto-sync as you add files

---

## Quick Start (3 Steps)

### Step 1: Add Your Files

```bash
# Copy your files to my_local_files/
cp ~/Desktop/*.pdf my_local_files/research/
cp ~/Documents/*.xlsx my_local_files/data/
cp ~/Downloads/*.txt my_local_files/notes/
```

Or just drag and drop files into `my_local_files/` using your file manager!

### Step 2: Initialize (First Time Only)

```bash
python auto_index_folder.py init
```

This will:
- Create the RAG store
- Upload all files from `my_local_files/`
- Create tracking index

### Step 3: Query Your Files!

```bash
# Start the web UI
streamlit run web_ui/app.py

# Or use Python
python -c "from src.rag.gemini_rag import GeminiRAG; \
rag = GeminiRAG(); \
print(rag.query('What files do I have?', 'local-files-store')['answer'])"
```

---

## Three Usage Modes

### Mode 1: One-Time Upload (init)

Upload all files once:

```bash
python auto_index_folder.py init
```

**Use when:**
- First time setup
- You have many files to upload at once

### Mode 2: Manual Sync (sync)

Check for changes and upload:

```bash
python auto_index_folder.py sync
```

**Use when:**
- You've added/edited some files
- You want control over when to sync

### Mode 3: Auto-Watch (watch)

Continuously monitor and auto-upload:

```bash
# Check every 60 seconds (default)
python auto_index_folder.py watch

# Check every 30 seconds
python auto_index_folder.py watch 30

# Check every 5 minutes
python auto_index_folder.py watch 300
```

**Use when:**
- You're actively working on files
- You want automatic background sync
- Press Ctrl+C to stop

---

## Complete Workflow

### Daily Workflow

```bash
# Morning: Start auto-watch in background
python auto_index_folder.py watch &

# Work on your files all day...
# Files are automatically uploaded as you save them!

# Evening: Stop auto-watch
# Press Ctrl+C or: kill %1
```

### Manual Workflow

```bash
# 1. Add files to folder
cp ~/Desktop/new_paper.pdf my_local_files/research/

# 2. Sync manually
python auto_index_folder.py sync

# 3. Query
streamlit run web_ui/app.py
```

---

## Folder Structure

```
my_local_files/
├── README.md          # Usage instructions
├── research/          # Research papers, PDFs
├── data/              # Excel files, datasets
├── notes/             # Text notes, documentation
└── papers/            # Academic papers

Add your own folders:
├── experiments/
├── reports/
└── references/
```

---

## Supported File Types

The auto-indexer handles:

✅ **PDF** (`.pdf`) - Research papers, documents
✅ **Excel** (`.xlsx`, `.xls`) - Spreadsheets, data
✅ **Text** (`.txt`) - Plain text notes
✅ **Markdown** (`.md`) - Documentation
✅ **Word** (`.docx`) - Documents
✅ **HTML** (`.html`) - Web pages

**File size limit:** 100 MB per file

---

## Examples

### Example 1: Upload Research Papers

```bash
# Create research folder
mkdir -p my_local_files/research

# Copy papers
cp ~/Desktop/LENR_Research/*.pdf my_local_files/research/

# Upload all
python auto_index_folder.py init

# Files are now searchable!
```

### Example 2: Sync After Editing

```bash
# Edit a file
nano my_local_files/notes/experiment_log.txt

# Sync changes
python auto_index_folder.py sync

# Only the changed file is uploaded
```

### Example 3: Continuous Auto-Sync

```bash
# Start watch mode
python auto_index_folder.py watch 60

# In another terminal, add files
cp ~/Downloads/new_data.xlsx my_local_files/data/

# Auto-indexer detects and uploads automatically!
# Output shows:
# [2025-01-15 14:23:10] Changes detected!
#   ➕ New: new_data.xlsx... ✅
#   ✓ Synced at 2025-01-15 14:23:10
```

### Example 4: Organize by Category

```bash
# Create organized structure
mkdir -p my_local_files/{experiments,results,references}

# Add files
cp ~/Desktop/exp_*.xlsx my_local_files/experiments/
cp ~/Documents/results_*.pdf my_local_files/results/
cp ~/Downloads/papers/*.pdf my_local_files/references/

# Upload with automatic categorization
python auto_index_folder.py init

# Files are tagged with folder names as categories!
```

---

## How It Works

### Change Detection

The script tracks files using `.file_index.json`:

```json
{
  "my_local_files/research/paper.pdf": {
    "size": 2048576,
    "modified": 1705315200.0,
    "name": "paper.pdf"
  }
}
```

**When you run sync:**
1. Scans `my_local_files/`
2. Compares to `.file_index.json`
3. Finds new files (not in index)
4. Finds changed files (different modified time)
5. Uploads only new/changed files
6. Updates index

### Upload Process

**For each file:**
1. Detects file type (PDF, Excel, etc.)
2. Extracts category from folder name
3. Adds metadata (filename, date, category, path)
4. Uploads to RAG store
5. Tracks success/failure

---

## Commands Reference

### Initialize

```bash
python auto_index_folder.py init
```

- Creates RAG store if needed
- Scans all files in `my_local_files/`
- Uploads everything
- Creates tracking index

### Sync Once

```bash
python auto_index_folder.py sync
```

- Loads existing index
- Finds new/changed files
- Uploads only changes
- Updates index

### Watch Mode

```bash
python auto_index_folder.py watch [interval]
```

- Runs continuously
- Checks every `interval` seconds (default: 60)
- Auto-uploads changes
- Press Ctrl+C to stop

### Help

```bash
python auto_index_folder.py
```

Shows usage instructions

---

## Output Examples

### Initialization Output

```
============================================================
Initializing Auto-Indexer
============================================================

✓ Store ready: local-files-store

📁 Found 5 files

📤 Uploading all files...

   research_paper.pdf... ✅
   experimental_data.xlsx... ✅
   notes.txt... ✅
   methods.md... ✅
   results.docx... ✅

============================================================
✅ Initialization Complete
============================================================
Uploaded: 5 files
Failed: 0 files

🏪 Store: local-files-store
📂 Watching: my_local_files/
```

### Sync Output

```
============================================================
Checking for Changes
============================================================

📝 Found 2 new files
📝 Found 1 changed files

➕ Uploading new files:

   new_paper.pdf... ✅
   additional_data.xlsx... ✅

🔄 Uploading changed files:

   notes.txt... ✅

============================================================
✅ Sync Complete
============================================================
```

### Watch Mode Output

```
============================================================
Auto-Indexer - Watch Mode
============================================================

📂 Watching: my_local_files/
🏪 Store: local-files-store
⏱️  Check interval: 60 seconds

Press Ctrl+C to stop

[2025-01-15 14:23:10] Changes detected!
   ➕ New: experiment_5.xlsx... ✅
   ✓ Synced at 2025-01-15 14:23:10

[2025-01-15 14:24:15] Changes detected!
   🔄 Changed: notes.txt... ✅
   ✓ Synced at 2025-01-15 14:24:15
```

---

## Troubleshooting

### "Folder not found"

**Problem:** `my_local_files/` doesn't exist

**Solution:**
```bash
mkdir -p my_local_files
python auto_index_folder.py init
```

### "Not initialized yet"

**Problem:** Trying to sync before init

**Solution:**
```bash
python auto_index_folder.py init
```

### "Folder is empty"

**Problem:** No files in `my_local_files/`

**Solution:**
```bash
# Add some files first
cp ~/Desktop/*.pdf my_local_files/
python auto_index_folder.py init
```

### File Not Uploading

**Possible causes:**
1. Unsupported file type
2. File too large (>100 MB)
3. Network issue

**Solution:**
```bash
# Check file
ls -lh my_local_files/yourfile.ext

# Check supported types in output
# If too large, split or compress
```

---

## Comparison: Three Scripts

| Feature | `upload_local_files.py` | `sync_changes.py` | `auto_index_folder.py` |
|---------|------------------------|-------------------|------------------------|
| **Upload all files** | ✅ Yes | ❌ No | ✅ Yes |
| **Track changes** | ❌ No | ✅ Yes | ✅ Yes |
| **Auto-watch** | ❌ No | ❌ No | ✅ Yes |
| **One script** | ✅ Yes | ❌ Needs init | ✅ Yes |
| **Best for** | One-time | Manual sync | Everything |

**Recommendation:** Use `auto_index_folder.py` - it combines all features!

---

## Integration with Web UI

After uploading files, use the web UI to query:

```bash
# Start web UI
streamlit run web_ui/app.py
```

**In the web UI:**
1. Select store: `local-files-store`
2. Ask questions about your files
3. Get answers with clickable citations
4. View source documents

---

## Advanced Usage

### Custom Store Name

Edit `auto_index_folder.py`:

```python
indexer = FolderAutoIndexer(
    folder_path="my_local_files",
    store_name="my-custom-store"  # Change this
)
```

### Custom Folder

```python
indexer = FolderAutoIndexer(
    folder_path="/Users/yourname/Documents/Research",  # Change this
    store_name="research-store"
)
```

### Run as Background Service

**Linux/Mac:**
```bash
# Start in background
nohup python auto_index_folder.py watch 300 > indexer.log 2>&1 &

# Check status
tail -f indexer.log

# Stop
pkill -f auto_index_folder
```

**Windows:**
```batch
# Create a scheduled task or use:
start /B python auto_index_folder.py watch 300
```

---

## Tips & Best Practices

### Organization

- Use descriptive folder names (they become categories)
- Group related files together
- Keep folder structure shallow (2-3 levels max)

### Performance

- Smaller files upload faster
- Watch mode with 60-300 second intervals is optimal
- Use `sync` for manual control, `watch` for automation

### Workflow

**For active work:**
```bash
python auto_index_folder.py watch 60  # Check every minute
```

**For occasional updates:**
```bash
python auto_index_folder.py sync  # Manual sync
```

**For batch uploads:**
```bash
python auto_index_folder.py init  # Upload everything
```

---

## Next Steps

1. **Add your files:**
   ```bash
   cp ~/Desktop/*.pdf my_local_files/
   ```

2. **Initialize:**
   ```bash
   python auto_index_folder.py init
   ```

3. **Query:**
   ```bash
   streamlit run web_ui/app.py
   ```

4. **Set up auto-sync:**
   ```bash
   python auto_index_folder.py watch 60
   ```

---

## See Also

- **LOCAL_FILES_GUIDE.md** - Comprehensive local file management
- **WHERE_TO_UPLOAD.md** - File upload locations and methods
- **HOW_TO_USE.md** - Complete system usage guide
- **TRAINING_GUIDE.md** - Adding documents to RAG

---

**Questions?** Check the other guides or the README!
