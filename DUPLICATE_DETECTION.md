# Duplicate Detection System

Automatic duplicate detection ensures you never index the same content twice.

---

## Storage Architecture

The system uses **dual storage** - both local and online:

### Local Storage (`.file_index.json`)

Stored on your computer in the project root:

```json
{
  "my_local_files/research/paper.pdf": {
    "size": 2048576,
    "modified": 1705315200.0,
    "name": "paper.pdf",
    "hash": "a7f2b9c1..."
  }
}
```

**What's stored locally:**
- File metadata (name, size, modification time)
- SHA256 content hash
- All files tracked (including duplicates)

**Purpose:**
- Fast change detection
- Duplicate identification
- No need to re-scan files
- Works offline

### Online Storage (Google File Search Store)

Stored in Google's cloud:

```
Google Cloud
├── File content and embeddings
├── Searchable text chunks
└── Metadata for retrieval
```

**What's stored online:**
- Actual file content
- Vector embeddings for semantic search
- Only unique files (duplicates excluded)

**Purpose:**
- Enable RAG queries from anywhere
- Semantic search capabilities
- Persistent knowledge base
- Cloud accessibility

### How They Work Together

```
Local Files                  Local Index              Online Store
───────────                  ────────────             ────────────
paper.pdf        ──scan──>   {metadata + hash}  ──upload──>  [RAG]
paper_copy.pdf   ──scan──>   {metadata + hash}  ──skip──>    [Not uploaded]
                             (duplicate detected)
```

**Flow:**
1. **Scan:** Read local files, calculate hashes
2. **Check:** Compare hashes in local index
3. **Upload:** Only upload unique content to cloud
4. **Track:** Store all files in local index

---

## How It Works

### Content-Based Detection

The system uses **SHA256 hashing** to detect duplicates based on file **content**, not filenames.

```
File 1: research/paper.pdf          Hash: abc123...
File 2: backup/paper_copy.pdf       Hash: abc123...  ← DUPLICATE!
File 3: research/different.pdf      Hash: xyz789...  ← UNIQUE
```

**Result:** Only Files 1 and 3 are uploaded. File 2 is skipped (duplicate content).

### Why Content-Based?

Traditional duplicate detection checks filenames:
- ❌ Misses copies with different names
- ❌ Misses files in different folders
- ❌ Can flag different files with same name

Our SHA256 hash approach:
- ✅ Detects identical content regardless of filename
- ✅ Detects identical content in different folders
- ✅ Ignores files with same name but different content
- ✅ Fast and efficient

---

## Features

### 1. Initial Upload (init)

When you first upload files, duplicates within the batch are detected:

```bash
python auto_index_folder.py init
```

**Output:**
```
📁 Found 10 files
🔍 Checking for duplicates...

📤 Uploading unique files...

   research_paper.pdf... ✅
   experiment_data.xlsx... ✅
   notes.txt... ✅
   paper_backup.pdf... ⏭️  Duplicate of research_paper.pdf
   data_copy.xlsx... ⏭️  Duplicate of experiment_data.xlsx

============================================================
✅ Initialization Complete
============================================================
✅ Uploaded: 3 files
⏭️  Skipped duplicates: 2 files
❌ Failed: 0 files
```

### 2. Sync Changes

When syncing updates, new duplicates are detected:

```bash
python auto_index_folder.py sync
```

**Scenario:** You add a file that has the same content as an already-indexed file.

**Output:**
```
============================================================
Checking for Changes
============================================================

📝 Found 2 new files
📝 Found 0 changed files
⏭️  Found 1 duplicate files (will skip)

⏭️  Skipping duplicate files:

   new_paper_copy.pdf → duplicate of research_paper.pdf

➕ Uploading new files:

   unique_document.pdf... ✅
```

### 3. Watch Mode

In watch mode, duplicates are automatically detected and skipped:

```bash
python auto_index_folder.py watch 60
```

**Output:**
```
[2025-01-15 14:23:10] Changes detected!
   ⏭️  Duplicate skipped: backup_file.pdf (same as original.pdf)
   ➕ New: new_unique_file.pdf... ✅
   ✓ Synced at 2025-01-15 14:23:10
```

---

## The Index File

All file information is stored in `.file_index.json` (local storage):

```json
{
  "my_local_files/research/paper.pdf": {
    "size": 2048576,
    "modified": 1705315200.0,
    "name": "paper.pdf",
    "hash": "a7f2b9c1e3d4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5"
  },
  "my_local_files/data/experiments.xlsx": {
    "size": 1024000,
    "modified": 1705315300.0,
    "name": "experiments.xlsx",
    "hash": "b8g3c0d2f4e5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6"
  }
}
```

