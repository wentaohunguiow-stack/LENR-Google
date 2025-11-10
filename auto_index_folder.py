"""Auto-index folder - watches my_local_files/ and uploads new/changed files automatically."""

import time
import json
from pathlib import Path
from datetime import datetime
from src.rag.gemini_rag import GeminiRAG


class FolderAutoIndexer:
    """Automatically index files from a folder to RAG system."""

    def __init__(self, folder_path="my_local_files", store_name="local-files-store"):
        self.folder_path = Path(folder_path)
        self.store_name = store_name
        self.index_file = Path(".file_index.json")
        self.rag = GeminiRAG()

    def load_index(self):
        """Load existing file index."""
        if self.index_file.exists():
            with open(self.index_file) as f:
                return json.load(f)
        return {}

    def save_index(self, index):
        """Save file index."""
        with open(self.index_file, 'w') as f:
            json.dump(index, f, indent=2)

    def get_file_info(self, file_path):
        """Get file metadata."""
        stat = file_path.stat()
        return {
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "name": file_path.name
        }

    def scan_folder(self):
        """Scan folder for all files."""
        files = {}
        for file_path in self.folder_path.rglob("*"):
            if file_path.is_file() and file_path.name != "README.md":
                files[str(file_path)] = self.get_file_info(file_path)
        return files

    def find_changes(self, old_index, current_files):
        """Find new and changed files."""
        new_files = []
        changed_files = []

        for file_path, file_info in current_files.items():
            if file_path not in old_index:
                new_files.append(Path(file_path))
            elif file_info["modified"] > old_index[file_path]["modified"]:
                changed_files.append(Path(file_path))

        return new_files, changed_files

    def upload_file_to_rag(self, file_path):
        """Upload a single file to RAG."""
        try:
            suffix = file_path.suffix.lower()
            relative_path = file_path.relative_to(self.folder_path)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "general"

            metadata = {
                "category": category,
                "filename": file_path.name,
                "upload_date": datetime.now().strftime("%Y-%m-%d"),
                "local_path": str(relative_path)
            }

            if suffix in ['.xlsx', '.xls']:
                self.rag.upload_excel(str(file_path), self.store_name, metadata=metadata)
            elif suffix in ['.pdf', '.txt', '.md', '.docx', '.html']:
                self.rag.upload_file(str(file_path), self.store_name, metadata=metadata)
            else:
                return False, "Unsupported file type"

            return True, "Success"
        except Exception as e:
            return False, str(e)

    def initialize(self):
        """Initialize the indexer - create store and scan files."""
        print("\n" + "="*60)
        print("Initializing Auto-Indexer")
        print("="*60 + "\n")

        # Check folder exists
        if not self.folder_path.exists():
            print(f"❌ Folder not found: {self.folder_path}")
            print(f"\nCreating folder...")
            self.folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created {self.folder_path}/")
            print(f"\n📝 Add your files to {self.folder_path}/")
            print(f"   Then run: python auto_index_folder.py")
            return False

        # Ensure store exists
        try:
            self.rag.create_store(self.store_name)
            print(f"✓ Store ready: {self.store_name}\n")
        except Exception as e:
            print(f"Note: {e}")

        # Scan and upload all files
        current_files = self.scan_folder()

        if not current_files:
            print("📂 Folder is empty")
            print(f"\n📝 Add files to {self.folder_path}/")
            print(f"   cp ~/Desktop/*.pdf {self.folder_path}/research/")
            print(f"   cp ~/Documents/*.xlsx {self.folder_path}/data/")
            return False

        print(f"📁 Found {len(current_files)} files\n")
        print("📤 Uploading all files...\n")

        uploaded = 0
        failed = 0

        for file_path_str in current_files:
            file_path = Path(file_path_str)
            print(f"   {file_path.name}...", end=" ")
            success, message = self.upload_file_to_rag(file_path)

            if success:
                print("✅")
                uploaded += 1
            else:
                print(f"❌ {message}")
                failed += 1

        # Save index
        self.save_index(current_files)

        print("\n" + "="*60)
        print(f"✅ Initialization Complete")
        print("="*60)
        print(f"Uploaded: {uploaded} files")
        print(f"Failed: {failed} files")
        print(f"\n🏪 Store: {self.store_name}")
        print(f"📂 Watching: {self.folder_path}/")

        return True

    def sync_once(self):
        """Check for changes and sync once."""
        print("\n" + "="*60)
        print("Checking for Changes")
        print("="*60 + "\n")

        old_index = self.load_index()

        if not old_index:
            print("❌ Not initialized yet")
            print("\nRun first: python auto_index_folder.py init")
            return

        current_files = self.scan_folder()
        new_files, changed_files = self.find_changes(old_index, current_files)

        if not new_files and not changed_files:
            print("✅ No changes detected. All files up to date!")
            return

        print(f"📝 Found {len(new_files)} new files")
        print(f"📝 Found {len(changed_files)} changed files\n")

        # Upload new files
        if new_files:
            print("➕ Uploading new files:\n")
            for file_path in new_files:
                print(f"   {file_path.name}...", end=" ")
                success, message = self.upload_file_to_rag(file_path)
                if success:
                    print("✅")
                else:
                    print(f"❌ {message}")

        # Upload changed files
        if changed_files:
            print("\n🔄 Uploading changed files:\n")
            for file_path in changed_files:
                print(f"   {file_path.name}...", end=" ")
                success, message = self.upload_file_to_rag(file_path)
                if success:
                    print("✅")
                else:
                    print(f"❌ {message}")

        # Update index
        self.save_index(current_files)

        print("\n" + "="*60)
        print("✅ Sync Complete")
        print("="*60)

    def watch(self, interval=60):
        """Watch folder and auto-upload changes (runs continuously)."""
        print("\n" + "="*60)
        print("Auto-Indexer - Watch Mode")
        print("="*60 + "\n")
        print(f"📂 Watching: {self.folder_path}/")
        print(f"🏪 Store: {self.store_name}")
        print(f"⏱️  Check interval: {interval} seconds")
        print("\nPress Ctrl+C to stop\n")

        old_index = self.load_index()

        if not old_index:
            print("⚠️  Not initialized. Running initialization first...\n")
            if not self.initialize():
                return
            old_index = self.load_index()

        try:
            while True:
                current_files = self.scan_folder()
                new_files, changed_files = self.find_changes(old_index, current_files)

                if new_files or changed_files:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\n[{timestamp}] Changes detected!")

                    # Upload new files
                    for file_path in new_files:
                        print(f"   ➕ New: {file_path.name}...", end=" ")
                        success, message = self.upload_file_to_rag(file_path)
                        if success:
                            print("✅")
                        else:
                            print(f"❌ {message}")

                    # Upload changed files
                    for file_path in changed_files:
                        print(f"   🔄 Changed: {file_path.name}...", end=" ")
                        success, message = self.upload_file_to_rag(file_path)
                        if success:
                            print("✅")
                        else:
                            print(f"❌ {message}")

                    # Update index
                    self.save_index(current_files)
                    old_index = current_files
                    print(f"   ✓ Synced at {timestamp}")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\n✓ Auto-indexer stopped")


