"""Basic usage example for Gemini RAG system."""

import os
from pathlib import Path
from dotenv import load_dotenv

from src.rag.gemini_rag import GeminiRAG

# Load environment variables
load_dotenv()


def main():
    """Demonstrate basic RAG functionality."""

    # Initialize RAG system
    print("Initializing Gemini RAG system...")
    rag = GeminiRAG()

    # Create a file search store
    print("\n1. Creating file search store...")
    store_name = rag.create_store("demo-store")
    print(f"   Created store: {store_name}")

    # List all stores
    print("\n2. Listing all stores...")
    stores = rag.list_stores()
    for store in stores:
        print(f"   - {store['display_name']}: {store['name']}")

    # Upload a document (you need to create a sample file)
    print("\n3. Uploading documents...")
    sample_file = Path("sample_document.txt")

    # Create a sample document if it doesn't exist
    if not sample_file.exists():
        sample_file.write_text("""
        Low-Energy Nuclear Reactions (LENR)

        Low-Energy Nuclear Reactions, sometimes called cold fusion, refers to nuclear
        reactions that occur at relatively low temperatures compared to traditional
        fusion reactions.

        Key Points:
        1. LENR experiments typically operate at near-room temperature
        2. The field remains controversial in the scientific community
        3. Various experimental setups have been proposed and tested
        4. Potential applications include clean energy generation

        Research History:
        The field gained attention in 1989 when Fleischmann and Pons announced
        their cold fusion experiments. Since then, researchers worldwide have
        continued investigations into LENR phenomena.

        Current Status:
        While some researchers report positive results, reproducibility remains
        a significant challenge. The theoretical understanding of the mechanisms
        is still developing.
        """)
        print(f"   Created sample document: {sample_file}")

    # Upload with metadata
    operation = rag.upload_file(
        file_path=sample_file,
        store_name=store_name,
        metadata={
            "category": "research",
            "topic": "LENR",
            "year": "2024"
        }
    )
    print(f"   Uploaded file, operation: {operation}")

    # Query the documents
    print("\n4. Querying the documents...")
    questions = [
        "What is LENR?",
        "What are the key points about LENR?",
        "Who were the early researchers in this field?",
        "What are the current challenges in LENR research?"
    ]

    for question in questions:
        print(f"\n   Q: {question}")
        response = rag.query(
            question=question,
            store_name=store_name
        )
        print(f"   A: {response['answer']}")

        if response['citations']:
            print(f"   Citations: {len(response['citations'])} sources")

    # Cleanup (optional)
    print("\n5. Cleanup...")
    cleanup = input("   Delete the demo store? (y/n): ").lower()
    if cleanup == 'y':
        rag.delete_store(store_name)
        print("   Store deleted")

    # Clean up sample file
    if sample_file.exists():
        sample_file.unlink()
        print("   Sample document removed")

    print("\n✓ Demo completed!")


if __name__ == "__main__":
    main()