**Key Information:**
- `size`: File size in bytes
- `modified`: Last modification timestamp
- `name`: Filename
- `hash`: SHA256 hash of file content (for duplicate detection)

---

## Use Cases

### Case 1: Multiple Copies of Same File

**Scenario:** You have backups of the same file in different folders.

```
my_local_files/
├── research/paper.pdf          (original)
├── backup/paper.pdf            (exact copy)
└── archive/paper_v1.pdf        (exact copy)
```

**Result:**
- Only `research/paper.pdf` is uploaded
- `backup/paper.pdf` and `archive/paper_v1.pdf` are skipped
- All three tracked in index, but only one in RAG

### Case 2: Renamed Files

**Scenario:** You rename a file but content stays the same.

```
Before: my_local_files/report_draft.pdf
After:  my_local_files/report_final.pdf  (same content, new name)
```

**Result:**
- `report_final.pdf` detected as duplicate of `report_draft.pdf`
- Not uploaded again
- Only name updated in index

### Case 3: Similar Names, Different Content

**Scenario:** Files with similar names but different content.

```
my_local_files/
├── experiment_v1.pdf      Hash: abc123...
└── experiment_v2.pdf      Hash: xyz789...  (different content)
```

**Result:**
- Both files uploaded (different hashes)
- No duplicates detected
- Both indexed separately

### Case 4: Updated File Content

**Scenario:** You edit a file's content.

```
Before: my_local_files/notes.txt      Hash: abc123...
After:  my_local_files/notes.txt      Hash: def456...  (content changed)
```

**Result:**
- File detected as changed (different hash)
- Updated version uploaded to RAG
- Index updated with new hash

---

## Benefits

### Storage Efficiency
- No duplicate content stored in RAG
- Saves storage space
- Reduces indexing costs

### Performance
- Faster queries (smaller index)
- No redundant search results
- Better relevance in answers

### Organization
- Clear tracking of unique files
- Easy identification of duplicates
- Maintains clean knowledge base

---

## Examples

### Example 1: Organize Files Without Duplicates

```bash
# You have files scattered across folders
my_local_files/
├── downloads/paper.pdf
├── desktop/paper.pdf        (same file)
└── documents/paper.pdf      (same file)

# Initialize
python auto_index_folder.py init

# Output
📁 Found 3 files
🔍 Checking for duplicates...

📤 Uploading unique files...
   paper.pdf... ✅
   paper.pdf... ⏭️  Duplicate of paper.pdf
   paper.pdf... ⏭️  Duplicate of paper.pdf

✅ Uploaded: 1 files
⏭️  Skipped duplicates: 2 files
```

### Example 2: Add Backup, Skip Duplicate

```bash
# Existing file
my_local_files/research/important.pdf  (already indexed)

# Add backup
cp my_local_files/research/important.pdf my_local_files/backup/

# Sync
python auto_index_folder.py sync

# Output
📝 Found 1 new files
⏭️  Found 1 duplicate files (will skip)

⏭️  Skipping duplicate files:
   important.pdf → duplicate of important.pdf

# Backup tracked but not uploaded (duplicate)
```

### Example 3: Update File Content

```bash
# Edit a file
echo "New content" >> my_local_files/notes.txt

# Sync
python auto_index_folder.py sync

# Output
📝 Found 0 new files
📝 Found 1 changed files

🔄 Uploading changed files:
   notes.txt... ✅

# Updated content indexed with new hash
```

---

## Technical Details

### Hash Calculation

SHA256 hash is calculated by reading file in 4KB chunks:

```python
def calculate_file_hash(self, file_path):
    """Calculate SHA256 hash of file content."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
```

**Characteristics:**
- Fast for large files (chunked reading)
- Deterministic (same content = same hash)
- Collision-resistant (virtually impossible for different files to have same hash)

### Duplicate Detection Logic

**During initialization:**
1. Scan all files in folder
2. Calculate hash for each file
3. Track seen hashes in memory
4. Skip files with already-seen hashes
5. Store all files in index (including duplicates)

**During sync:**
1. Load existing index (with hashes)
2. Scan current files, calculate hashes
3. For new files: check if hash exists in index
4. For changed files: check if new hash matches other files
5. Skip files with duplicate hashes
6. Update index with new/changed files

---

## Index Management

### View Index

```bash
cat .file_index.json | python -m json.tool
```

### Check Specific File Hash

```bash
cat .file_index.json | python -m json.tool | grep -A 5 "your_file.pdf"
```

### Find Duplicates Manually

```python
import json
from collections import defaultdict

# Load index
with open('.file_index.json') as f:
    index = json.load(f)

# Group by hash
by_hash = defaultdict(list)
for path, info in index.items():
    by_hash[info['hash']].append(path)

# Find duplicates
for hash_val, paths in by_hash.items():
    if len(paths) > 1:
        print(f"Duplicate files (hash: {hash_val[:8]}...):")
        for path in paths:
            print(f"  - {path}")
```

