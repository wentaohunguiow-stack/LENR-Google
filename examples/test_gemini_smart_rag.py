"""
Test Gemini Smart RAG System - Best Gemini Solution
Only 1 Google API key needed, best quality, lowest cost
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.gemini_smart_rag import GeminiSmartRAG

def main():
    print("=" * 60)
    print("Gemini Smart RAG System Test")
    print("=" * 60)
    print()

    # Step 1: Initialize
    print("1. Initializing Gemini Smart RAG...")
    try:
        rag = GeminiSmartRAG(persist_directory="./test_gemini_smart_rag_db")
        print("   ✅ Gemini Smart RAG initialized")
        print(f"   Model: {rag.model}")
        print(f"   Embeddings: {rag.embedding_model}")
        print()
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        print()
        print("   Please set GOOGLE_API_KEY environment variable:")
        print("   export GOOGLE_API_KEY='your-key-here'")
        print()
        print("   Get your key at: https://aistudio.google.com/apikey")
        return

    # Step 2: Create collection
    print("2. Creating collection...")
    rag.create_collection("test_docs")
    print("   ✅ Created collection: test_docs")
    print()

    # Step 3: Upload demo files
    print("3. Uploading demo files...")
    demo_dir = Path(__file__).parent.parent / "demo_data"

    if not demo_dir.exists():
        print("   ⚠️  demo_data directory not found")
        print("   Creating test document...")

        # Create a test file
        test_file = Path("test_document.txt")
        test_file.write_text("""
LENR (Low Energy Nuclear Reactions)

LENR, or Low Energy Nuclear Reactions, is a field of research investigating nuclear reactions
that occur at relatively low temperatures and energies, compared to traditional hot fusion.

Key Points:
1. LENR reactions occur at room temperature or modest temperatures
2. They potentially offer a clean, safe energy source
3. Research continues into the mechanisms and applications
4. Various approaches include palladium-deuterium systems and nickel-hydrogen systems

The field remains controversial but continues to attract research interest globally.
        """.strip())

        print(f"   Uploading: {test_file.name}")
        chunks = rag.upload_file(test_file, "test_docs")
        print(f"   ✅ {chunks} chunks indexed")
        print()

        # Clean up
        test_file.unlink()

    else:
        # Upload demo files
        demo_files = list(demo_dir.glob("*.txt")) + list(demo_dir.glob("*.pdf"))
        if demo_files:
            for demo_file in demo_files[:3]:  # Upload first 3 files
                print(f"   Uploading: {demo_file.name}")
                try:
                    chunks = rag.upload_file(demo_file, "test_docs")
                    print(f"   ✅ {chunks} chunks indexed")
                except Exception as e:
                    print(f"   ⚠️  Failed: {e}")
        else:
            print("   ⚠️  No demo files found")
        print()

    # Step 4: Database statistics
    print("4. Database statistics:")
    stats = rag.get_stats()
    print(f"   Collections: {stats['collections']}")
    print(f"   Total documents: {stats['total_documents']}")
    print(f"   Database size: {stats['database_size_mb']:.2f} MB")
    print(f"   Indexed files: {stats['indexed_files']}")
    print()

    # Step 5: Test query
    print("5. Testing query...")
    print("   Q: What is LENR?")
    print()

    try:
        result = rag.query(
            "What is LENR?",
            collection_name="test_docs",
            n_results=3,
            temperature=0.7
        )

        print("   📝 Answer:")
        print("   " + "-" * 56)
        # Print answer with indentation
        for line in result['answer'].split('\n'):
            print(f"   {line}")
        print("   " + "-" * 56)
        print()

        print(f"   📚 Sources: {result['n_sources']}")
        for i, source in enumerate(result['sources'], 1):
            print(f"      {i}. {source['filename']} (relevance: {source['relevance']:.3f})")
        print()

    except Exception as e:
        print(f"   ❌ Query failed: {e}")
        print()

    # Step 6: Cost estimate
    print("6. Cost estimate:")
    print("   Embeddings: FREE (Gemini API)")
    print("   Per query: ~$0.0005 (Gemini 2.0 Flash)")
    print("   1000 queries: ~$0.50/month")
    print("   Storage: FREE (local disk)")
    print()
    print("   💰 Total: ~$0.50-1/month (cheapest option!)")
    print()

    print("=" * 60)
    print("✅ Gemini Smart RAG Test Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Index your files: python index_gemini.py")
    print("2. Start web UI: streamlit run streamlit_gemini.py")
    print()


if __name__ == "__main__":
    main()
