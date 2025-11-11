"""
测试本地RAG系统
Test local RAG system
"""

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.local_rag import LocalRAG


def main():
    print("="*60)
    print("本地RAG测试 / Local RAG Test")
    print("="*60)

    # 初始化
    print("\n1. 初始化LocalRAG...")
    rag = LocalRAG(
        persist_directory="./test_chroma_db",
        embedding_model="all-MiniLM-L6-v2"  # 小而快的模型
    )

    # 创建collection
    print("\n2. 创建collection...")
    rag.create_collection("test_docs")

    # 上传demo文件
    print("\n3. 上传demo文件...")
    demo_dir = Path(__file__).parent.parent / "demo_data"

    if demo_dir.exists():
        for txt_file in demo_dir.glob("*.txt"):
            print(f"   上传: {txt_file.name}")
            chunks = rag.upload_file(
                txt_file,
                collection_name="test_docs",
                metadata={"source": "demo", "type": "research"}
            )
            print(f"   ✅ {chunks} chunks indexed")
    else:
        print("   ⚠️ Demo data not found")

    # 查看统计
    print("\n4. 数据库统计:")
    stats = rag.get_stats()
    print(f"   Collections: {stats['collections']}")
    print(f"   Total documents: {stats['total_documents']}")
    print(f"   Database size: {stats['database_size_mb']:.2f} MB")

    # 测试查询
    print("\n5. 测试查询...")
    questions = [
        "What is LENR?",
        "Who are the main researchers?",
        "What are the experimental methods?"
    ]

    for q in questions:
        print(f"\n   Q: {q}")
        result = rag.query(q, "test_docs", n_results=3)
        print(f"   A: {result['answer'][:200]}...")
        print(f"   Sources: {result['n_sources']}")

    print("\n" + "="*60)
    print("✅ 测试完成！")
    print("="*60)


if __name__ == "__main__":
    main()
