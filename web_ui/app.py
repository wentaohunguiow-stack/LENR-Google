"""
Streamlit Web Interface for LENR Google RAG System.

Interactive interface with clickable citations, similar to OpenEvidence.
Run with: streamlit run web_ui/app.py
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.gemini_rag import GeminiRAG
from src.utils.citation_formatter import CitationFormatter
from src.utils.document_viewer import DocumentViewer, CitationNavigator
from dotenv import load_dotenv

load_dotenv()


# Page configuration
st.set_page_config(
    page_title="LENR RAG - Interactive Citations",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for citation styling
st.markdown("""
<style>
    .citation-link {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 2px 6px;
        border-radius: 3px;
        text-decoration: none;
        font-weight: 600;
        margin: 0 2px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .citation-link:hover {
        background-color: #1976d2;
        color: white;
    }
    .reference-item {
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #1976d2;
        background-color: #f5f5f5;
        border-radius: 4px;
    }
    .reference-number {
        font-weight: bold;
        color: #1976d2;
        font-size: 1.1em;
    }
    .reference-title {
        font-weight: 600;
        color: #333;
        margin: 5px 0;
    }
    .reference-preview {
        color: #666;
        font-size: 0.9em;
        font-style: italic;
        margin: 8px 0;
        padding: 8px;
        background-color: white;
        border-radius: 3px;
    }
    .reference-metadata {
        font-size: 0.85em;
        color: #999;
        margin-top: 5px;
    }
    .answer-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 20px 0;
    }
    .section-header {
        color: #1976d2;
        font-size: 1.3em;
        font-weight: 600;
        margin-top: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #1976d2;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'rag' not in st.session_state:
    try:
        st.session_state.rag = GeminiRAG()
        st.session_state.rag_initialized = True
    except ValueError as e:
        st.session_state.rag_initialized = False
        st.session_state.error = str(e)

if 'query_history' not in st.session_state:
    st.session_state.query_history = []

if 'current_store' not in st.session_state:
    st.session_state.current_store = None

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []


def display_citation_reference(ref: dict, ref_number: int):
    """Display a single citation reference with interactive elements."""
    with st.container():
        st.markdown(f"""
        <div class="reference-item" id="ref-{ref_number}">
            <span class="reference-number">[{ref_number}]</span>
            <div class="reference-title">{ref.get('title', 'Untitled Source')}</div>
        """, unsafe_allow_html=True)

        # Show preview text
        preview = ref.get('text', '')
        if preview:
            preview_text = preview[:300] + "..." if len(preview) > 300 else preview
            st.markdown(f'<div class="reference-preview">"{preview_text}"</div>', unsafe_allow_html=True)

        # Metadata
        metadata = ref.get('metadata', {})
        if metadata:
            meta_str = " | ".join([f"{k}: {v}" for k, v in metadata.items()])
            st.markdown(f'<div class="reference-metadata">{meta_str}</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Show full text in expander
        if preview:
            with st.expander("View full excerpt"):
                st.text(preview)

        # Link to source if available
        uri = ref.get('uri', '')
        if uri:
            st.markdown(f"[📄 View Source Document]({uri})")


def main():
    """Main application."""

    # Sidebar
    with st.sidebar:
        st.title("🔬 LENR RAG System")
        st.markdown("### Interactive Citations")

        if not st.session_state.rag_initialized:
            st.error("⚠️ RAG system not initialized")
            st.info("Please set GOOGLE_API_KEY in your .env file")
            return

        st.success("✅ System Ready")

        st.markdown("---")

        # Store management
        st.markdown("### Document Store")

        # List existing stores
        if st.button("🔄 Refresh Stores"):
            pass  # Will trigger re-render

        try:
            stores = st.session_state.rag.list_stores()
            store_options = [s['display_name'] for s in stores]

            if stores:
                selected_store_name = st.selectbox(
                    "Select Store",
                    options=store_options,
                    key="store_selector"
                )

                # Find full store name
                selected_store = next(
                    (s for s in stores if s['display_name'] == selected_store_name),
                    None
                )

                if selected_store:
                    st.session_state.current_store = selected_store['name']
                    st.info(f"Using: {selected_store_name}")
            else:
                st.warning("No stores found")

        except Exception as e:
            st.error(f"Error loading stores: {e}")

        # Create new store
        with st.expander("➕ Create New Store"):
            new_store_name = st.text_input("Store Name")
            if st.button("Create"):
                if new_store_name:
                    try:
                        store_name = st.session_state.rag.create_store(new_store_name)
                        st.success(f"Created: {new_store_name}")
                        st.session_state.current_store = store_name
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        # File upload
        with st.expander("📤 Upload Documents"):
            uploaded_files = st.file_uploader(
                "Choose files",
                accept_multiple_files=True,
                type=['pdf', 'txt', 'md', 'docx', 'xlsx', 'xls']
            )

            if uploaded_files and st.session_state.current_store:
                if st.button("Upload to Store"):
                    with st.spinner("Uploading..."):
                        for uploaded_file in uploaded_files:
                            # Save temporarily
                            temp_path = Path(f"/tmp/{uploaded_file.name}")
                            temp_path.write_bytes(uploaded_file.read())

                            try:
                                # Check file type and upload accordingly
                                if temp_path.suffix.lower() in ['.xlsx', '.xls']:
                                    st.session_state.rag.upload_excel(
                                        temp_path,
                                        st.session_state.current_store
                                    )
                                else:
                                    st.session_state.rag.upload_file(
                                        temp_path,
                                        st.session_state.current_store
                                    )

                                st.success(f"✅ Uploaded: {uploaded_file.name}")
                                st.session_state.uploaded_files.append(uploaded_file.name)

                            except Exception as e:
                                st.error(f"❌ Error uploading {uploaded_file.name}: {e}")
                            finally:
                                # Clean up
                                if temp_path.exists():
                                    temp_path.unlink()

        st.markdown("---")
        st.markdown("### Query Settings")

        model = st.selectbox(
            "Model",
            options=["gemini-2.5-flash", "gemini-2.5-pro"],
            index=0
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Lower = more focused, Higher = more creative"
        )

    # Main content area
    st.title("🔬 LENR Research Assistant")
    st.markdown("### Ask questions about your documents with interactive citations")

    if not st.session_state.current_store:
        st.info("👈 Please select or create a document store in the sidebar to get started")
        return

    # Query input
    query = st.text_area(
        "Ask your question:",
        height=100,
        placeholder="Example: What are the main experimental methods used in LENR research?"
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)

    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.query_history = []
            st.rerun()

    if search_button and query:
        with st.spinner("Searching documents..."):
            try:
                # Perform query
                if any(keyword in query.lower() for keyword in ['excel', 'data', 'table', 'spreadsheet']):
                    response = st.session_state.rag.query_excel_data(
                        query,
                        st.session_state.current_store,
                        model=model,
                        temperature=temperature
                    )
                else:
                    response = st.session_state.rag.query(
                        query,
                        st.session_state.current_store,
                        model=model,
                        temperature=temperature
                    )

                # Format citations
                formatted = CitationFormatter.format_response_with_citations(
                    response['answer'],
                    response['citations']
                )

                # Store in history
                st.session_state.query_history.insert(0, {
                    'query': query,
                    'response': response,
                    'formatted': formatted
                })

            except Exception as e:
                st.error(f"Error during search: {e}")
                return

    # Display results
    if st.session_state.query_history:
        latest = st.session_state.query_history[0]

        # Display answer
        st.markdown('<div class="section-header">Answer</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            st.markdown(latest['formatted']['formatted_answer'])

            if latest['formatted']['citation_count'] > 0:
                st.info(f"📚 {latest['formatted']['citation_count']} sources cited")

            st.markdown('</div>', unsafe_allow_html=True)

        # Display references
        if latest['formatted']['references']:
            st.markdown('<div class="section-header">References</div>', unsafe_allow_html=True)

            for ref in latest['formatted']['references']:
                display_citation_reference(ref, ref['number'])

        # Query details
        with st.expander("📊 Query Details"):
            st.write(f"**Model:** {latest['response'].get('model', 'N/A')}")
            st.write(f"**Query:** {latest['query']}")
            st.write(f"**Citations Found:** {len(latest['response']['citations'])}")

        st.markdown("---")

        # Previous queries
        if len(st.session_state.query_history) > 1:
            with st.expander(f"📜 Previous Queries ({len(st.session_state.query_history) - 1})"):
                for i, item in enumerate(st.session_state.query_history[1:], 1):
                    st.markdown(f"**{i}. {item['query'][:100]}...**")
                    st.write(item['formatted']['formatted_answer'][:200] + "...")
                    st.markdown("---")


if __name__ == "__main__":
    main()
