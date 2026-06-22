# ResearchPaperAI — Agentic RAG for Research Papers

> Most PDF chatbots just chunk your document and do a simple vector search. ResearchPaperAI goes further — it **understands your query intent**, **translates it into multiple search strategies**, **fuses results using Reciprocal Rank Fusion**, **re-ranks with BM25**, and **routes it through a LangGraph agent pipeline** to produce structured, citation-backed answers. It's not a chatbot wrapper — it's a research assistant engine.

---

## Why This Is Different

| Feature | Typical PDF RAG | ResearchPaperAI |
|---|---|---|
| Query handling | Single embedding lookup | Query understanding → multi-query translation |
| Retrieval | Top-K similarity | Multi-query + RRF fusion + BM25 re-rank |
| Keyword search | No | BM25 Okapi re-ranking on retrieved chunks |
| Hybrid retrieval | No | Vector (60%) + BM25 (40%) weighted fusion |
| Routing | None | LangGraph router (research vs comparison) |
| Output | Raw LLM answer | Structured analysis with citations |
| Multi-paper | No | Yes — compare across papers |
| Upload | No | Runtime PDF upload + Pinecone ingestion |
| Agents | None | 6 specialized agents |

---

## Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────┐
│               Streamlit Frontend                │
│         (Upload PDF / Chat / Citations)         │
└───────────────────┬─────────────────────────────┘
                    │ HTTP
                    ▼
