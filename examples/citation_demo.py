"""Demonstration of citation features without web UI."""

from pathlib import Path
from dotenv import load_dotenv

from src.rag.gemini_rag import GeminiRAG
from src.utils.citation_formatter import CitationFormatter

load_dotenv()


def demonstrate_citations():
    """Demonstrate interactive citation functionality."""

    print("=" * 70)
    print("Interactive Citations Demo")
    print("=" * 70)

    # Initialize RAG
    print("\n1. Initializing RAG system...")
    rag = GeminiRAG()

    # Create store
    print("\n2. Creating document store...")
    store_name = rag.create_store("citation-demo")
    print(f"   Store: {store_name}")

    # Create sample document with citations
    print("\n3. Creating sample research paper...")
    sample_doc = Path("sample_research_paper.txt")
    sample_doc.write_text("""
    Low-Energy Nuclear Reactions: A Comprehensive Review

    Abstract:
    Low-Energy Nuclear Reactions (LENR), sometimes referred to as cold fusion,
    represent a class of nuclear phenomena that occur at or near room temperature.
    This paper reviews the historical development, experimental methods, and
    theoretical models proposed to explain LENR phenomena.

    1. Introduction

    The field of LENR gained widespread attention in 1989 when Fleischmann and
    Pons announced their controversial cold fusion experiments. Since then,
    researchers worldwide have continued investigations into these phenomena,
    with varying degrees of success and skepticism from the scientific community.

    2. Historical Development

    The modern era of LENR research began in March 1989 with the announcement
    by Martin Fleischmann and Stanley Pons at the University of Utah. They
    reported excess heat production during electrolysis of heavy water with
    palladium electrodes. This announcement sparked both intense interest and
    controversy within the scientific community.

    Following the initial announcement, numerous replication attempts were made
    worldwide, with mixed results. Some laboratories reported positive results,
    while others failed to detect any anomalous effects. This lack of
    reproducibility became one of the major challenges facing the field.

    3. Experimental Methods

    3.1 Electrolytic Cells
    The most common experimental approach involves electrolysis of heavy water
    (D2O) using palladium or platinum cathodes. The process requires careful
    control of current density and temperature. Excess heat is measured using
    various calorimetric methods including isoperibolic, Seebeck, and flow
    calorimetry.

    3.2 Gas Loading
    An alternative method involves loading palladium or nickel with deuterium
    or hydrogen gas at elevated pressures. This approach allows for better
    control of loading conditions and can achieve higher deuterium-to-metal
    ratios.

    3.3 Plasma Methods
    Glow discharge and plasma electrolysis represent another category of
    experimental approaches. These methods involve lower current densities
    but can still achieve significant deuterium loading.

    4. Theoretical Models

    Several theoretical frameworks have been proposed to explain LENR:

    4.1 Lattice-Assisted Nuclear Reactions
    This model proposes that the metal lattice structure facilitates nuclear
    reactions by creating conditions that enhance tunneling probabilities
    through coherent effects.

    4.2 Neutron-Transfer Models
    These models suggest virtual neutron exchange between deuterium nuclei
    facilitated by the lattice environment.

    4.3 Widom-Larsen Theory
    This theory proposes that collective effects and weak interactions play
    a key role in LENR phenomena.

    5. Current Status and Challenges

    Despite decades of research, LENR remains controversial. The main challenges
    include:
    - Lack of consistent reproducibility
    - Absence of a widely accepted theoretical framework
    - Difficulty in detecting expected nuclear signatures
    - Need for more rigorous experimental protocols

    6. Conclusion

    LENR represents an intriguing area of research that continues to attract
    both supporters and critics. While some researchers report positive results,
    the field still faces significant challenges in achieving widespread
    scientific acceptance. Future work should focus on improving reproducibility
    and developing more comprehensive theoretical models.

    References:
    1. Fleischmann, M., Pons, S. (1989). "Electrochemically induced nuclear
       fusion of deuterium." Journal of Electroanalytical Chemistry.
    2. Storms, E. (2007). "The Science of Low Energy Nuclear Reaction."
       World Scientific Publishing.
    3. Widom, A., Larsen, L. (2006). "Ultra low momentum neutron catalyzed
       nuclear reactions on metallic hydride surfaces."
    """)

    print(f"   Created: {sample_doc}")

    # Upload document
    print("\n4. Uploading document to RAG system...")
    rag.upload_file(
        sample_doc,
        store_name,
        metadata={
            "type": "research_paper",
            "topic": "LENR",
            "year": "2024"
        }
    )
    print("   ✓ Document uploaded and indexed")

    # Query with citations
    print("\n5. Querying the document...")

    queries = [
        "Who were the pioneers of LENR research and when did they announce their findings?",
        "What are the main experimental methods used in LENR research?",
        "What theoretical models have been proposed to explain LENR?",
        "What are the current challenges facing LENR research?"
    ]

    for i, question in enumerate(queries, 1):
        print(f"\n{'=' * 70}")
        print(f"Query {i}: {question}")
        print('=' * 70)

        # Perform query
        response = rag.query(
            question,
            store_name,
            temperature=0.3  # Lower temperature for factual accuracy
        )

        # Format with citations
        formatted = CitationFormatter.format_response_with_citations(
            response['answer'],
            response['citations']
        )

        # Display answer
        print(f"\n📝 ANSWER:")
        print(f"{formatted['formatted_answer']}")

        # Display citations
        if formatted['references']:
            print(f"\n📚 REFERENCES ({formatted['citation_count']} sources):")
            print()

            for ref in formatted['references']:
                print(f"[{ref['number']}] {ref['title']}")

                # Show preview
                preview = ref['text'][:200] + "..." if len(ref['text']) > 200 else ref['text']
                print(f"    > {preview}")

                # Show metadata
                if ref['metadata']:
                    meta_str = " | ".join([f"{k}: {v}" for k, v in ref['metadata'].items()])
                    print(f"    {meta_str}")

                print()

        else:
            print("\n(No citations found)")

    # Generate markdown report
    print("\n6. Generating citation report...")

    # Perform comprehensive query
    comprehensive_response = rag.query(
        "Provide a comprehensive summary of LENR research including history, methods, and challenges",
        store_name,
        temperature=0.3,
        max_output_tokens=4096
    )

    formatted = CitationFormatter.format_response_with_citations(
        comprehensive_response['answer'],
        comprehensive_response['citations']
    )

    # Create markdown report
    report_md = CitationFormatter.create_reference_markdown(formatted['references'])

    report_file = Path("citation_report.md")
    report_file.write_text(f"""# LENR Research Summary with Citations

## Question
Provide a comprehensive summary of LENR research including history, methods, and challenges

## Answer

{formatted['formatted_answer']}

{report_md}

---

*Generated by LENR RAG System*
*Sources: {formatted['citation_count']} documents*
""")

    print(f"   ✓ Report saved to: {report_file}")

    # Cleanup
    print("\n7. Cleanup...")
    cleanup = input("   Delete demo files and store? (y/n): ").lower()
    if cleanup == 'y':
        rag.delete_store(store_name)
        sample_doc.unlink()
        if report_file.exists():
            report_file.unlink()
        print("   ✓ Cleaned up")

    print("\n" + "=" * 70)
    print("✓ Citation demo completed!")
    print("=" * 70)

    print("\n💡 Key Features Demonstrated:")
    print("  • Automatic citation extraction from RAG queries")
    print("  • Numbered reference formatting")
    print("  • Citation metadata tracking")
    print("  • Source excerpt preservation")
    print("  • Markdown report generation")
    print("\n🌐 Next Step: Try the web UI for interactive citations!")
    print("   Run: streamlit run web_ui/app.py")


if __name__ == "__main__":
    demonstrate_citations()
