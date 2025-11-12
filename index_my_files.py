"""
Index Your 7000+ Files for Enterprise RAG
This script uploads all your files to the enterprise RAG system
"""

from src.rag.enterprise_rag import EnterpriseRAG
from pathlib import Path
import time
import sys

def main():
    print("=" * 60)
    print("Enterprise RAG - File Indexing")
    print("=" * 60)
    print()

    # Configuration
    INDEX_NAME = "my-7000-files"
    FILES_DIRECTORY = "my_local_files"  # Change this to your directory
    BATCH_SIZE = 50  # Process 50 files at a time

    # Supported file types
    SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.md', '.docx', '.xlsx', '.xls'}

    # Step 1: Initialize RAG
    print("Step 1: Initializing Enterprise RAG...")
    try:
        rag = EnterpriseRAG(index_name=INDEX_NAME)
        print("✅ Enterprise RAG initialized")
        print(f"   Index name: {INDEX_NAME}")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print()
        print("Please check:")
        print("1. All API keys are set in .env")
        print("2. Dependencies are installed: pip install -r requirements_enterprise.txt")
        print("3. Run test first: python examples/test_enterprise_rag.py")
        sys.exit(1)

    # Step 2: Find files
    print(f"Step 2: Finding files in '{FILES_DIRECTORY}'...")

    files_path = Path(FILES_DIRECTORY)
    if not files_path.exists():
        print(f"❌ Directory not found: {FILES_DIRECTORY}")
        print()
        print("Please create the directory and add your files:")
        print(f"   mkdir -p {FILES_DIRECTORY}")
        print(f"   cp your_files/* {FILES_DIRECTORY}/")
        sys.exit(1)

    # Get all files
    all_files = list(files_path.rglob("*"))
    files_to_index = [
        f for f in all_files
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files_to_index:
        print(f"❌ No supported files found in {FILES_DIRECTORY}")
        print()
        print(f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}")
        sys.exit(1)

    print(f"✅ Found {len(files_to_index)} files to index")
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

    # Confirm
    print(f"This will upload {len(files_to_index)} files to index '{INDEX_NAME}'")
    print("Estimated time: 1-2 hours for 7000 files")
    print()
    response = input("Continue? [Y/n]: ")
    if response.lower() == 'n':
        print("Aborted.")
        sys.exit(0)
    print()

    # Step 3: Index files
    print("Step 3: Indexing files...")
    print("This may take 1-2 hours. Progress will be shown.")
    print()

    start_time = time.time()

    try:
        stats = rag.batch_upload(
            files_to_index,
            batch_size=BATCH_SIZE,
            show_progress=True
        )
    except KeyboardInterrupt:
        print()
        print("⚠️  Indexing interrupted by user")
        print("Files indexed so far are saved.")
        print("Run this script again to continue indexing remaining files.")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ Indexing failed: {e}")
        sys.exit(1)

    elapsed = time.time() - start_time

    # Step 4: Results
    print()
    print("=" * 60)
    print("✅ INDEXING COMPLETE!")
    print("=" * 60)
    print()
    print(f"Time taken: {elapsed/3600:.1f} hours ({elapsed/60:.1f} minutes)")
    print(f"Files indexed: {stats['successful']}/{stats['total']}")
    print(f"Total chunks: {stats['total_chunks']:,}")
    print(f"Failed: {stats['failed']}")
    print()

    if stats['failed'] > 0:
        print("⚠️  Some files failed to index. Check the logs above.")
        print()

    # Index statistics
    print("Checking index statistics...")
    index_stats = rag.get_index_stats()
    print(f"   Total vectors in index: {index_stats['total_vectors']:,}")
    print(f"   Index dimension: {index_stats['dimension']}")
    print()

    # Cost estimate
    cost_per_query = 0.01  # Approximate
    print("💰 Cost estimate:")
    print(f"   One-time indexing: ~${stats['total_chunks'] * 0.0001:.2f}")
    print(f"   Per query: ~${cost_per_query}")
    print(f"   1000 queries/month: ~${cost_per_query * 1000:.2f}/month")
    print()

    print("=" * 60)
    print("Next steps:")
    print("=" * 60)
    print()
    print("1. Test a query:")
    print("   python")
    print("   >>> from src.rag.enterprise_rag import EnterpriseRAG")
    print(f"   >>> rag = EnterpriseRAG(index_name='{INDEX_NAME}')")
    print("   >>> result = rag.query('Your question')")
    print("   >>> print(result['answer'])")
    print()
    print("2. Start web interface:")
    print("   streamlit run streamlit_enterprise.py")
    print()
    print("3. Share with team:")
    print("   - Share API keys (securely)")
    print(f"   - Share index name: {INDEX_NAME}")
    print("   - Team can query immediately!")
    print()
    print("🚀 Your Enterprise RAG is ready!")
    print()


if __name__ == "__main__":
    main()
