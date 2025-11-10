# Working with Local Files and Updating the RAG System

Guide for managing local files and keeping your RAG system synchronized.

---

## Overview

This guide shows you how to:
1. Keep your files locally on your computer
2. Upload them to the RAG system
3. Update the system when files change
4. Manage multiple versions

---

## Setup: Organize Your Local Files

### Step 1: Create a Local Folder

Create a dedicated folder for your files:

```bash
# Navigate to the project
cd LENR-Google

# Create a folder for your local files
mkdir my_local_files

# Create subfolders for organization
mkdir my_local_files/research
mkdir my_local_files/data
mkdir my_local_files/notes
mkdir my_local_files/reports
```

Your structure:
```
LENR-Google/
├── my_local_files/          ← Your local files here
│   ├── research/
│   │   ├── paper1.pdf
│   │   └── paper2.pdf
│   ├── data/
│   │   ├── experiments.xlsx
│   │   └── results.xlsx
│   ├── notes/
│   │   └── meeting_notes.txt
│   └── reports/
│       └── monthly_report.pdf
├── demo_data/               ← Demo files (already there)
└── web_ui/
    └── app.py
```

### Step 2: Add Your Files

Copy or move your files to the local folder:

```bash
# Copy files from Desktop
cp ~/Desktop/*.pdf my_local_files/research/

# Copy Excel files from Documents
cp ~/Documents/*.xlsx my_local_files/data/

# Copy from Downloads
cp ~/Downloads/*.txt my_local_files/notes/
```

**Your files stay local** - they won't be uploaded until you explicitly do it.

---

## Upload Local Files to RAG System

### Method 1: Upload All Files (Initial Setup)

Create a script to upload everything:

**File: `upload_local_files.py`**

```python
"""Upload all local files to RAG system."""

from pathlib import Path
from src.rag.gemini_rag import GeminiRAG
from datetime import datetime

def upload_all_local_files():
    """Upload all files from my_local_files/ to RAG."""

    # Initialize
    rag = GeminiRAG()

    # Create or use existing store
    store_name = rag.create_store("local-files-store")
    print(f"Using store: {store_name}\n")

    # Define local directory
    local_dir = Path("my_local_files")

    if not local_dir.exists():
        print("❌ my_local_files/ directory not found!")
        print("Create it first: mkdir my_local_files")
        return

    # Track uploads
    uploaded = []
    failed = []

    # Upload all files
    for file_path in local_dir.rglob("*"):
        if not file_path.is_file():
            continue

        # Determine file type
        suffix = file_path.suffix.lower()

        # Get relative path for metadata
        relative_path = file_path.relative_to(local_dir)
        category = relative_path.parts[0] if len(relative_path.parts) > 1 else "general"

        try:
            # Metadata
            metadata = {
                "category": category,
                "filename": file_path.name,
                "upload_date": datetime.now().strftime("%Y-%m-%d"),
                "local_path": str(file_path)
            }

            # Upload based on file type
            if suffix in ['.xlsx', '.xls']:
                print(f"📊 Uploading Excel: {relative_path}")
                rag.upload_excel(
                    str(file_path),
                    store_name,
                    metadata=metadata,
                    conversion_format="markdown"
                )
                uploaded.append(file_path)

            elif suffix in ['.pdf', '.txt', '.md', '.docx', '.html']:
                print(f"📄 Uploading document: {relative_path}")
                rag.upload_file(
                    str(file_path),
                    store_name,
                    metadata=metadata
                )
                uploaded.append(file_path)

            else:
                print(f"⏭️  Skipping unsupported: {relative_path}")

        except Exception as e:
            print(f"❌ Error with {relative_path}: {e}")
            failed.append(file_path)

    # Summary
    print("\n" + "="*60)
    print("Upload Summary")
    print("="*60)
    print(f"✅ Uploaded: {len(uploaded)} files")
    print(f"❌ Failed: {len(failed)} files")

    if uploaded:
        print("\n📚 Uploaded files:")
        for f in uploaded[:10]:  # Show first 10
            print(f"   - {f.name}")
        if len(uploaded) > 10:
            print(f"   ... and {len(uploaded) - 10} more")

    if failed:
        print("\n❌ Failed files:")
        for f in failed:
            print(f"   - {f.name}")

    print(f"\n🏪 Store name: {store_name}")
    print("✓ Ready to query!")

    return store_name


if __name__ == "__main__":
    store = upload_all_local_files()

    if store:
        # Test query
        print("\n" + "="*60)
        print("Testing upload...")
        print("="*60)

        from src.rag.gemini_rag import GeminiRAG
        rag = GeminiRAG()

        response = rag.query(
            "What files have been uploaded? List the main topics.",
            store
        )

        print("\nAnswer:")
        print(response["answer"])
```

