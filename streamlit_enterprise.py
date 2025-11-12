"""
Enterprise RAG Streamlit App
Best-in-class components for production use
"""

import streamlit as st
from pathlib import Path
import os
from src.rag.enterprise_rag import EnterpriseRAG

# Page config
st.set_page_config(
    page_title="Enterprise RAG System",
    page_icon="🚀",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(120deg, #2962ff, #00bcd4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .source-box {
        padding: 15px;
        border-left: 4px solid #2962ff;
        background-color: #f5f7fa;
        margin: 10px 0;
        border-radius: 5px;
    }
    .metric-card {
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG
@st.cache_resource
def init_rag():
    """Initialize Enterprise RAG system"""
    return EnterpriseRAG(
        openai_api_key=st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY")),
        pinecone_api_key=st.secrets.get("PINECONE_API_KEY", os.getenv("PINECONE_API_KEY")),
        cohere_api_key=st.secrets.get("COHERE_API_KEY", os.getenv("COHERE_API_KEY")),
        anthropic_api_key=st.secrets.get("ANTHROPIC_API_KEY", os.getenv("ANTHROPIC_API_KEY")),
        index_name=st.secrets.get("PINECONE_INDEX", os.getenv("PINECONE_INDEX", "enterprise-rag"))
    )

try:
    rag = init_rag()
    system_ready = True
except Exception as e:
    system_ready = False
    st.error(f"❌ System initialization failed: {e}")
    st.info("""
    Please configure API keys in `.env` file or Streamlit secrets:
    - OPENAI_API_KEY
    - PINECONE_API_KEY
    - COHERE_API_KEY (optional)
    - ANTHROPIC_API_KEY (optional)
    """)

# Header
st.markdown('<div class="main-header">🚀 Enterprise RAG System</div>', unsafe_allow_html=True)
st.markdown("""
Premium RAG with best-in-class components:
**OpenAI** embeddings • **Pinecone** vector DB • **Cohere** reranking • **Claude 3.5** LLM
""")
st.markdown("---")

if not system_ready:
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ System Status")

    # Get stats
    try:
        stats = rag.get_stats()
        st.metric("Total Vectors", f"{stats['total_vectors']:,}")
        st.metric("Dimensions", stats['dimension'])
        st.metric("Index Fullness", f"{stats['index_fullness']:.1%}")
    except:
        st.warning("Unable to load stats")

    st.markdown("---")

    st.subheader("💎 Premium Features")
    st.markdown("""
    - ✅ 3072-dim embeddings
    - ✅ Unlimited scale
    - ✅ Smart reranking
    - ✅ Claude 3.5 Sonnet
    - ✅ 99.9% uptime
    - ✅ Auto-scaling
    """)

    st.markdown("---")

    st.subheader("📊 Cost Estimate")
    st.markdown("""
    **Per Query:**
    - Embedding: $0.00001
    - Search: $0
    - Reranking: $0.002
    - LLM: $0.006

    **Total:** ~$0.01/query
    """)

# Main tabs
tab1, tab2, tab3 = st.tabs(["💬 Query", "📤 Upload", "📈 Analytics"])

# Tab 1: Query
with tab1:
    st.header("Ask Questions")

    question = st.text_area(
        "Your question:",
        height=100,
        placeholder="Ask anything about your documents..."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        top_k = st.number_input("Initial results", min_value=5, max_value=50, value=20)
    with col2:
        rerank_top_k = st.number_input("Final results", min_value=1, max_value=20, value=5)
    with col3:
        use_reranking = st.checkbox("Use reranking", value=True)
    with col4:
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

    if st.button("🔍 Search", type="primary", use_container_width=True):
        if question:
            with st.spinner("Searching with premium AI..."):
                try:
                    result = rag.query(
                        question,
                        top_k=top_k,
                        rerank_top_k=rerank_top_k,
                        use_reranking=use_reranking,
                        temperature=temperature
                    )

                    # Display answer
                    st.subheader("Answer:")
                    st.markdown(f'<div class="source-box">{result["answer"]}</div>',
                              unsafe_allow_html=True)

                    # Display model used
                    st.caption(f"Model: {result.get('model', 'Unknown')}")

                    # Display sources
                    st.subheader(f"📚 Sources ({result['n_sources']}):")

                    for i, source in enumerate(result['sources'], 1):
                        with st.expander(
                            f"Source {i}: {source['filename']} "
                            f"(Score: {source.get('rerank_score', source.get('score', 0)):.3f})"
                        ):
                            st.markdown(f"**Chunk ID:** {source['chunk_id']}")

                            if 'rerank_score' in source:
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Vector Score", f"{source['score']:.3f}")
                                with col2:
                                    st.metric("Rerank Score", f"{source['rerank_score']:.3f}")

                            st.markdown("**Content:**")
                            st.markdown(f'<div class="source-box">{source["text"]}</div>',
                                      unsafe_allow_html=True)

                    # Show cost estimate
                    st.info(f"💰 Estimated cost for this query: ~$0.01")

                except Exception as e:
                    st.error(f"❌ Query error: {e}")
        else:
            st.warning("Please enter a question")

# Tab 2: Upload
with tab2:
    st.header("Upload Files")

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

    if st.button("📤 Upload to Enterprise RAG"):
        if uploaded_files:
            progress_bar = st.progress(0)
            total = len(uploaded_files)
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
                        metadata={"filename": file.name},
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )

                    # Cleanup
                    temp_path.unlink()

                    # Estimate cost
                    cost = chunks * 0.00001  # Rough estimate
                    total_cost += cost
                    total_chunks += chunks

                    st.success(f"✅ {file.name}: {chunks} chunks indexed (~${cost:.4f})")

                except Exception as e:
                    st.error(f"❌ {file.name}: {e}")

                progress_bar.progress((idx + 1) / total)

            st.balloons()
            st.info(f"💰 Total indexing cost: ~${total_cost:.2f}")
            st.success(f"✅ Uploaded {total_chunks} total chunks")

        else:
            st.warning("Please select files to upload")

# Tab 3: Analytics
with tab3:
    st.header("📈 System Analytics")

    try:
        stats = rag.get_stats()

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Vectors",
                f"{stats['total_vectors']:,}",
                help="Number of embedded chunks"
            )
        with col2:
            st.metric(
                "Embedding Dimensions",
                stats['dimension'],
                help="Vector size (3072 for text-embedding-3-large)"
            )
        with col3:
            st.metric(
                "Index Fullness",
                f"{stats['index_fullness']:.1%}",
                help="Percentage of index capacity used"
            )

        st.markdown("---")

        # Cost estimates
        st.subheader("💰 Cost Estimates")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Monthly Storage:**")
            storage_gb = (stats['total_vectors'] * 12 * 1024) / (1024**3)  # Rough estimate
            storage_cost = storage_gb * 0.045
            st.metric("Storage Size", f"{storage_gb:.2f} GB")
            st.metric("Storage Cost", f"${storage_cost:.2f}/month")

        with col2:
            st.markdown("**Query Costs:**")
            queries_per_month = st.number_input("Queries/month", value=1000, step=100)
            query_cost = queries_per_month * 0.01
            st.metric("Total Query Cost", f"${query_cost:.2f}/month")

        st.info(f"💰 Total estimated monthly cost: ~${storage_cost + query_cost:.2f}")

    except Exception as e:
        st.error(f"Error loading analytics: {e}")

    st.markdown("---")

    # System info
    st.subheader("ℹ️ System Information")

    st.markdown("""
    ## Enterprise RAG System

    ### Premium Components:

    **Embeddings: OpenAI text-embedding-3-large**
    - 3072 dimensions (highest quality)
    - Cost: $0.13 per 1M tokens
    - Best semantic understanding

    **Vector Database: Pinecone Serverless**
    - Unlimited scale
    - Auto-scaling
    - 99.9% uptime SLA
    - Cost: $0.045 per GB/month

    **Reranking: Cohere rerank-english-v3.0**
    - 2x better relevance
    - Smart context understanding
    - Cost: $2 per 1K searches

    **LLM: Claude 3.5 Sonnet**
    - 200K context window
    - Best reasoning capabilities
    - Cost: $3 per 1M input tokens

    ### Features:

    - ✅ Unlimited scale (millions of documents)
    - ✅ Best quality (3072-dim embeddings)
    - ✅ Smart reranking (highest relevance)
    - ✅ Production-ready (99.9% uptime)
    - ✅ Easy sharing (cloud-based)
    - ✅ Fast (<5s per query)

    ### Support:

    - [OpenAI Documentation](https://platform.openai.com/docs)
    - [Pinecone Documentation](https://docs.pinecone.io)
    - [Cohere Documentation](https://docs.cohere.com)
    - [Anthropic Documentation](https://docs.anthropic.com)
    """)

    # Debug info
    with st.expander("🔧 Debug Info"):
        st.json({
            "index_name": rag.index_name,
            "embedding_model": rag.embedding_model,
            "embedding_dim": rag.embedding_dim,
            "llm_model": rag.llm_model if rag.anthropic_client else "None",
            "has_openai": rag.openai_client is not None,
            "has_pinecone": rag.index is not None,
            "has_cohere": rag.cohere_client is not None,
            "has_anthropic": rag.anthropic_client is not None,
            "stats": stats
        })
