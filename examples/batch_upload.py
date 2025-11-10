"""Batch upload example for processing multiple documents."""

import os
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

from src.rag.gemini_rag import GeminiRAG

load_dotenv()


def scan_directory(directory: Path) -> list:
    """Scan directory for supported document files."""
    supported_extensions = {'.txt', '.pdf', '.md', '.html', '.docx'}
    files = []

    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            files.append(file_path)

    return files


def extract_metadata_from_path(file_path: Path) -> Dict[str, str]:
    """
    Extract metadata from file path structure.

    Example structure:
        documents/category/year/filename.txt
        -> {category: 'category', year: 'year', filename: 'filename'}
    """
    parts = file_path.parts
    metadata = {
        'filename': file_path.stem,
        'extension': file_path.suffix,
        'size_kb': f"{file_path.stat().st_size / 1024:.2f}"
    }

    # Try to extract category and year from path
    if len(parts) >= 2:
        metadata['category'] = parts[-2]

    if len(parts) >= 3:
        # Check if second-to-last part looks like a year
        potential_year = parts[-3]
        if potential_year.isdigit() and len(potential_year) == 4:
            metadata['year'] = potential_year

    return metadata


def batch_upload_documents():
    """Demonstrate batch uploading of documents."""

    print("=" * 60)
    print("Batch Document Upload Demo")
    print("=" * 60)

    # Initialize RAG
    rag = GeminiRAG()

    # Create demo directory structure
    print("\n1. Setting up demo directory structure...")
    base_dir = Path("documents")
    categories = ["research_papers", "experiments", "theory"]

    demo_files = []
    for category in categories:
        cat_dir = base_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)

        # Create sample files
        for i in range(3):
            file_path = cat_dir / f"{category}_doc_{i+1}.txt"
            file_path.write_text(f"""
            Sample document in category: {category}
            Document number: {i+1}

            This is a demo document for batch upload testing.
            It contains information about {category}.

            Content: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            This document demonstrates the batch upload functionality of the
            Gemini RAG system.
            """)
            demo_files.append(file_path)
            print(f"   Created: {file_path}")

    # Scan directory
    print("\n2. Scanning directory for documents...")
    files = scan_directory(base_dir)
    print(f"   Found {len(files)} documents")

    # Create store
    print("\n3. Creating file search store...")
    store_name = rag.create_store("batch-upload-demo")
    print(f"   Store: {store_name}")

    # Batch upload
    print("\n4. Batch uploading documents...")
    operations = rag.batch_upload(
        file_paths=files,
        store_name=store_name,
        metadata_fn=extract_metadata_from_path
    )

    print(f"   Uploaded: {len(operations)}/{len(files)} documents")
    for i, op in enumerate(operations[:5], 1):  # Show first 5
        print(f"   [{i}] {op}")
    if len(operations) > 5:
        print(f"   ... and {len(operations) - 5} more")

    # Test queries
    print("\n5. Testing queries on uploaded documents...")

    test_queries = [
        "What categories of documents are available?",
        "Summarize the content about research papers",
        "What information is in the experiments category?"
    ]

    for query in test_queries:
        print(f"\n   Q: {query}")
        response = rag.query(query, store_name)
        print(f"   A: {response['answer'][:200]}...")

    # Statistics
    print("\n6. Upload Statistics:")
    print(f"   Total files scanned: {len(files)}")
    print(f"   Successfully uploaded: {len(operations)}")
    print(f"   Categories: {len(categories)}")

    by_category = {}
    for file_path in files:
        cat = file_path.parts[-2]
        by_category[cat] = by_category.get(cat, 0) + 1

    print("\n   Files by category:")
    for cat, count in by_category.items():
        print(f"   - {cat}: {count} files")

    # Cleanup
    print("\n7. Cleanup...")
    cleanup = input("   Delete demo files and store? (y/n): ").lower()
    if cleanup == 'y':
        rag.delete_store(store_name)

        # Remove all demo files
        for file_path in demo_files:
            file_path.unlink()

        # Remove directories
        for category in categories:
            (base_dir / category).rmdir()
        base_dir.rmdir()

        print("   Cleaned up")

    print("\n✓ Batch upload demo completed!")


if __name__ == "__main__":
    batch_upload_documents()