**Run it:**

```bash
python upload_local_files.py
```

### Method 2: Upload Specific Folders

Upload only certain categories:

**File: `upload_research.py`**

```python
"""Upload only research papers."""

from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
store = rag.create_store("research-papers")

# Upload only from research folder
research_dir = Path("my_local_files/research")

for pdf_file in research_dir.glob("*.pdf"):
    print(f"Uploading: {pdf_file.name}")
    rag.upload_file(
        pdf_file,
        store,
        metadata={
            "type": "research_paper",
            "category": "research"
        }
    )

print("✓ Research papers uploaded!")
```

### Method 3: Use Web UI

```bash
# 1. Start web interface
streamlit run web_ui/app.py

# 2. Create store

# 3. Click "Upload Documents"

# 4. Navigate to: LENR-Google/my_local_files/

# 5. Select files and upload
```

---

## Update When Files Change

### Scenario 1: File Content Changed

When you edit a file locally, you need to re-upload it:

**File: `update_file.py`**

```python
"""Update a specific file in the RAG system."""

from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

def update_file(local_file_path, store_name):
    """
    Re-upload a file that was changed locally.

    Note: This uploads a NEW version. The old version remains
    in the store unless you delete it.
    """

    rag = GeminiRAG()

    file_path = Path(local_file_path)

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    print(f"📤 Updating {file_path.name}...")

    # Add version metadata
    from datetime import datetime
    metadata = {
        "filename": file_path.name,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "latest"
    }

    try:
        if file_path.suffix in ['.xlsx', '.xls']:
            rag.upload_excel(file_path, store_name, metadata=metadata)
        else:
            rag.upload_file(file_path, store_name, metadata=metadata)

        print(f"✅ Updated: {file_path.name}")

    except Exception as e:
        print(f"❌ Error: {e}")


# Usage
if __name__ == "__main__":
    # Update a specific file
    update_file(
        "my_local_files/research/paper1.pdf",
        "local-files-store"
    )
```

### Scenario 2: Multiple Files Changed

Track and update changed files:

**File: `sync_changes.py`**

```python
"""Sync changed files to RAG system."""

import json
from pathlib import Path
from datetime import datetime
from src.rag.gemini_rag import GeminiRAG

def save_file_index():
    """Save current state of files."""
    local_dir = Path("my_local_files")
    index = {}

    for file_path in local_dir.rglob("*"):
        if file_path.is_file():
            index[str(file_path)] = {
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
                "name": file_path.name
            }

    with open(".file_index.json", "w") as f:
        json.dump(index, f, indent=2)

    print(f"✓ Indexed {len(index)} files")


def find_changed_files():
    """Find files that changed since last sync."""

    # Load previous index
    index_file = Path(".file_index.json")
    if not index_file.exists():
        print("No previous index found. Run save_file_index() first.")
        return []

    with open(index_file) as f:
        old_index = json.load(f)

    # Check current files
    local_dir = Path("my_local_files")
    changed = []
    new = []

    for file_path in local_dir.rglob("*"):
        if not file_path.is_file():
            continue

        file_str = str(file_path)
        current_mtime = file_path.stat().st_mtime

        if file_str not in old_index:
            new.append(file_path)
        elif current_mtime > old_index[file_str]["modified"]:
            changed.append(file_path)

    return changed, new


def sync_to_rag(store_name):
    """Upload changed and new files."""

    changed, new = find_changed_files()

    if not changed and not new:
        print("✓ No changes detected. All files up to date!")
        return

    print(f"\n📝 Found {len(changed)} changed files")
    print(f"📝 Found {len(new)} new files")
    print()

    rag = GeminiRAG()

    # Upload changed files
    for file_path in changed:
        print(f"🔄 Updating: {file_path.name}")
        try:
            metadata = {
                "status": "updated",
                "updated_at": datetime.now().isoformat()
            }

            if file_path.suffix in ['.xlsx', '.xls']:
                rag.upload_excel(file_path, store_name, metadata=metadata)
            else:
                rag.upload_file(file_path, store_name, metadata=metadata)

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Upload new files
    for file_path in new:
        print(f"➕ Adding: {file_path.name}")
        try:
            metadata = {
                "status": "new",
                "added_at": datetime.now().isoformat()
            }

            if file_path.suffix in ['.xlsx', '.xls']:
                rag.upload_excel(file_path, store_name, metadata=metadata)
            else:
                rag.upload_file(file_path, store_name, metadata=metadata)

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Update index
    save_file_index()

    print(f"\n✅ Sync complete!")


# Usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "init":
            print("Initializing file index...")
            save_file_index()

        elif command == "sync":
            store_name = sys.argv[2] if len(sys.argv) > 2 else "local-files-store"
            print(f"Syncing to store: {store_name}")
            sync_to_rag(store_name)

        else:
            print("Unknown command. Use: init or sync")
    else:
        print("Usage:")
        print("  python sync_changes.py init              # First time setup")
        print("  python sync_changes.py sync <store>      # Sync changes")
```

