"""
Gemini Smart RAG - Streamlit Web Interface
Simple, powerful, beautiful - powered by Gemini
"""

import streamlit as st
from pathlib import Path
import os
from src.rag.gemini_smart_rag import GeminiSmartRAG

# Page config
st.set_page_config(
    page_title="Gemini Smart RAG",
    page_icon="💎",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4285F4;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-box {
        padding: 15px;
        border-left: 4px solid #4285F4;
        background-color: #f0f2f6;
        margin: 10px 0;
        border-radius: 4px;
    }
    .cost-badge {
        display: inline-block;
        padding: 4px 12px;
        background-color: #34A853;
        color: white;
        border-radius: 12px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG
@st.cache_resource
def init_rag():
    """Initialize Gemini Smart RAG system"""
    persist_dir = os.getenv("GEMINI_SMART_RAG_DB", "./gemini_smart_rag_db")
    return GeminiSmartRAG(persist_directory=persist_dir)

try:
    rag = init_rag()
    system_ready = True
except Exception as e:
    system_ready = False
    st.error(f"❌ System initialization failed: {e}")
    st.info("Please set GOOGLE_API_KEY in .env file")
    st.code("echo 'GOOGLE_API_KEY=your-key' > .env")
    st.stop()

# Header
st.markdown('<div class="main-header">💎 Gemini Smart RAG</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Google Gemini • Only 1 API key • FREE embeddings • $0.50/month</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ System Info")

    # Cost estimate
    st.markdown("### 💰 Cost (Lowest!)")
    st.markdown("""
    <div style='background-color: #E8F5E9; padding: 15px; border-radius: 8px;'>
        <b>Embeddings:</b> FREE ✨<br>
        <b>Per Query:</b> ~$0.0005<br>
        <b>1000 Queries:</b> ~$0.50-1/month<br>
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

        col1, col2 = st.columns([2, 8])
        with col1:
            n_results = st.number_input("# Sources", min_value=1, max_value=10, value=5)
        with col2:
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

        if st.button("🔍 Search", type="primary"):
            if question:
                with st.spinner("Searching with Gemini..."):
                    try:
                        result = rag.query(
                            question,
                            collection_name=selected_collection,
                            n_results=n_results,
                            temperature=temperature
                        )

                        # Cost estimate
                        st.markdown('<span class="cost-badge">Cost: ~$0.0005 (FREE embeddings!)</span>', unsafe_allow_html=True)
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
                            st.success(f"✅ {file.name}: {chunks} chunks (cost: FREE!)")
                        else:
                            st.info(f"⏭️ {file.name}: Already indexed (duplicate)")

                    except Exception as e:
                        st.error(f"❌ {file.name}: {e}")

                    progress_bar.progress((idx + 1) / total)

                st.markdown("---")
                st.success(f"✅ Upload complete!")
                st.write(f"**Files indexed:** {successful}/{total}")
                st.write(f"**Total chunks:** {total_chunks:,}")
                st.write(f"**Total cost:** FREE (Gemini embeddings)")
                st.balloons()
            else:
                st.warning("Please select files to upload")

# Tab 3: About
with tab3:
    st.header("About Gemini Smart RAG")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ## Why Gemini Smart RAG?

        **Simplest:**
        - ✅ Only 1 API key (Google)
        - ✅ 3-minute setup
        - ✅ Easy to use

        **Cheapest:**
        - ✅ FREE embeddings
        - ✅ $0.0005 per query
        - ✅ $0.50-1/month total
        - ✅ Free storage

        **Powerful:**
        - ✅ Unlimited storage (local)
        - ✅ Gemini 2.0 Flash quality
        - ✅ 768-dim embeddings
        - ✅ Duplicate detection
        - ✅ 2M token context

        """)

    with col2:
        st.markdown("""
        ## Tech Stack

        **Embeddings:**
        - Google text-embedding-004
        - 768 dimensions
        - **FREE!** ✨

        **Vector Database:**
        - ChromaDB (local)
        - Unlimited storage
        - Fast search

        **LLM:**
        - Gemini 2.0 Flash
        - $0.0005 per query
        - 2M token context
        - Excellent quality

        **Storage:**
        - Local disk (your computer)
        - Export/import supported
        - No vendor lock-in
        """)

    st.markdown("---")

    st.markdown("""
    ## Comparison

    | Feature | Gemini Smart RAG | OpenAI Smart RAG | Enterprise RAG |
    |---------|------------------|------------------|----------------|
    | **API Keys** | 1 | 1 | 4 |
    | **Cost/Month** | $0.50-1 | $3-5 | $15 |
    | **Embeddings** | FREE | $0.02/1M | Paid |
    | **Quality** | Excellent | Excellent | Excellent |
    | **Setup** | 3 min | 3 min | 30 min |
    | **Storage** | Unlimited | Unlimited | Unlimited |

    **Gemini Smart RAG = Cheapest option with excellent quality!**
    """)

# Tab 4: Quick Start
with tab4:
    st.header("🚀 Quick Start Guide")

    st.markdown("""
    ## Complete Setup in 3 Steps

    ### Step 1: Get API Key
    ```bash
    # Go to: https://aistudio.google.com/apikey
    # Click "Create API key"
    # Copy the key
    ```

    ### Step 2: Install & Configure
    ```bash
    pip install -r requirements_gemini.txt
    echo "GOOGLE_API_KEY=your-key-here" > .env
    ```

    ### Step 3: Test
    ```bash
    python examples/test_gemini_smart_rag.py
    ```

    ---

    ## Index Your Files

    ### Automated (Recommended):
    ```bash
    # Put files in my_local_files/
    python index_gemini.py
    ```

    ### Manual:
    Use the "📤 Upload" tab above

    ---

    ## Query Your Data

    ### Web Interface (This Page):
    Go to "💬 Query" tab

    ### Python:
    ```python
    from src.rag.gemini_smart_rag import GeminiSmartRAG

    rag = GeminiSmartRAG()
    result = rag.query("Your question", "my_docs")
    print(result['answer'])
    ```

    ---

    ## Cost Calculator

    **Embeddings:**
    - FREE! ✨

    **Per Query:**
    - Gemini 2.0 Flash: $0.0005
    - **Total: ~$0.0005**

    **Monthly (1000 queries):**
    - **Total: ~$0.50-1**

    **Indexing (7000 files):**
    - **FREE!** ✨

    ---

    ## Why Choose Gemini?

    1. **Cheapest:** FREE embeddings + lowest query cost
    2. **Simple:** Only 1 API key needed
    3. **Quality:** Gemini 2.0 Flash is excellent
    4. **Context:** 2M tokens (very long documents)
    5. **Multimodal:** Can handle images (future feature)

    ---

    ## Documentation

    - **START_GEMINI.md** - Complete guide
    - **Google AI Studio** - https://aistudio.google.com/
    """)

    st.success("📖 Read START_GEMINI.md for complete documentation")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <b>Gemini Smart RAG</b> • Powered by Google Gemini<br>
    Only 1 API key • FREE embeddings • $0.50/month • Excellent quality
</div>
""", unsafe_allow_html=True)
