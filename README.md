# ⚡ cag-service

> **Cache-Augmented Generation (CAG) as a Service**
> Pre-load your knowledge. Query with any LLM. Zero retrieval latency.

[![CI](https://github.com/yourorg/cag-service/actions/workflows/ci.yml/badge.svg)](https://github.com/yourorg/cag-service/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cag-service)](https://pypi.org/project/cag-service/)

---

## What is CAG?

**Cache-Augmented Generation (CAG)** is an alternative to Retrieval-Augmented Generation (RAG) for bounded knowledge bases.

Instead of retrieving documents at query time, CAG **pre-compiles your entire knowledge corpus into the LLM's context window at startup**. The result:

| | RAG | **CAG** |
|--|-----|---------|
| Retrieval latency | ✅ Low (top-k only) | ✅ **Zero** |
| Recall accuracy | ⚠️ Depends on embeddings | ✅ **Perfect within corpus** |
| Chunking errors | ⚠️ Common | ✅ **None** |
| Infrastructure | ❌ Vector DB + embeddings | ✅ **Just the LLM** |
| Best for | Large, dynamic corpora | **Bounded, curated knowledge** |

**Sweet spots for CAG:** SOPs, runbooks, compliance docs, product FAQs, API references — anything that fits in a modern LLM's context window (32k–128k tokens).

---

## Features

- 📚 **Multi-format loaders** — `.txt`, `.md`, `.json`, directories, or plain Python dicts
- 🔌 **4 LLM backends** — Ollama (local), OpenAI, Anthropic Claude, HuggingFace
- ⚡ **FastAPI REST service** — drop-in microservice with Swagger docs
- 🐳 **Docker + Compose** — one-command deployment including Ollama
- 🔄 **Hot-reload cache** — add/remove documents at runtime via API
- 🌊 **Streaming support** — SSE streaming endpoint for real-time UX
- 🧪 **Full test suite** — pytest, no live LLM required for core tests
- 📦 **pip installable** — use as a library or run as a service

---

## Quick Start

### As a Python library

```bash
pip install cag-service[ollama]
```

```python
from cag_service import CAGCache, CAGEngine, OllamaBackend, Document

# 1. Build a cache
cache = CAGCache(name="support-kb")
cache.add(Document(
    id="SOP-001",
    title="VPN Troubleshooting",
    content="Update VPN client to v5.x. Re-import .ovpn profile. Flush DNS...",
    tags=["network", "vpn"],
))

# 2. Create engine
engine = CAGEngine(cache=cache, backend=OllamaBackend("llama3.3"))

# 3. Query
response = engine.query("User can't connect to VPN after laptop replacement.")
print(response.answer)
# → "Based on SOP-001, ask the user to update their VPN client to v5.x and re-import..."
```

### As a REST API (Docker)

```bash
# Clone
git clone https://github.com/yourorg/cag-service.git
cd cag-service

# Launch (pulls Ollama + llama3.3 automatically)
docker-compose up

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I fix ORA-01555?"}'
```

API docs available at `http://localhost:8000/docs`

### Without Docker

```bash
pip install -r requirements.txt

# Set your backend
export CAG_PROVIDER=ollama        # or openai / anthropic / huggingface
export CAG_MODEL=llama3.3
export OLLAMA_HOST=http://localhost:11434

# Start Ollama (separate terminal)
ollama serve && ollama pull llama3.3

# Start the API
uvicorn cag_service.api:app --host 0.0.0.0 --port 8000 --reload
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Health check |
| `GET`  | `/cache/stats` | Cache metadata (doc count, token estimate, version) |
| `GET`  | `/cache/documents` | List all documents |
| `POST` | `/cache/documents` | Add a document (hot-reload) |
| `DELETE` | `/cache/documents/{id}` | Remove a document |
| `POST` | `/query` | CAG query — returns full response |
| `POST` | `/query/stream` | CAG query — Server-Sent Events stream |

### POST /query

```json
{
  "question": "What is the refund policy?",
  "history":  [],
  "temperature": 0.2
}
```

Response:

```json
{
  "answer":         "Based on FAQ-002, refunds are available within 30 days...",
  "documents_used": ["FAQ-002"],
  "model":          "llama3.3",
  "latency_ms":     312.5,
  "cache_version":  "a1b2c3d4"
}
```

---

## Project Structure

```
cag-service/
├── cag_service/
│   ├── __init__.py       # Public API
│   ├── core.py           # CAGCache, CAGEngine, Document, CAGResponse
│   ├── backends.py       # Ollama, OpenAI, Anthropic, HuggingFace adapters
│   ├── loaders.py        # File & dict loaders + example corpora
│   └── api.py            # FastAPI REST service
├── examples/
│   ├── basic_usage.py    # Minimal library example
│   ├── multi_backend.py  # Provider switching
│   └── load_from_files.py# File/directory loading
├── tests/
│   └── test_core.py      # Pytest suite (no live LLM required)
├── .github/workflows/
│   └── ci.yml            # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## LLM Backends

Install only what you need:

```bash
pip install cag-service[ollama]       # local, free, private
pip install cag-service[openai]       # GPT-4o, GPT-4-turbo
pip install cag-service[anthropic]    # Claude Sonnet / Opus
pip install cag-service[huggingface]  # Mistral, Llama, etc.
pip install cag-service[all-backends] # everything
```

Switch providers with two environment variables:

```bash
# Ollama (default)
CAG_PROVIDER=ollama    CAG_MODEL=llama3.3

# OpenAI
CAG_PROVIDER=openai    CAG_MODEL=gpt-4o          OPENAI_API_KEY=sk-...

# Anthropic
CAG_PROVIDER=anthropic CAG_MODEL=claude-sonnet-4-20250514 ANTHROPIC_API_KEY=sk-ant-...

# HuggingFace
CAG_PROVIDER=huggingface CAG_MODEL=mistralai/Mistral-7B-Instruct-v0.3 HF_TOKEN=hf_...
```

---

## Loading Your Knowledge

```python
from cag_service import CAGCache
from cag_service.loaders import (
    from_string,
    from_text_file,
    from_markdown_file,
    from_json_file,
    from_directory,
)

cache = CAGCache(name="my-kb")

# From a string
cache.add(from_string("All tickets must be resolved in 48h.", doc_id="SLA-001", title="SLA"))

# From files
cache.add(from_text_file("runbooks/db_recovery.txt"))
cache.add(from_markdown_file("docs/onboarding.md"))

# From a JSON file (list of {id, title, content} objects)
cache.add_many(from_json_file("knowledge/faqs.json"))

# Entire directory
cache.add_many(from_directory("./knowledge", extensions=[".txt", ".md"], recursive=True))

print(cache.stats())
# {'name': 'my-kb', 'document_count': 12, 'estimated_tokens': 8400, 'cache_version': 'ab12ef34', ...}
```

---

## Use Cases

| Domain | Example corpus | Sample query |
|--------|---------------|-------------|
| **Enterprise IT** | SOPs, runbooks, incident playbooks | *"What are the steps for a P1 database outage?"* |
| **Customer Support** | FAQs, return policies, product manuals | *"Can I return a used item after 30 days?"* |
| **Legal & Compliance** | Policies, contracts, regulations | *"What is the data retention requirement under GDPR Art. 5?"* |
| **Developer Docs** | API references, changelogs, guides | *"How do I authenticate with the v3 API?"* |
| **HR & Onboarding** | Employee handbook, benefits, processes | *"How do I request parental leave?"* |

---

## Real-World Integration: PeopleSoft Sentry

`cag-service` powers the SOP engine in [PeopleSoft Sentry](https://github.com/yourorg/peoplesoft-sentry), an AIOps diagnostic tool for PeopleSoft production support. It resolves IB errors and Process Monitor failures by matching live DB data against pre-cached SOPs — with zero retrieval latency.

---

## Contributing

1. Fork the repo and create a feature branch
2. Run tests: `pytest tests/ -v`
3. Lint: `ruff check cag_service/`
4. Open a PR with a clear description

Issues and feature requests are welcome!

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## GitHub Description

```
⚡ Cache-Augmented Generation (CAG) as a Service — pre-load your SOPs, runbooks,
or FAQs into an LLM context for zero-latency knowledge queries.
Supports Ollama, OpenAI, Anthropic & HuggingFace. FastAPI + Docker included.
```

**Topics:** `cag` `llm` `rag` `ai` `fastapi` `ollama` `openai` `anthropic` `python` `knowledge-base` `aiops` `nlp`