**Usage:**

```bash
# First time: Create index of current files
python sync_changes.py init

# Later: After editing files, sync changes
python sync_changes.py sync local-files-store
```

---

## Workflow: Daily Updates

### Daily Routine

1. **Edit your local files** (in `my_local_files/`)
   - Update Excel spreadsheets
   - Revise documents
   - Add new files

2. **Sync to RAG system**
   ```bash
   python sync_changes.py sync local-files-store
   ```

3. **Test queries**
   ```bash
   streamlit run web_ui/app.py
   # Ask questions to verify updates
   ```

### Weekly Routine

1. **Full re-upload** (ensures everything is current)
   ```bash
   python upload_local_files.py
   ```

2. **Test comprehensive queries**
   ```python
   from src.rag.gemini_rag import GeminiRAG

   rag = GeminiRAG()

   # Test across all documents
   response = rag.query(
       "Summarize all recent updates and findings",
       "local-files-store"
   )
   print(response["answer"])
   ```

---

## Managing Versions

### Keep Old Versions Locally

```bash
# Create versions folder
mkdir my_local_files/versions

# Before updating a file, save the old version
cp my_local_files/research/paper.pdf \
   my_local_files/versions/paper_v1_2024-01-15.pdf

# Edit the current version
# my_local_files/research/paper.pdf (current)

# Upload updated version
python update_file.py my_local_files/research/paper.pdf local-files-store
```

### Version Tracking Script

**File: `version_tracker.py`**

```python
"""Track file versions before updates."""

import shutil
from pathlib import Path
from datetime import datetime

def backup_file(file_path, backup_dir="my_local_files/versions"):
    """Create backup before updating."""

    file_path = Path(file_path)
    backup_dir = Path(backup_dir)
    backup_dir.mkdir(exist_ok=True)

    # Create version filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
    backup_path = backup_dir / backup_name

    # Copy file
    shutil.copy2(file_path, backup_path)

    print(f"✓ Backed up: {file_path.name} → {backup_name}")
    return backup_path


# Usage
if __name__ == "__main__":
    # Before editing, backup
    backup_file("my_local_files/research/paper.pdf")

    # Now safe to edit the original
    print("→ Now you can safely edit the file")
```

---

## Example: Complete Local File Workflow

### Setup (One Time)

```bash
# 1. Create local folder structure
mkdir -p my_local_files/{research,data,notes}

# 2. Add your files
cp ~/Desktop/*.pdf my_local_files/research/
cp ~/Documents/*.xlsx my_local_files/data/

# 3. Initial upload
python upload_local_files.py

# 4. Initialize sync tracking
python sync_changes.py init
```

### Daily Workflow

```bash
# Morning: Edit your files
# - Open my_local_files/data/results.xlsx
# - Update data
# - Save

# Upload changes
python sync_changes.py sync local-files-store

# Verify in web UI
streamlit run web_ui/app.py
# Ask: "What's the latest data?"
```

### Weekly Workflow

