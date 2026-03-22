"""
cag-service
===========
Cache-Augmented Generation as a Service.

Quick Start
-----------
    from cag_service import CAGCache, CAGEngine, OllamaBackend, Document

    cache = CAGCache(name="my-knowledge-base")
    cache.add(Document(id="DOC-1", title="Refund Policy", content="..."))

    engine = CAGEngine(cache=cache, backend=OllamaBackend("llama3.3"))
    response = engine.query("What is the refund window?")
    print(response.answer)
"""

from .core import CAGCache, CAGEngine, CAGResponse, Document
from .backends import (
    BaseLLMBackend,
    OllamaBackend,
    OpenAIBackend,
    AnthropicBackend,
    HuggingFaceBackend,
    create_backend,
)
from .loaders import (
    from_dict,
    from_dicts,
    from_string,
    from_text_file,
    from_markdown_file,
    from_json_file,
    from_directory,
    load_example_sops,
    load_example_customer_support,
)

__version__ = "1.0.0"
__author__  = "CAG Service Contributors"
__all__ = [
    # Core
    "CAGCache", "CAGEngine", "CAGResponse", "Document",
    # Backends
    "BaseLLMBackend", "OllamaBackend", "OpenAIBackend",
    "AnthropicBackend", "HuggingFaceBackend", "create_backend",
    # Loaders
    "from_dict", "from_dicts", "from_string",
    "from_text_file", "from_markdown_file", "from_json_file",
    "from_directory", "load_example_sops", "load_example_customer_support",
]
