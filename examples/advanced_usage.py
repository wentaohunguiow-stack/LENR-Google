"""Advanced usage examples for Gemini RAG system."""

import os
from pathlib import Path
from dotenv import load_dotenv

from src.rag.gemini_rag import GeminiRAG

load_dotenv()


def create_sample_documents():
    """Create sample documents for testing."""
    docs_dir = Path("sample_docs")
    docs_dir.mkdir(exist_ok=True)

    documents = {
        "lenr_overview.txt": """
        LENR Overview Document

        Low-Energy Nuclear Reactions (LENR) represent a class of nuclear phenomena
        occurring at or near room temperature. Unlike hot fusion which requires
        millions of degrees, LENR experiments operate under much milder conditions.

        Historical Context:
        - 1989: Fleischmann-Pons experiment announced
        - 1990s: Widespread skepticism and reduced funding
        - 2000s: Renewed interest with new experimental approaches
        - 2010s: Private sector investment increases
        - 2020s: Continued research with improved diagnostics

        Key Concepts:
        - Deuterium loading in palladium or nickel
        - Anomalous heat production
        - Nuclear signatures (neutrons, tritium, transmutation)
        - Surface chemistry and nanostructures
        """,
        "experimental_methods.txt": """
        LENR Experimental Methods

        Various experimental approaches have been developed:

        1. Electrolytic Cells:
        - Heavy water electrolysis
        - Palladium or platinum cathodes
        - Current density optimization
        - Temperature monitoring

        2. Gas Loading:
        - High-pressure deuterium
        - Nickel or palladium powders
        - Thermal cycling
        - Pressure-composition isotherms

        3. Plasma Methods:
        - Glow discharge
        - Beam-target experiments
        - Plasma electrolysis

        Measurement Techniques:
        - Calorimetry (isoperibolic, Seebeck, flow)
        - Nuclear detection (neutrons, gammas, charged particles)
        - Mass spectrometry for isotope analysis
        - Surface analysis (SEM, XPS, SIMS)
        """,
        "theoretical_models.txt": """
        LENR Theoretical Models

        Several theoretical frameworks attempt to explain LENR:

        1. Lattice-Assisted Nuclear Reactions:
        - Deuterium in metal lattices
        - Enhanced tunneling probabilities
        - Coherent effects

        2. Neutron-Transfer Models:
        - Virtual neutron exchange
        - Compound nucleus formation

        3. Surface Plasmon Models:
        - Electromagnetic enhancement
        - Localized energy concentration

        4. Widom-Larsen Theory:
        - Collective effects
        - Weak interactions

        Challenges:
        - Lack of consistent theoretical framework
        - Difficulty explaining all observations
        - Need for quantum many-body calculations
        """
    }

    created_files = []
    for filename, content in documents.items():
        filepath = docs_dir / filename
        filepath.write_text(content)
        created_files.append(filepath)
        print(f"Created: {filepath}")

    return created_files


def demonstrate_advanced_features():
    """Demonstrate advanced RAG features."""

    print("=" * 60)
    print("Gemini RAG - Advanced Usage Demo")
    print("=" * 60)

    # Initialize
    rag = GeminiRAG()

    # Create documents
    print("\n1. Creating sample documents...")
    docs = create_sample_documents()

    # Create store
    print("\n2. Creating file search store...")
    store_name = rag.create_store("lenr-research-advanced")
    print(f"   Store created: {store_name}")

    # Batch upload with metadata function
    print("\n3. Batch uploading with custom metadata...")

    def generate_metadata(file_path):
        """Generate metadata based on filename."""
        name = Path(file_path).stem
        metadata = {
            "source": "demo",
            "language": "en"
        }

        if "overview" in name:
            metadata.update({"category": "introduction", "level": "basic"})
        elif "experimental" in name:
            metadata.update({"category": "methods", "level": "intermediate"})
        elif "theoretical" in name:
            metadata.update({"category": "theory", "level": "advanced"})

        return metadata

    operations = rag.batch_upload(
        file_paths=docs,
        store_name=store_name,
        metadata_fn=generate_metadata
    )
    print(f"   Uploaded {len(operations)} documents")

    # Query with different models and parameters
    print("\n4. Querying with different configurations...")

    queries = [
        {
            "question": "What are the main experimental methods used in LENR research?",
            "model": "gemini-2.5-flash",
            "temperature": 0.3,  # More focused
        },
        {
            "question": "Compare and contrast the different theoretical models of LENR",
            "model": "gemini-2.5-flash",
            "temperature": 0.7,  # More creative
        },
        {
            "question": "What is the historical timeline of LENR research?",
            "model": "gemini-2.5-flash",
            "temperature": 0.1,  # Very precise
        }
    ]

    for i, query_config in enumerate(queries, 1):
        print(f"\n   Query {i}:")
        print(f"   Q: {query_config['question']}")
        print(f"   Model: {query_config['model']}, Temp: {query_config['temperature']}")

        response = rag.query(
            question=query_config['question'],
            store_name=store_name,
            model=query_config['model'],
            temperature=query_config['temperature']
        )

        print(f"   A: {response['answer'][:300]}...")  # Truncate for display
        print(f"   Citations: {len(response['citations'])}")

    # Custom chunking configuration
    print("\n5. Uploading with custom chunking config...")
    custom_doc = Path("sample_docs/custom_chunk.txt")
    custom_doc.write_text("""
    This is a test document with custom chunking configuration.
    We can control how the document is split into chunks for better retrieval.
    Smaller chunks may provide more precise citations, while larger chunks
    provide more context. The overlap between chunks helps maintain continuity.
    """ * 10)  # Repeat to make it longer

    rag.upload_file(
        file_path=custom_doc,
        store_name=store_name,
        metadata={"type": "test"},
        chunking_config={
            "max_tokens_per_chunk": 512,  # Smaller chunks
            "max_overlap_tokens": 128      # More overlap
        }
    )
    print("   Uploaded with custom chunking")

    # Query with citation analysis
    print("\n6. Detailed citation analysis...")
    response = rag.query(
        question="What measurement techniques are used in LENR experiments?",
        store_name=store_name
    )

    print(f"   Answer: {response['answer']}")
    print(f"\n   Detailed Citations:")
    for i, citation in enumerate(response['citations'], 1):
        print(f"   [{i}] {citation.get('title', 'Untitled')}")
        if 'text' in citation:
            print(f"       Excerpt: {citation['text'][:100]}...")

    # Cleanup
    print("\n7. Cleanup...")
    cleanup = input("   Delete demo files and store? (y/n): ").lower()
    if cleanup == 'y':
        rag.delete_store(store_name)
        for doc in docs:
            doc.unlink()
        custom_doc.unlink()
        Path("sample_docs").rmdir()
        print("   Cleaned up")

    print("\n✓ Advanced demo completed!")


if __name__ == "__main__":
    demonstrate_advanced_features()
