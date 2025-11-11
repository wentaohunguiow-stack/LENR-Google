"""
Snowflake Streamlit App - Local RAG System
Entry file prepared for Snowflake deployment
"""

import streamlit as st
from pathlib import Path
import os
from src.rag.local_rag import LocalRAG

# Page config
st.set_page_config(
    page_title="Local RAG System",
    page_icon="🔬",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .source-box {
        padding: 15px;
        border-left: 4px solid #1f77b4;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG
@st.cache_resource
def init_rag():
    """Initialize RAG system"""
    # Snowflake uses /tmp for temporary storage
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "/tmp/chroma_db")

    return LocalRAG(
        api_key=st.secrets.get("GOOGLE_API_KEY", None),
        persist_directory=persist_dir,
        embedding_model="all-MiniLM-L6-v2"  # Fast model for Snowflake
    )

try:
    rag = init_rag()
    system_ready = True
except Exception as e:
    system_ready = False
    st.error(f"❌ System initialization failed: {e}")

# Header
st.markdown('<div class="main-header">🔬 Local RAG System</div>', unsafe_allow_html=True)
st.markdown("Fully local RAG system - No storage limits, all data processed locally")
st.markdown("---")

if not system_ready:
    st.stop()

# Sidebar
with st.sidebar:
    st.header("📚 Collection Management")

    # Create collection
    with st.expander("➕ Create Collection"):
        new_collection = st.text_input("Collection name")
        if st.button("Create"):
            if new_collection:
                try:
                    rag.create_collection(new_collection)
                    st.success(f"✅ Created: {new_collection}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    # List collections
    st.subheader("📂 Collections")
    try:
        collections = rag.list_collections()
        if collections:
            for col in collections:
                st.write(f"**{col['name']}** ({col['count']} docs)")
        else:
            st.info("No collections yet")
    except Exception as e:
        st.error(f"Error loading collections: {e}")

    # System stats
    st.markdown("---")
    st.subheader("📊 Statistics")
    try:
        stats = rag.get_stats()
        st.metric("Collections", stats['collections'])
        st.metric("Total Docs", stats['total_documents'])
        st.metric("DB Size (MB)", f"{stats['database_size_mb']:.2f}")
    except:
        pass

# Main area tabs
tab1, tab2, tab3 = st.tabs(["💬 Query", "📤 Upload", "ℹ️ Info"])

# Tab 1: Query
with tab1:
    st.header("Ask Questions")

    # Select collection
    collections = rag.list_collections()
    if not collections:
        st.warning("⚠️ No collections available. Please create one and upload files first.")
    else:
        collection_names = [c['name'] for c in collections]
        selected_collection = st.selectbox("Select collection", collection_names)

        # Query input
        question = st.text_area("Your question:", height=100)

        col1, col2, col3 = st.columns([2, 2, 6])
        with col1:
            n_results = st.number_input("# Sources", min_value=1, max_value=10, value=5)
        with col2:
            temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

        if st.button("🔍 Search", type="primary"):
            if question:
                with st.spinner("Searching..."):
                    try:
                        result = rag.query(
                            question,
                            collection_name=selected_collection,
                            n_results=n_results,
                            temperature=temperature
                        )

                        # Display answer
                        st.subheader("Answer:")
                        st.markdown(result['answer'])

                        # Display sources
                        st.subheader(f"📚 Sources ({result['n_sources']}):")
                        for i, source in enumerate(result['sources'], 1):
                            with st.expander(f"Source {i}: {source['filename']}"):
                                st.markdown(f"**Distance:** {source['distance']:.4f}")
                                st.markdown(f"**Chunk ID:** {source['chunk_id']}")
                                st.markdown("**Content:**")
                                st.markdown(f'<div class="source-box">{source["text"]}</div>',
                                          unsafe_allow_html=True)

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

                for idx, file in enumerate(uploaded_files):
                    st.write(f"Uploading {file.name}...")

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

                        st.success(f"✅ {file.name}: {chunks} chunks indexed")

                    except Exception as e:
                        st.error(f"❌ {file.name}: {e}")

                    progress_bar.progress((idx + 1) / total)

                st.balloons()
            else:
                st.warning("Please select files to upload")

# Tab 3: Info
with tab3:
    st.header("ℹ️ System Information")

    st.markdown("""
    ## Local RAG System

    ### Features:
    - ✅ **No storage limits** - Only limited by local disk space
    - ✅ **Local indexing** - Local embeddings and vector storage
    - ✅ **Uses Gemini** - Gemini API for answer generation only
    - ✅ **Fast search** - Local vector search
    - ✅ **Privacy** - All data stays local

    ### Tech Stack:
    - **Vector DB:** ChromaDB (local)
    - **Embeddings:** sentence-transformers (local)
    - **Generation:** Google Gemini API (optional)
    - **UI:** Streamlit

    ### Supported File Types:
    - PDF (`.pdf`)
    - Text (`.txt`, `.md`)
    - Word (`.docx`)
    - Excel (`.xlsx`, `.xls`)

    ### Workflow:
    1. Upload file → Extract text locally
    2. Chunk text → Generate embeddings locally
    3. Store in local ChromaDB
    4. Query → Local vector search
    5. Generate answer → Gemini API

    ### Snowflake Deployment Notes:
    - Data stored in `/tmp/chroma_db`
    - Data lost after app restart
    - Implement persistence solution (Snowflake Stage or Table)

    ### Documentation:
    - See `LOCAL_RAG_GUIDE.md` for details
    """)

    # Debug info
    with st.expander("🔧 Debug Info"):
        st.json({
            "persist_directory": rag.persist_directory,
            "embedding_model": rag.embedding_model,
            "has_api_key": rag.api_key is not None,
            "collections": len(rag.list_collections())
        })
