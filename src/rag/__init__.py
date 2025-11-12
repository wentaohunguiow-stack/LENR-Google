"""RAG implementations - Gemini-focused"""

__all__ = []

# Gemini Smart RAG - Recommended solution
try:
    from src.rag.gemini_smart_rag import GeminiSmartRAG
    __all__.append("GeminiSmartRAG")
except ImportError:
    pass

# Original Gemini RAG (for reference)
try:
    from src.rag.gemini_rag import GeminiRAG
    __all__.append("GeminiRAG")
except ImportError:
    pass

# Local RAG (alternative for privacy-focused users)
try:
    from src.rag.local_rag import LocalRAG
    __all__.append("LocalRAG")
except ImportError:
    pass