┌─────────────────────────────────────────────────┐
│              FastAPI Backend                    │
│   /upload  /chat  /compare  /research           │
└───────────────────┬─────────────────────────────┘
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
┌─────────────────┐   ┌──────────────────────────┐
│  PDF Ingestion  │   │   RAG / Agent Pipeline   │
│                 │   │                          │
│  PDFLoader      │   │  Query Understanding     │
│  MetadataExtract│   │       ↓                  │
│  SectionChunker │   │  Query Translation       │
│  RecursiveChunk │   │  (4 diverse sub-queries) │
│  EmbeddingGen   │   │       ↓                  │
│  Pinecone Upsert│   │  Multi-Query Retriever   │
└─────────────────┘   │       ↓                  │
                      │  RRF Fusion              │
                      │  (Reciprocal Rank Fusion)│
                      │       ↓                  │
                      │  BM25 Re-Rank            │
                      │  (Okapi BM25 scoring)    │
                      │       ↓                  │
                      │  LangGraph Router        │
                      │  ┌────┴────┐             │
                      │  ▼        ▼              │
                      │ Research  Comparison     │
                      │  Agent    Agent          │
                      │       ↓                  │
                      │  Answer Generation       │
                      │  + Citation Agent        │
                      └──────────────────────────┘
                                  │
                    ┌─────────────┴──────────┐
                    ▼                        ▼
           ┌───────────────┐       ┌──────────────────┐
           │  Pinecone     │       │  Ollama (local)  │
           │  Vector DB    │       │  qwen2.5:3b LLM  │
           │  (nomic embeds│       │  nomic-embed-text│
           └───────────────┘       └──────────────────┘
```

---

## Agent Pipeline Detail

```
understand_query()        → intent, topics, query_type (JSON)
      ↓
translate_query()         → 4 diverse sub-queries (definition, architecture,
      ↓                     methodology, evaluation)
MultiQueryRetriever       → runs each sub-query against Pinecone
      ↓
RRF.fuse()                → merges ranked lists, surfaces best chunks
      ↓
BM25Retriever.rerank()    → keyword-aware re-ranking of fused results
      ↓                     (BM25Okapi — tokenized corpus scoring)
HybridRetriever           → optional: vector (60%) + BM25 (40%) weighted path
      ↓
LangGraph Router          → routes to research_node or comparison_node
      ↓
ResearchAgent /           → structured LLM analysis
ComparisonAgent
      ↓
CitationAgent             → paper title + section citations
```

---

## Folder Structure

```
ResearchPaperAI/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── query_understanding.py   # Intent + topic extraction
│   │   │   ├── query_translation.py     # Multi-query generation
│   │   │   ├── query_router.py          # Routes to LangGraph
│   │   │   ├── research_agent.py        # Single-paper analysis
│   │   │   ├── comparison_agent.py      # Cross-paper comparison
│   │   │   ├── answer_generation.py     # Final answer synthesis
│   │   │   ├── citation_agent.py        # Source citation extractor
│   │   │   └── paper_selection_agent.py # Dynamic paper selector
│   │   │
│   │   ├── api/
│   │   │   ├── server.py                # FastAPI routes
│   │   │   └── memory.py                # Session conversation memory
│   │   │
│   │   ├── graph/
│   │   │   ├── graph_builder.py         # LangGraph DAG definition
│   │   │   ├── router.py                # Query routing logic
│   │   │   ├── nodes.py                 # Graph node functions
│   │   │   └── state.py                 # GraphState TypedDict
│   │   │
│   │   ├── ingestion/
│   │   │   ├── pdf_loader.py            # pypdf text extraction
│   │   │   ├── metadata_extractor.py    # Title, abstract, sections
│   │   │   ├── chunker.py               # Section-aware chunking
│   │   │   ├── recursive_chunker.py     # LangChain recursive splitter
│   │   │   └── document_processor.py   # Full ingestion pipeline
│   │   │
│   │   ├── retrieval/
│   │   │   ├── retriever.py             # Pinecone vector search
│   │   │   ├── multi_query_retriever.py # Parallel multi-query search
│   │   │   ├── rrf.py                   # Reciprocal Rank Fusion
│   │   │   ├── bm25_retriever.py        # BM25 Okapi re-ranker
│   │   │   ├── hybrid_retriever.py      # Vector + BM25 weighted fusion
│   │   │   └── fusion_retriever.py      # MultiQuery → RRF → BM25 pipeline
│   │   │
│   │   ├── embeddings/
│   │   │   └── embedding_generator.py  # Ollama nomic-embed-text
│   │   │
│   │   ├── vectordb/
│   │   │   ├── pinecone_client.py       # Pinecone connection
│   │   │   └── vector_store.py          # Upsert / delete operations
│   │   │
│   │   ├── llm/
│   │   │   └── ollama_client.py         # Cached ChatOllama client
│   │   │
│   │   └── rag/
│   │       └── rag_pipeline.py          # End-to-end RAG orchestration
│   │
│   ├── data/pdfs/                       # Preloaded research papers
│   └── uploads/                         # Runtime uploaded PDFs
│
├── frontend/
│   └── streamlit_app.py                 # Chat UI + upload + citations
│
├── tests/                               # Integration test scripts
├── scripts/                             # Pinecone utility scripts
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Ollama — `qwen2.5:3b` (local, no API cost) |
| Embeddings | Ollama — `nomic-embed-text` (local) |
| Vector DB | Pinecone (serverless) |
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain + LangChain-Ollama |
| API Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| PDF Parsing | pypdf |
| Text Splitting | LangChain RecursiveCharacterTextSplitter |
| Retrieval Strategy | Multi-Query + RRF + BM25 re-rank |
| Keyword Ranking | `rank-bm25` — BM25Okapi |

---

## Quickstart

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables
Create `backend/.env`:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name
```

### 3. Pull Ollama models
```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
```

### 4. Start the backend
```bash
uvicorn backend.app.api.server:app --reload --port 8000
```

### 5. Start the frontend
```bash
streamlit run frontend/streamlit_app.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload` | Upload and ingest a PDF |
| POST | `/chat` | Conversational Q&A with citations |
| POST | `/compare` | Structured cross-paper comparison |
| POST | `/research` | Deep single-topic analysis |
| POST | `/citations` | Extract citations for a query |
| POST | `/delete-pdf` | Remove a PDF from Pinecone + disk |
| GET | `/health` | Health check |

---

## How Retrieval Works

Two retrieval paths are available depending on the route:

### FusionRetriever (default — used by chat + research agents)

1. **Query Understanding** — LLM extracts intent and query type
2. **Query Translation** — generates 4 sub-queries (definition, architecture, methodology, evaluation)
3. **Multi-Query Retrieval** — each sub-query hits Pinecone independently
4. **RRF Fusion** — rank positions fused using `score = 1 / (k + rank + 1)`, `k=60`
5. **BM25 Re-Rank** — `BM25Okapi` re-scores the fused pool on the original query tokens, surfaces the most keyword-relevant chunks
6. **Top-5 chunks** passed to the answer agent as context

### HybridRetriever (alternative — vector + BM25 weighted fusion)

1. **Vector Search** — Pinecone top-10 by embedding similarity
2. **BM25 Re-Rank** — same top-10 pool re-scored with `BM25Okapi`
3. **Weighted Score Fusion** — combined using reciprocal rank: `vector × 0.6 + bm25 × 0.4`
4. **Top-5 chunks** returned

### Why BM25 on top of vector search?

| Scenario | Vector search alone | With BM25 re-rank |
|---|---|---|
| Exact term match (e.g. `"BLEU score"`) | May miss exact phrasing | BM25 boosts exact-match chunks |
| Acronyms / model names | Embedding similarity diluted | BM25 scores exact token hits highly |
| Long fused pools | All chunks ranked by position | Re-ranked by actual query relevance |

---

## LangGraph Flow

```
[router] → decide_route() → [research] → END
                          → [comparison] → END
```

The router calls `understand_query()` and sets `task_type` on state. Conditional edges dispatch to the appropriate agent node.
