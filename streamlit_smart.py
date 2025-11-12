"""
Smart RAG - Streamlit Web Interface
Simple, powerful, beautiful
"""

import streamlit as st
from pathlib import Path
import os
from src.rag.smart_rag import SmartRAG

# Page config
st.set_page_config(
    page_title="Smart RAG System",
    page_icon="🧠",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-box {
        padding: 15px;
        border-left: 4px solid #4CAF50;
        background-color: #f0f2f6;
        margin: 10px 0;
        border-radius: 4px;
    }
    .cost-badge {
        display: inline-block;
        padding: 4px 12px;
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 0.9rem;
    }
    .stat-card {
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG
@st.cache_resource
def init_rag():
    """Initialize Smart RAG system"""
    persist_dir = os.getenv("SMART_RAG_DB", "./smart_rag_db")
    return SmartRAG(persist_directory=persist_dir)

try:
    rag = init_rag()
    system_ready = True
except Exception as e:
    system_ready = False
    st.error(f"❌ System initialization failed: {e}")
    st.info("Please set OPENAI_API_KEY in .env file")
    st.code("echo 'OPENAI_API_KEY=your-key' > .env")
    st.stop()

# Header
st.markdown('<div class="main-header">🧠 Smart RAG System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Best balance of quality, cost, and simplicity • Only 1 API key needed</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ System Info")

    # Cost estimate
    st.markdown("### 💰 Cost")
    st.markdown("""
    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px;'>
        <b>Per Query:</b> ~$0.003<br>
        <b>1000 Queries:</b> ~$3-5/month<br>
        <b>Storage:</b> Free (local)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Collection Management
    st.header("📚 Collections")

    with st.expander("➕ Create Collection"):
        new_collection = st.text_input("Collection name", key="new_coll")
        if st.button("Create"):
            if new_collection:
                try:
                    rag.create_collection(new_collection)
                    st.success(f"✅ Created: {new_collection}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")

    # List collections
    try:
        collections = rag.list_collections()
        if collections:
            for col in collections:
                st.markdown(f"**{col['name']}** ({col['count']:,} docs)")
        else:
            st.info("No collections yet")
    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown("---")

    # System stats
    st.header("📊 Statistics")
    try:
        stats = rag.get_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Collections", stats['collections'])
            st.metric("Total Docs", f"{stats['total_documents']:,}")
        with col2:
            st.metric("DB Size", f"{stats['database_size_mb']:.1f} MB")
            st.metric("Files", stats['indexed_files'])
    except:
        pass

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Query", "📤 Upload", "📖 About", "🚀 Quick Start"])

# Tab 1: Query
with tab1:
    st.header("Ask Questions")

    collections = rag.list_collections()
    if not collections:
        st.warning("⚠️ No collections available. Create one and upload files first.")
    else:
        collection_names = [c['name'] for c in collections]
        selected_collection = st.selectbox("Select collection", collection_names)

        # Query input
        question = st.text_area("Your question:", height=100, placeholder="What are the key findings about LENR?")

        col1, col2, col3 = st.columns([2, 2, 6])
        with col1:
            n_results = st.number_input("# Sources", min_value=1, max_value=10, value=5)
        with col2:
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

        use_gpt4 = st.checkbox("Use GPT-4 Turbo (recommended)", value=True)
        if not use_gpt4:
            st.info("Using GPT-3.5 Turbo - Lower cost (~$0.001/query) but lower quality")

        if st.button("🔍 Search", type="primary"):
            if question:
                with st.spinner("Searching and generating answer..."):
                    try:
                        result = rag.query(
                            question,
                            collection_name=selected_collection,
                            n_results=n_results,
                            temperature=temperature,
                            use_gpt4=use_gpt4
                        )

                        # Cost estimate
                        cost = 0.003 if use_gpt4 else 0.001
                        st.markdown(f'<span class="cost-badge">Cost: ~${cost}</span>', unsafe_allow_html=True)
                        st.markdown("")

                        # Display answer
                        st.subheader("Answer:")
                        st.markdown(result['answer'])

                        # Display sources
                        st.subheader(f"📚 Sources ({result['n_sources']}):")
                        for i, source in enumerate(result['sources'], 1):
                            with st.expander(f"Source {i}: {source['filename']} (relevance: {source['relevance']:.3f})"):
                                st.markdown(f"**Chunk ID:** {source['chunk_id']}")
                                st.markdown(f"**Distance:** {source['distance']:.4f}")
                                st.markdown("**Content:**")
                                st.markdown(f'<div class="source-box">{source["text"]}</div>',
                                          unsafe_allow_html=True)

                        # Model info
                        st.caption(f"Model: {result['model']}")

                    except Exception as e:
                        st.error(f"❌ Query error: {e}")
            else:
                st.warning("Please enter a question")

# Tab 2: Upload
with tab2:
    st.header("Upload Files")

    collections = rag.list_collections()
    if not collections:
        st.warning("⚠️ Please create a collection first (see sidebar)")
    else:
        collection_names = [c['name'] for c in collections]
        target_collection = st.selectbox("Target collection", collection_names, key="upload_col")

        # File uploader
        uploaded_files = st.file_uploader(
            "Choose files",
            accept_multiple_files=True,
            type=['pdf', 'txt', 'md', 'docx', 'xlsx', 'xls']
        )

        col1, col2 = st.columns(2)
        with col1:
            chunk_size = st.number_input("Chunk size", min_value=500, max_value=3000, value=1000)
        with col2:
            chunk_overlap = st.number_input("Chunk overlap", min_value=50, max_value=500, value=200)

        if st.button("📤 Upload"):
            if uploaded_files:
                progress_bar = st.progress(0)
                total = len(uploaded_files)
                successful = 0
                total_chunks = 0
                total_cost = 0

                for idx, file in enumerate(uploaded_files):
                    st.write(f"Processing {file.name}...")

                    try:
                        # Save temporarily
                        temp_path = Path(f"/tmp/{file.name}")
                        with open(temp_path, 'wb') as f:
                            f.write(file.read())

                        # Upload to RAG
                        chunks = rag.upload_file(
                            temp_path,
                            collection_name=target_collection,
                            metadata={"filename": file.name},
                            chunk_size=chunk_size,
                            chunk_overlap=chunk_overlap
                        )

                        # Cleanup
                        temp_path.unlink()

                        if chunks > 0:
                            successful += 1
                            total_chunks += chunks
                            cost = chunks * 0.00002  # text-embedding-3-small
                            total_cost += cost
                            st.success(f"✅ {file.name}: {chunks} chunks (cost: ${cost:.4f})")
                        else:
                            st.info(f"⏭️ {file.name}: Already indexed (duplicate)")

                    except Exception as e:
                        st.error(f"❌ {file.name}: {e}")

                    progress_bar.progress((idx + 1) / total)

                st.markdown("---")
                st.success(f"✅ Upload complete!")
                st.write(f"**Files indexed:** {successful}/{total}")
                st.write(f"**Total chunks:** {total_chunks:,}")
                st.write(f"**Total cost:** ${total_cost:.4f}")
                st.balloons()
            else:
                st.warning("Please select files to upload")

# Tab 3: About
with tab3:
    st.header("About Smart RAG")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ## Why Smart RAG?

        **Simple:**
        - ✅ Only 1 API key (OpenAI)
        - ✅ 3-minute setup
        - ✅ Easy to use

        **Powerful:**
        - ✅ Unlimited storage (local)
        - ✅ GPT-4 Turbo quality
        - ✅ 1536-dim embeddings
        - ✅ Duplicate detection

        **Affordable:**
        - ✅ $3-5/month for 1000 queries
        - ✅ $0.003 per query
        - ✅ Free storage

        """)

    with col2:
        st.markdown("""
        ## Tech Stack

        **Embeddings:**
        - OpenAI text-embedding-3-small
        - 1536 dimensions
        - $0.02 per 1M tokens

        **Vector Database:**
        - ChromaDB (local)
        - Unlimited storage
        - Fast search

        **LLM:**
        - GPT-4 Turbo (default)
        - GPT-3.5 Turbo (optional)
        - Best quality answers

        **Storage:**
        - Local disk (your computer)
        - Export/import supported
        - No vendor lock-in
        """)

    st.markdown("---")

    st.markdown("""
    ## Comparison

    | Feature | Smart RAG | Enterprise RAG | Local RAG |
    |---------|-----------|----------------|-----------|
    | **API Keys** | 1 | 4 | 0-1 |
    | **Cost/Month** | $3-5 | $15 | $0-1 |
    | **Quality** | Excellent | Excellent | Good |
    | **Setup** | 3 min | 30 min | 10 min |
    | **Storage** | Unlimited | Unlimited | Unlimited |
    | **Best For** | Most users | Large teams | Privacy |

    **Smart RAG = Best balance**
    """)

    st.markdown("---")

    st.markdown("""
    ## Supported Files

    - **PDF** (.pdf)
    - **Text** (.txt, .md)
    - **Word** (.docx)
    - **Excel** (.xlsx, .xls)

    Maximum file size: Limited only by disk space
    """)

# Tab 4: Quick Start
with tab4:
    st.header("🚀 Quick Start Guide")

    st.markdown("""
    ## Complete Setup in 3 Steps

    ### Step 1: Get API Key
    ```bash
    # Go to: https://platform.openai.com/api-keys
    # Create new key and copy it
    ```

    ### Step 2: Install & Configure
    ```bash
    pip install -r requirements_smart.txt
    echo "OPENAI_API_KEY=your-key-here" > .env
    ```

    ### Step 3: Test
    ```bash
    python examples/test_smart_rag.py
    ```

    ---

    ## Index Your Files

    ### Automated (Recommended):
    ```bash
    # Put files in my_local_files/
    python index_smart.py
    ```

    ### Manual:
    Use the "📤 Upload" tab above

    ---

    ## Query Your Data

    ### Web Interface (This Page):
    Go to "💬 Query" tab

    ### Python:
    ```python
    from src.rag.smart_rag import SmartRAG

    rag = SmartRAG()
    result = rag.query("Your question", "my_docs")
    print(result['answer'])
    ```

    ---

    ## Share Database

    ### Export:
    ```bash
    python database_manager.py export ./smart_rag_db backup.tar.gz
    ```

    ### Share:
    Upload `backup.tar.gz` to Google Drive, Dropbox, etc.

    ### Import:
    ```bash
    python database_manager.py import backup.tar.gz ./smart_rag_db
    ```

    ---

    ## Deploy to Snowflake

    1. Upload files: `streamlit_smart.py`, `src/`, `requirements_smart.txt`
    2. Add secret: `OPENAI_API_KEY`
    3. Deploy!

    ---

    ## Cost Calculator

    **Per Query:**
    - Embedding: $0.00002
    - GPT-4 Turbo: $0.003
    - **Total: ~$0.003**

    **Monthly (1000 queries):**
    - Total: **~$3-5**

    **Indexing (7000 files):**
    - One-time: **~$0.70**

    ---

    ## Documentation

    - **START_HERE.md** - Main guide
    - **SMART_RAG_GUIDE.md** - Detailed reference
    - **OpenAI Docs** - https://platform.openai.com/docs
    """)

    st.success("📖 Read START_HERE.md for complete documentation")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <b>Smart RAG</b> • Simple • Powerful • Affordable<br>
    Only 1 API key • $3-5/month • GPT-4 quality
</div>
""", unsafe_allow_html=True)
