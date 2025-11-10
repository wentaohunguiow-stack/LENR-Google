"""Upload all local files from my_local_files/ directory to RAG system."""

from pathlib import Path
from src.rag.gemini_rag import GeminiRAG
from datetime import datetime

def upload_all_local_files():
    """Upload all files from my_local_files/ to RAG."""

    print("\n" + "="*60)
    print("Local Files Upload Script")
    print("="*60 + "\n")

    # Initialize
    rag = GeminiRAG()

    # Create or use existing store
    store_name = rag.create_store("local-files-store")
    print(f"📦 Using store: {store_name}\n")

    # Define local directory
    local_dir = Path("my_local_files")

    if not local_dir.exists():
        print("❌ my_local_files/ directory not found!")
        print("\nCreate it first:")
        print("  mkdir my_local_files")
        print("\nThen add your files:")
        print("  cp your_files/*.pdf my_local_files/")
        return None

    # Count files
    all_files = list(local_dir.rglob("*"))
    file_count = sum(1 for f in all_files if f.is_file())

    if file_count == 0:
        print("❌ No files found in my_local_files/")
        print("\nAdd some files first:")
        print("  cp ~/Desktop/*.pdf my_local_files/")
        print("  cp ~/Documents/*.xlsx my_local_files/")
        return None

    print(f"📁 Found {file_count} files to upload\n")

    # Track uploads
    uploaded = []
    failed = []
    skipped = []

    # Upload all files
    for file_path in local_dir.rglob("*"):
        if not file_path.is_file():
            continue

        # Get file info
        suffix = file_path.suffix.lower()
        relative_path = file_path.relative_to(local_dir)
        category = relative_path.parts[0] if len(relative_path.parts) > 1 else "general"

        try:
            # Metadata
            metadata = {
                "category": category,
                "filename": file_path.name,
                "upload_date": datetime.now().strftime("%Y-%m-%d"),
                "local_path": str(relative_path)
            }

            # Upload based on file type
            if suffix in ['.xlsx', '.xls']:
                print(f"📊 Uploading Excel: {relative_path}")
                rag.upload_excel(
                    str(file_path),
                    store_name,
                    metadata=metadata,
                    conversion_format="markdown"
                )
                uploaded.append(file_path)

            elif suffix in ['.pdf', '.txt', '.md', '.docx', '.html']:
                print(f"📄 Uploading document: {relative_path}")
                rag.upload_file(
                    str(file_path),
                    store_name,
                    metadata=metadata
                )
                uploaded.append(file_path)

            else:
                print(f"⏭️  Skipping unsupported: {relative_path}")
                skipped.append(file_path)

        except Exception as e:
            print(f"❌ Error with {relative_path}: {e}")
            failed.append(file_path)

    # Summary
    print("\n" + "="*60)
    print("Upload Summary")
    print("="*60)
    print(f"✅ Successfully uploaded: {len(uploaded)} files")
    print(f"⏭️  Skipped (unsupported): {len(skipped)} files")
    print(f"❌ Failed: {len(failed)} files")

    if uploaded:
        print("\n📚 Uploaded files:")
        for f in uploaded[:10]:  # Show first 10
            print(f"   - {f.name}")
        if len(uploaded) > 10:
            print(f"   ... and {len(uploaded) - 10} more")

    if failed:
        print("\n❌ Failed files:")
        for f in failed:
            print(f"   - {f.name}")

    print(f"\n🏪 Store name: {store_name}")
    print("\n✓ Ready to query your local files!")

    return store_name


def test_upload(store_name):
    """Test that upload worked by querying."""

    if not store_name:
        return

    print("\n" + "="*60)
    print("Testing Upload")
    print("="*60 + "\n")

    try:
        rag = GeminiRAG()

        print("Asking: 'What files have been uploaded?'\n")

        response = rag.query(
            "What files have been uploaded? List the main topics or categories.",
            store_name,
            temperature=0.3
        )

        print("Answer:")
        print(response["answer"])

        if response['citations']:
            print(f"\n✓ Found {len(response['citations'])} source citations")
        else:
            print("\n⚠️ No citations found (this might be normal if query is general)")

    except Exception as e:
        print(f"❌ Error testing: {e}")


if __name__ == "__main__":
    # Upload all files
    store = upload_all_local_files()

    # Test if upload worked
    if store:
        test_upload(store)

        print("\n" + "="*60)
        print("Next Steps:")
        print("="*60)
        print("\n1. Query your files via web UI:")
        print("   streamlit run web_ui/app.py")
        print("\n2. Or query via Python:")
        print("   python -c \"from src.rag.gemini_rag import GeminiRAG; \\")
        print("   rag = GeminiRAG(); \\")
        print(f"   print(rag.query('Your question?', '{store}')['answer'])\"")
        print("\n3. To update files later:")
        print("   python sync_changes.py sync")
        print()
