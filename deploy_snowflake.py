"""
Helper script for deploying to Snowflake Streamlit
"""

import os
import shutil
from pathlib import Path

def prepare_snowflake_deployment():
    """Prepare files needed for Snowflake deployment"""

    print("=" * 60)
    print("Preparing Snowflake Streamlit Deployment")
    print("=" * 60)
    print()

    # Create deployment directory
    deploy_dir = Path("./snowflake_deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()

    print("1. Creating deployment directory...")
    print(f"   ✓ {deploy_dir}")
    print()

    # Copy necessary files
    print("2. Copying necessary files...")

    files_to_copy = [
        "streamlit_gemini.py",
        "requirements_gemini.txt",
        "environment.yml",
    ]

    for file in files_to_copy:
        src = Path(file)
        if src.exists():
            shutil.copy(src, deploy_dir / file)
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} (not found)")

    # Copy src directory
    src_dir = Path("src")
    if src_dir.exists():
        shutil.copytree(src_dir, deploy_dir / "src")
        print(f"   ✓ src/")
    else:
        print(f"   ✗ src/ (not found)")

    print()

    # Modify streamlit_gemini.py for Snowflake compatibility
    print("3. Modifying streamlit_gemini.py for Snowflake compatibility...")
    streamlit_file = deploy_dir / "streamlit_gemini.py"

    if streamlit_file.exists():
        with open(streamlit_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add Snowflake compatibility header
        snowflake_header = '''"""
Gemini Smart RAG - Snowflake Streamlit Version
"""

import streamlit as st
import os

# Snowflake adaptation: use secrets instead of .env
def get_google_api_key():
    """Get API key from Snowflake secrets or environment variable"""
    try:
        # Try to get from Snowflake secrets
        return st.secrets["GOOGLE_API_KEY"]
    except:
        # Fallback to environment variable
        return os.getenv("GOOGLE_API_KEY")

# Override original environment variable retrieval
os.environ['GOOGLE_API_KEY'] = get_google_api_key() or ""

# Use temporary directory for database storage
SNOWFLAKE_TEMP_DIR = "/tmp/gemini_smart_rag_db"

'''

        # Insert header
        if "import streamlit as st" not in content[:200]:
            content = snowflake_header + "\n" + content
        else:
            # Replace part after import statement
            import_idx = content.find("import streamlit as st")
            next_line = content.find("\n", import_idx) + 1
            content = content[:next_line] + snowflake_header + content[next_line:]

        # Save modified file
        with open(streamlit_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("   ✓ Added Snowflake compatibility code")
    else:
        print("   ✗ streamlit_gemini.py not found")

    print()

    # Create README
    print("4. Creating Snowflake deployment README...")
    readme_content = """# Snowflake Deployment Guide

## Deployment Steps

### 1. Login to Snowflake
Visit: https://app.snowflake.com/

### 2. Create Streamlit App
1. Click "Streamlit" → "Create"
2. Select "From scratch"

### 3. Upload Files
Upload the following files to Snowflake:
- `streamlit_gemini.py` (main application file)
- `src/` (entire folder)
- `environment.yml` (dependency configuration)

### 4. Configure Secrets
Add in Snowflake Streamlit settings:

```toml
GOOGLE_API_KEY = "your-google-api-key-here"
```

Get API key: https://aistudio.google.com/apikey

### 5. Deploy
Click the "Deploy" button and wait 1-2 minutes to complete.

## Important Notes

1. **Data Persistence**:
   - Snowflake uses temporary storage (`/tmp`)
   - Data will be lost on app restart
   - Recommend pre-indexing database and uploading

2. **Upload Pre-indexed Database**:
   ```bash
   # Index locally
   python index_gemini.py

   # Export database
   python database_manager.py export ./gemini_smart_rag_db db.tar.gz

   # Upload db.tar.gz to Snowflake Stage
   ```

3. **Performance Considerations**:
   - First query may be slow (cold start)
   - Recommend using small test dataset

## FAQ

**Q: What if database is lost?**
A: Use Snowflake Stage to store pre-indexed database, load automatically on startup.

**Q: How to update app?**
A: Edit files directly in Snowflake UI, saves and redeploys automatically.

**Q: Does it support multiple users?**
A: Yes, but all users share the same database.
"""

    readme_file = deploy_dir / "SNOWFLAKE_README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("   ✓ SNOWFLAKE_README.md")
    print()

    # Completion
    print("=" * 60)
    print("✓ Preparation Complete!")
    print("=" * 60)
    print()
    print("Deployment files location:")
    print(f"  {deploy_dir.absolute()}")
    print()
    print("Next steps:")
    print("  1. Visit https://app.snowflake.com/")
    print("  2. Upload files from snowflake_deploy/")
    print("  3. Configure GOOGLE_API_KEY secret")
    print("  4. Click Deploy")
    print()
    print("For detailed instructions, see:")
    print(f"  {readme_file.absolute()}")
    print()


if __name__ == "__main__":
    prepare_snowflake_deployment()
