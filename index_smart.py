"""
Index Your 7000+ Files - Smart RAG
Simple script to index all your files
"""

from src.rag.smart_rag import SmartRAG
from pathlib import Path
import time
import sys

def main():
    print("=" * 60)
    print("Smart RAG - File Indexing")
    print("=" * 60)
    print()

    # Configuration
    FILES_DIRECTORY = "my_local_files"
    COLLECTION_NAME = "my_docs"
    SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.md', '.docx', '.xlsx', '.xls'}

    # Step 1: Initialize
    print("Step 1: Initializing Smart RAG...")
    try:
        rag = SmartRAG()
        print("✅ Smart RAG initialized")
        print(f"   Model: {rag.model}")
        print(f"   Storage: {rag.persist_directory}")
        print()
    except Exception as e:
        print(f"❌ Failed: {e}")
        print()
        print("Please set your OpenAI API key:")
        print("  echo 'OPENAI_API_KEY=your-key' > .env")
        print()
        print("Get key at: https://platform.openai.com/api-keys")
        sys.exit(1)

    # Step 2: Find files
    print(f"Step 2: Finding files in '{FILES_DIRECTORY}'...")

    files_path = Path(FILES_DIRECTORY)
    if not files_path.exists():
        print(f"❌ Directory not found: {FILES_DIRECTORY}")
        print()
        print("Creating directory...")
        files_path.mkdir(parents=True)
        print(f"✅ Created: {FILES_DIRECTORY}")
        print()
        print("Please add your files there:")
        print(f"  cp your_files/* {FILES_DIRECTORY}/")
        sys.exit(0)

    # Find all files
    all_files = list(files_path.rglob("*"))
    files_to_index = [
        f for f in all_files
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files_to_index:
        print(f"❌ No files found in {FILES_DIRECTORY}")
        print()
        print(f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
        print()
        print("Add files:")
        print(f"  cp your_files/* {FILES_DIRECTORY}/")
        sys.exit(0)

    print(f"✅ Found {len(files_to_index)} files")
    print()

    # File type breakdown
    file_types = {}
    for f in files_to_index:
        ext = f.suffix.lower()
        file_types[ext] = file_types.get(ext, 0) + 1

    print("File types:")
    for ext, count in sorted(file_types.items()):
        print(f"   {ext}: {count} files")
    print()

    # Step 3: Create collection
    print(f"Step 3: Creating collection '{COLLECTION_NAME}'...")
    rag.create_collection(COLLECTION_NAME)
    print(f"✅ Collection ready")
    print()

    # Confirm
    print(f"Ready to index {len(files_to_index)} files")

    # Estimate time and cost
    estimated_minutes = len(files_to_index) * 2 / 60  # ~2 seconds per file
    estimated_cost = len(files_to_index) * 0.0001  # ~$0.0001 per file

    print(f"Estimated time: {estimated_minutes:.0f} minutes")
    print(f"Estimated cost: ${estimated_cost:.2f}")
    print()

    response = input("Continue? [Y/n]: ")
    if response.lower() == 'n':
        print("Cancelled.")
        sys.exit(0)
    print()

    # Step 4: Index files
    print("Step 4: Indexing files...")
    print("Progress will be shown below:")
    print()

    start_time = time.time()

    try:
        stats = rag.batch_upload(
            files_to_index,
            collection_name=COLLECTION_NAME,
            batch_size=20,
            show_progress=True
        )
    except KeyboardInterrupt:
        print()
        print("⚠️  Interrupted by user")
        print("Files indexed so far are saved.")
        sys.exit(0)
    except Exception as e:
        print()
        print(f"❌ Failed: {e}")
        sys.exit(1)

    elapsed = time.time() - start_time

    # Results
    print()
    print("=" * 60)
    print("✅ INDEXING COMPLETE!")
    print("=" * 60)
    print()
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"📁 Files: {stats['successful']}/{stats['total']}")
    print(f"📝 Chunks: {stats['total_chunks']:,}")
    print(f"⚠️  Skipped: {stats['skipped']} (duplicates)")
    print(f"❌ Failed: {stats['failed']}")
    print()

    # Database stats
    print("Database statistics:")
    db_stats = rag.get_stats()
    print(f"   Total documents: {db_stats['total_documents']:,}")
    print(f"   Database size: {db_stats['database_size_mb']:.2f} MB")
    print(f"   Indexed files: {db_stats['indexed_files']}")
    print()

    # Cost estimate
    actual_cost = stats['total_chunks'] * 0.00002  # text-embedding-3-small cost
    print("💰 Actual cost:")
    print(f"   Indexing: ~${actual_cost:.3f}")
    print(f"   Per query: ~$0.003 (GPT-4 Turbo)")
    print(f"   1000 queries/month: ~$3-5")
    print()

    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print()
    print("1. Test a query:")
    print(f"   python")
    print(f"   >>> from src.rag.smart_rag import SmartRAG")
    print(f"   >>> rag = SmartRAG()")
    print(f"   >>> result = rag.query('Your question', '{COLLECTION_NAME}')")
    print(f"   >>> print(result['answer'])")
    print()
    print("2. Start web interface:")
    print(f"   streamlit run streamlit_smart.py")
    print()
    print("3. Export database for sharing:")
    print(f"   python database_manager.py export ./smart_rag_db shared.tar.gz")
    print()
    print("🚀 Your Smart RAG is ready!")
    print()


if __name__ == "__main__":
    main()