### Reset Index

```bash
# Delete index (forces re-initialization)
rm .file_index.json

# Re-initialize
python auto_index_folder.py init
```

---

## Troubleshooting

### "Duplicate detected but files are different"

**Possible causes:**
1. Files have identical content but different metadata
2. Only content is compared, not metadata

**Solution:**
- This is expected behavior
- Only content matters for RAG indexing
- Metadata differences don't affect search

### "Different files detected as duplicate"

**Very unlikely** - SHA256 collision probability is negligible.

**If this happens:**
1. Verify files are actually different: `diff file1 file2`
2. Check file hashes manually: `sha256sum file1 file2`
3. Report as bug if truly different

### "Updated file not detected"

**Possible causes:**
1. File modification time not updated
2. Content actually unchanged

**Solution:**
```bash
# Force update modification time
touch my_local_files/your_file.pdf

# Sync
python auto_index_folder.py sync
```

### "Want to force re-upload of duplicate"

**If you need to re-upload:**

**Option 1: Edit index**
```bash
# Remove file from index
python -c "
import json
with open('.file_index.json') as f:
    index = json.load(f)
del index['my_local_files/your_file.pdf']
with open('.file_index.json', 'w') as f:
    json.dump(index, f, indent=2)
"

# Sync (will upload as new)
python auto_index_folder.py sync
```

**Option 2: Delete index and re-initialize**
```bash
rm .file_index.json
python auto_index_folder.py init
```

---

## Best Practices

### 1. Clean Up Duplicates

Before initializing, remove obvious duplicates:

```bash
# Find duplicate filenames
find my_local_files -type f -name "*.pdf" | sort | uniq -d

# Remove backups
find my_local_files -name "*_backup*" -type f -delete
find my_local_files -name "*_copy*" -type f -delete
```

### 2. Organize Before Upload

Structure files logically to avoid confusion:

```bash
my_local_files/
├── active/          # Current working files
├── archive/         # Old versions (might have duplicates)
└── reference/       # Reference materials
```

### 3. Regular Index Cleanup

Periodically review index for orphaned entries:

```bash
# List files in index but not in folder
python -c "
import json
from pathlib import Path

with open('.file_index.json') as f:
    index = json.load(f)

for path in index:
    if not Path(path).exists():
        print(f'Orphaned: {path}')
"
```

### 4. Version Control for Documents

If you need multiple versions, use clear naming:

```bash
# Good - clearly different versions
my_local_files/
├── report_v1_draft.pdf
├── report_v2_revised.pdf
└── report_v3_final.pdf

# Bad - unclear, might be duplicates
my_local_files/
├── report.pdf
├── report_new.pdf
└── report_copy.pdf
```

---

## Configuration

### Change Hash Algorithm

By default, SHA256 is used. To change:

Edit `auto_index_folder.py`:

```python
def calculate_file_hash(self, file_path):
    # Change to MD5 (faster, less secure)
    md5_hash = hashlib.md5()

    # Or SHA512 (slower, more secure)
    sha512_hash = hashlib.sha512()
```

**Recommendation:** Stick with SHA256 (good balance).

### Disable Duplicate Detection

If you want to upload all files regardless:

Edit `auto_index_folder.py`, in `find_changes()`:

```python
# Comment out duplicate detection
# is_duplicate, duplicate_path = self.is_duplicate_content(file_hash, old_index)
# if is_duplicate:
#     duplicate_files.append(...)
#     continue

# Always treat as new
new_files.append(Path(file_path))
```

---

## Summary

### What Gets Detected

✅ Exact copies with different names
✅ Files in different folders with same content
✅ Renamed files with unchanged content
✅ Backup files that match originals

### What Doesn't Get Detected

❌ Similar files with slightly different content
❌ Files with same name but different content
❌ Compressed vs uncompressed versions

### Storage Location

The system uses **dual storage** - both online and local:

🗄️ **Local Storage:** `.file_index.json` (in project root)
- Stores file metadata (name, size, modified time, hash)
- Tracks all files and duplicates
- Used for change detection
- Fast local access

☁️ **Online Storage:** Google File Search Store (cloud)
- Stores actual file content and embeddings
- Enables semantic search and RAG queries
- Only unique files uploaded (no duplicates)
- Accessible from anywhere

### Commands

```bash
# Initialize with duplicate detection
python auto_index_folder.py init

# Sync with duplicate detection
python auto_index_folder.py sync

# Watch with automatic duplicate detection
python auto_index_folder.py watch 60
```

---

**Questions?** Check AUTO_INDEX_GUIDE.md for more details!
