"""Sync local file changes to RAG system."""

import json
from pathlib import Path
from datetime import datetime
from src.rag.gemini_rag import GeminiRAG


def save_file_index():
    """Save current state of files."""
    local_dir = Path("my_local_files")

    if not local_dir.exists():
        print("❌ my_local_files/ not found. Create it first:")
        print("   mkdir my_local_files")
        return

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
    print(f"✓ Saved to .file_index.json")


def find_changed_files():
    """Find files that changed since last sync."""

    # Load previous index
    index_file = Path(".file_index.json")
    if not index_file.exists():
        print("❌ No previous index found.")
        print("\nRun this first:")
        print("  python sync_changes.py init")
        return [], []

    with open(index_file) as f:
        old_index = json.load(f)

    # Check current files
    local_dir = Path("my_local_files")

    if not local_dir.exists():
        print("❌ my_local_files/ not found")
        return [], []

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


def sync_to_rag(store_name="local-files-store"):
    """Upload changed and new files."""

    print("\n" + "="*60)
    print("Syncing Local Files to RAG")
    print("="*60 + "\n")

    changed, new = find_changed_files()

    if not changed and not new:
        print("✓ No changes detected. All files up to date!")
        return

    print(f"📝 Found {len(changed)} changed files")
    print(f"📝 Found {len(new)} new files")
    print()

    rag = GeminiRAG()

    # Upload changed files
    if changed:
        print("🔄 Updating changed files:\n")
        for file_path in changed:
            print(f"   {file_path.name}")
            try:
                metadata = {
                    "status": "updated",
                    "updated_at": datetime.now().isoformat(),
                    "category": file_path.parent.name
                }

                if file_path.suffix in ['.xlsx', '.xls']:
                    rag.upload_excel(file_path, store_name, metadata=metadata)
                else:
                    rag.upload_file(file_path, store_name, metadata=metadata)

                print(f"   ✅ Updated\n")

            except Exception as e:
                print(f"   ❌ Error: {e}\n")

    # Upload new files
    if new:
        print("➕ Adding new files:\n")
        for file_path in new:
            print(f"   {file_path.name}")
            try:
                metadata = {
                    "status": "new",
                    "added_at": datetime.now().isoformat(),
                    "category": file_path.parent.name
                }

                if file_path.suffix in ['.xlsx', '.xls']:
                    rag.upload_excel(file_path, store_name, metadata=metadata)
                else:
                    rag.upload_file(file_path, store_name, metadata=metadata)

                print(f"   ✅ Added\n")

            except Exception as e:
                print(f"   ❌ Error: {e}\n")

    # Update index
    print("💾 Updating file index...")
    save_file_index()

    print("\n" + "="*60)
    print(f"✅ Sync complete!")
    print("="*60)
    print(f"\n🏪 Store: {store_name}")
    print("✓ Files are up to date in RAG system")


def show_status():
    """Show current sync status."""

    print("\n" + "="*60)
    print("Local Files Sync Status")
    print("="*60 + "\n")

    index_file = Path(".file_index.json")

    if not index_file.exists():
        print("❌ Not initialized yet")
        print("\nRun: python sync_changes.py init")
        return

    changed, new = find_changed_files()

    if not changed and not new:
        print("✅ All files are up to date")
    else:
        if changed:
            print(f"🔄 {len(changed)} changed files:")
            for f in changed:
                print(f"   - {f.name}")

        if new:
            print(f"\n➕ {len(new)} new files:")
            for f in new:
                print(f"   - {f.name}")

        print("\nRun to sync: python sync_changes.py sync")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "init":
            print("\n📁 Initializing file tracking...")
            save_file_index()
            print("\n✓ Done! Files are now being tracked")
            print("\nNext: Edit your files, then run:")
            print("  python sync_changes.py sync")

        elif command == "sync":
            store_name = sys.argv[2] if len(sys.argv) > 2 else "local-files-store"
            sync_to_rag(store_name)

        elif command == "status":
            show_status()

        else:
            print("❌ Unknown command. Use: init, sync, or status")

    else:
        print("\nUsage:")
        print("  python sync_changes.py init              # First time setup")
        print("  python sync_changes.py status            # Check for changes")
        print("  python sync_changes.py sync [store]      # Upload changes")
        print("\nExample:")
        print("  python sync_changes.py init")
        print("  # ... edit some files ...")
        print("  python sync_changes.py status")
        print("  python sync_changes.py sync local-files-store")
