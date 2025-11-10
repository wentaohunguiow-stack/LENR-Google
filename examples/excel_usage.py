"""Excel file integration example for Gemini RAG system."""

import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

from src.rag.gemini_rag import GeminiRAG
from src.utils.excel_handler import ExcelHandler

load_dotenv()


def create_sample_excel_files():
    """Create sample Excel files for demonstration."""
    examples_dir = Path("examples")

    # Sample 1: Sales data
    sales_data = {
        "Month": ["January", "February", "March", "April", "May", "June"],
        "Product_A_Sales": [12500, 13200, 14800, 15600, 16200, 17100],
        "Product_B_Sales": [8900, 9200, 10100, 10800, 11500, 12200],
        "Product_C_Sales": [6700, 7100, 7800, 8200, 8900, 9500],
        "Total_Revenue": [28100, 29500, 32700, 34600, 36600, 38800],
        "Region": ["North", "North", "South", "South", "East", "West"]
    }

    sales_df = pd.DataFrame(sales_data)
    sales_file = examples_dir / "sample_sales_data.xlsx"
    sales_df.to_excel(sales_file, index=False, sheet_name="Q1-Q2 Sales")

    # Add a second sheet with summary
    with pd.ExcelWriter(sales_file, mode='a', engine='openpyxl') as writer:
        summary_data = {
            "Product": ["Product A", "Product B", "Product C"],
            "Total_Sales": [89400, 62700, 48200],
            "Avg_Monthly_Sales": [14900, 10450, 8033],
            "Growth_Rate": ["12%", "15%", "18%"]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, index=False, sheet_name="Summary")

    print(f"Created: {sales_file}")

    # Sample 2: Research data
    research_data = {
        "Experiment_ID": ["EXP001", "EXP002", "EXP003", "EXP004", "EXP005"],
        "Temperature_C": [22, 25, 30, 35, 40],
        "Pressure_Bar": [1.0, 1.2, 1.5, 1.8, 2.0],
        "Reaction_Time_Min": [45, 38, 32, 28, 25],
        "Yield_Percent": [65.2, 72.4, 78.9, 82.1, 85.3],
        "Researcher": ["Alice", "Bob", "Alice", "Carol", "Bob"]
    }

    research_df = pd.DataFrame(research_data)
    research_file = examples_dir / "sample_research_data.xlsx"
    research_df.to_excel(research_file, index=False, sheet_name="Experiments")

    print(f"Created: {research_file}")

    return [sales_file, research_file]