def main():
    """Main entry point."""
    import sys

    indexer = FolderAutoIndexer()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "init":
            indexer.initialize()

        elif command == "sync":
            indexer.sync_once()

        elif command == "watch":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            indexer.watch(interval)

        else:
            print("❌ Unknown command")
            print("\nUsage:")
            print("  python auto_index_folder.py init              # Initialize and upload all")
            print("  python auto_index_folder.py sync              # Check and sync once")
            print("  python auto_index_folder.py watch [interval]  # Auto-sync continuously")

    else:
        print("\n" + "="*60)
        print("Auto-Index Folder - Automatic RAG Indexing")
        print("="*60 + "\n")
        print("Commands:")
        print("  init    - Initialize: scan and upload all files")
        print("  sync    - Sync once: upload new/changed files")
        print("  watch   - Watch mode: auto-sync continuously\n")
        print("Usage:")
        print("  python auto_index_folder.py init")
        print("  python auto_index_folder.py sync")
        print("  python auto_index_folder.py watch [interval_seconds]\n")
        print("Examples:")
        print("  python auto_index_folder.py init         # First time setup")
        print("  python auto_index_folder.py sync         # Manual sync")
        print("  python auto_index_folder.py watch 30     # Auto-sync every 30 seconds")
        print("  python auto_index_folder.py watch 300    # Auto-sync every 5 minutes\n")
        print("Folder: my_local_files/")
        print("Store: local-files-store\n")


if __name__ == "__main__":
    main()
