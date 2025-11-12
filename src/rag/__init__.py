"""RAG implementations - Import only what's available based on installed dependencies"""

__all__ = []

# Try to import GeminiRAG
try:
    from src.rag.gemini_rag import GeminiRAG
    __all__.append("GeminiRAG")
except ImportError:
    pass

# Try to import LocalRAG
try:
    from src.rag.local_rag import LocalRAG
    __all__.append("LocalRAG")
except ImportError:
    pass

# Try to import EnterpriseRAG
try:
    from src.rag.enterprise_rag import EnterpriseRAG
    __all__.append("EnterpriseRAG")
except ImportError:
    pass

# Try to import SmartRAG
try:
    from src.rag.smart_rag import SmartRAG
    __all__.append("SmartRAG")
except ImportError:
    pass

# Try to import GeminiSmartRAG
try:
    from src.rag.gemini_smart_rag import GeminiSmartRAG
    __all__.append("GeminiSmartRAG")
except ImportError:
    pass
