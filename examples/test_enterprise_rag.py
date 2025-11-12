"""
Test Enterprise RAG System
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.enterprise_rag import EnterpriseRAG


def main():
    print("="*60)
    print("Enterprise RAG Test - Premium Components")
    print("="*60)

    # Initialize
    print("\n1. Initializing Enterprise RAG...")
    print("   - OpenAI text-embedding-3-large (3072 dim)")
    print("   - Pinecone serverless vector DB")
    print("   - Cohere rerank-english-v3.0")
    print("   - Claude 3.5 Sonnet")

    try:
        rag = EnterpriseRAG(index_name="test-enterprise")
        print("   ✅ Initialized successfully")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("\n   Make sure you have API keys in .env:")
        print("   - OPENAI_API_KEY")
        print("   - PINECONE_API_KEY")
        print("   - COHERE_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        return

    # Check if demo files exist
    demo_dir = Path(__file__).parent.parent / "demo_data"

    if not demo_dir.exists():
        print("\n   ⚠️ Demo data not found. Skipping upload test.")
    else:
        # Upload demo files
        print("\n2. Uploading demo files...")
        txt_files = list(demo_dir.glob("*.txt"))

        if txt_files:
            for txt_file in txt_files[:2]:  # Upload first 2 files
                print(f"   Uploading: {txt_file.name}")
                try:
                    chunks = rag.upload_file(txt_file)
                    print(f"   ✅ {chunks} chunks indexed")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        else:
            print("   No .txt files found in demo_data")

    # Get stats
    print("\n3. Index Statistics:")
    try:
        stats = rag.get_stats()
        print(f"   Total vectors: {stats['total_vectors']}")
        print(f"   Dimension: {stats['dimension']}")
        print(f"   Index fullness: {stats['index_fullness']}")
    except Exception as e:
        print(f"   ❌ Error getting stats: {e}")

    # Test queries
    print("\n4. Testing Queries:")
    questions = [
        "What is LENR?",
        "Who are the main researchers?",
        "What experimental methods are used?"
    ]

    for q in questions:
        print(f"\n   Q: {q}")
        try:
            result = rag.query(
                q,
                top_k=10,
                rerank_top_k=3,
                use_reranking=True
            )
            print(f"   A: {result['answer'][:150]}...")
            print(f"   Sources: {result['n_sources']}")
            print(f"   Model: {result['model']}")

            # Show top source
            if result['sources']:
                top_source = result['sources'][0]
                print(f"   Top source: {top_source['filename']} "
                      f"(score: {top_source.get('rerank_score', 0):.3f})")

        except Exception as e:
            print(f"   ❌ Query error: {e}")

    print("\n" + "="*60)
    print("✅ Enterprise RAG Test Complete!")
    print("="*60)

    # Cost estimate
    print("\n💰 Estimated costs for this test:")
    print("   - Embeddings: ~$0.001")
    print("   - Storage: ~$0.0001/month")
    print("   - Reranking: ~$0.01")
    print("   - LLM: ~$0.01")
    print("   Total: ~$0.02")


if __name__ == "__main__":
    main()