```bash
# Monday: Clean up and organize
# - Review my_local_files/
# - Archive old files to versions/
# - Add new files

# Full sync
python upload_local_files.py

# Generate report
python -c "
from src.rag.gemini_rag import GeminiRAG

rag = GeminiRAG()
response = rag.query(
    'Create a summary of all documents and data in the system',
    'local-files-store'
)

with open('weekly_summary.txt', 'w') as f:
    f.write(response['answer'])

print('✓ Weekly summary generated')
"
```

---

## Configuration File

Create a config for your local setup:

**File: `local_config.json`**

```json
{
  "local_files_dir": "my_local_files",
  "store_name": "local-files-store",
  "backup_dir": "my_local_files/versions",
  "folders": {
    "research": {
      "upload": true,
      "metadata": {
        "category": "research",
        "type": "paper"
      }
    },
    "data": {
      "upload": true,
      "metadata": {
        "category": "data",
        "type": "experimental"
      },
      "excel_format": "markdown"
    },
    "notes": {
      "upload": true,
      "metadata": {
        "category": "notes",
        "type": "documentation"
      }
    }
  },
  "auto_backup": true,
  "sync_on_change": false
}
```

**Use it:**

```python
"""Load config and use for uploads."""

import json
from pathlib import Path
from src.rag.gemini_rag import GeminiRAG

# Load config
with open("local_config.json") as f:
    config = json.load(f)

rag = GeminiRAG()
local_dir = Path(config["local_files_dir"])
store_name = config["store_name"]

# Upload based on config
for folder_name, folder_config in config["folders"].items():
    if not folder_config["upload"]:
        continue

    folder_path = local_dir / folder_name

    for file_path in folder_path.glob("*"):
        if file_path.is_file():
            metadata = folder_config["metadata"].copy()
            metadata["filename"] = file_path.name

            if file_path.suffix in ['.xlsx', '.xls']:
                excel_format = folder_config.get("excel_format", "markdown")
                rag.upload_excel(
                    file_path,
                    store_name,
                    metadata=metadata,
                    conversion_format=excel_format
                )
            else:
                rag.upload_file(file_path, store_name, metadata=metadata)

            print(f"✓ Uploaded: {file_path.name}")
```

---

## Tips and Best Practices

### ✅ DO:

1. **Keep organized folders**
   ```
   my_local_files/
   ├── research/    (papers, articles)
   ├── data/        (Excel, CSV)
   ├── notes/       (meeting notes, ideas)
   └── reports/     (final reports)
   ```

2. **Use descriptive filenames**
   ```
   ✅ Smith_2024_LENR_Experiments.pdf
   ❌ doc1.pdf
   ```

3. **Backup before major changes**
   ```bash
   python version_tracker.py my_local_files/important.pdf
   ```

4. **Sync regularly**
   ```bash
   # Add to your morning routine
   python sync_changes.py sync local-files-store
   ```

5. **Test after uploads**
   ```python
   response = rag.query("What's new?", store)
   ```

### ❌ DON'T:

1. **Don't delete local files after upload**
   - Keep local copies
   - They're your source of truth

2. **Don't upload directly from Downloads**
   - First move to organized folder
   - Then upload

3. **Don't upload same file multiple times manually**
   - Use sync script instead
   - Prevents duplicates

4. **Don't skip backups for important files**
   - Create versions before major edits

---

## Troubleshooting

### "File already uploaded"

The system doesn't prevent duplicates. Each upload creates a new entry.

**Solution:** Use sync script which tracks what's uploaded.

### "Changes not reflected"

**Problem:** Old version still being retrieved

**Solution:**
1. Wait a few minutes (indexing takes time)
2. Create new store for major updates
3. Be specific in queries: "According to latest data..."

### "Too many files to track"

**Problem:** Hard to know what's uploaded

**Solution:** Use the sync tracking system:
```bash
python sync_changes.py init    # Creates index
python sync_changes.py sync    # Only uploads changes
```

---

## Summary

### Your Workflow:

1. **Keep files in:** `my_local_files/`
2. **Upload with:** `python upload_local_files.py`
3. **Sync changes:** `python sync_changes.py sync local-files-store`
4. **Query via:** `streamlit run web_ui/app.py`

### Key Scripts:

- `upload_local_files.py` - Upload all files
- `sync_changes.py` - Track and sync changes
- `update_file.py` - Update specific file
- `version_tracker.py` - Backup before edits

---

**Your files stay local, the RAG system stays updated!** 🎯