def demonstrate_excel_integration():
    """Demonstrate Excel file integration with RAG."""

    print("=" * 60)
    print("Excel File Integration Demo")
    print("=" * 60)

    # Initialize RAG
    rag = GeminiRAG()

    # Create sample Excel files
    print("\n1. Creating sample Excel files...")
    excel_files = create_sample_excel_files()

    # Create store
    print("\n2. Creating file search store...")
    store_name = rag.create_store("excel-demo")
    print(f"   Store: {store_name}")

    # Explore Excel file structure
    print("\n3. Analyzing Excel files...")
    for excel_file in excel_files:
        summary = ExcelHandler.get_excel_summary(excel_file)
        print(f"\n   File: {summary['filename']}")
        print(f"   Size: {summary['file_size_mb']:.2f} MB")
        print(f"   Sheets: {summary['sheet_count']}")
        for sheet in summary['sheets']:
            print(f"     - {sheet['name']}: {sheet['rows']} rows × {sheet['columns']} columns")

    # Upload Excel files with different conversion formats
    print("\n4. Uploading Excel files to RAG system...")

    # Upload sales data as markdown (best for tables)
    print("\n   Uploading sales data (markdown format)...")
    rag.upload_excel(
        excel_files[0],
        store_name,
        metadata={
            "category": "sales",
            "period": "Q1-Q2",
            "year": "2024"
        },
        conversion_format="markdown"
    )

    # Upload research data as structured text (better for readability)
    print("   Uploading research data (text format)...")
    rag.upload_excel(
        excel_files[1],
        store_name,
        metadata={
            "category": "research",
            "experiment_type": "LENR",
            "year": "2024"
        },
        conversion_format="text"
    )

    print("   ✓ All Excel files uploaded successfully")

    # Query the Excel data
    print("\n5. Querying Excel data...")

    queries = [
        {
            "question": "What were the sales for Product A in March?",
            "category": "Sales Query"
        },
        {
            "question": "What is the total revenue trend from January to June?",
            "category": "Sales Analysis"
        },
        {
            "question": "Which experiment had the highest yield and what were its conditions?",
            "category": "Research Query"
        },
        {
            "question": "How does temperature affect reaction time in the experiments?",
            "category": "Research Analysis"
        },
        {
            "question": "Which region had sales in March and what were the total sales?",
            "category": "Regional Analysis"
        },
        {
            "question": "What is the average monthly sales for Product C?",
            "category": "Product Analysis"
        }
    ]

    for i, query_info in enumerate(queries, 1):
        print(f"\n   Query {i} [{query_info['category']}]:")
        print(f"   Q: {query_info['question']}")

        response = rag.query_excel_data(
            question=query_info['question'],
            store_name=store_name
        )

        print(f"   A: {response['answer']}")

        if response['citations']:
            print(f"   Sources: {len(response['citations'])} citations")

    # Demonstrate conversion preview
    print("\n6. Conversion format examples...")
    print("\n   Converting to Markdown:")
    markdown = ExcelHandler.excel_to_markdown(excel_files[0])
    print(markdown[:300] + "...\n")

    print("   Converting to Structured Text:")
    text = ExcelHandler.excel_to_structured_text(excel_files[1])
    print(text[:300] + "...\n")

    # Advanced: Batch upload multiple Excel files
    print("\n7. Advanced: Batch upload demonstration...")
    print("   Creating additional Excel files...")

    # Create more sample files
    additional_files = []
    for quarter in ["Q3", "Q4"]:
        data = {
            "Month": ["Jul", "Aug", "Sep"] if quarter == "Q3" else ["Oct", "Nov", "Dec"],
            "Sales": [40000, 42000, 44000] if quarter == "Q3" else [46000, 48000, 50000]
        }
        df = pd.DataFrame(data)
        file_path = Path("examples") / f"sample_{quarter}_data.xlsx"
        df.to_excel(file_path, index=False)
        additional_files.append(file_path)
        print(f"   Created: {file_path.name}")

    def metadata_generator(file_path):
        filename = Path(file_path).stem
        if "Q3" in filename:
            return {"quarter": "Q3", "year": "2024"}
        elif "Q4" in filename:
            return {"quarter": "Q4", "year": "2024"}
        return {}

    print("\n   Batch uploading...")
    operations = rag.batch_upload_excel(
        additional_files,
        store_name,
        conversion_format="text",
        metadata_fn=metadata_generator
    )
    print(f"   ✓ Uploaded {len(operations)} files")

    # Query across all uploaded data
    print("\n8. Querying across all Excel data...")
    response = rag.query_excel_data(
        "What is the sales trend across all quarters?",
        store_name
    )
    print(f"   Q: What is the sales trend across all quarters?")
    print(f"   A: {response['answer']}")

    # Cleanup
    print("\n9. Cleanup...")
    cleanup = input("   Delete demo files and store? (y/n): ").lower()
    if cleanup == 'y':
        rag.delete_store(store_name)

        # Delete all created Excel files
        for excel_file in excel_files + additional_files:
            if excel_file.exists():
                excel_file.unlink()

        print("   ✓ Cleaned up")

    print("\n" + "=" * 60)
    print("✓ Excel integration demo completed!")
    print("=" * 60)

    print("\n💡 Key Takeaways:")
    print("  • Excel files are automatically converted to searchable formats")
    print("  • Markdown format works best for preserving table structure")
    print("  • Text format is more readable for complex data")
    print("  • Metadata helps organize and filter Excel files")
    print("  • Use query_excel_data() for optimized structured data queries")


if __name__ == "__main__":
    demonstrate_excel_integration()
