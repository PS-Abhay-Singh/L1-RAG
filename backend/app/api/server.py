from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
import os

from backend.app.ingestion.document_processor import DocumentProcessor
from backend.app.agents.comparison_agent import compare_papers
from backend.app.agents.research_agent import ResearchAgent
from backend.app.agents.citation_agent import verify_citation
from backend.app.rag.rag_pipeline import RAGPipeline
from backend.app.vectordb.vector_store import VectorStore

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = FastAPI(title="ResearchPaperAI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    query: str
    history: List[dict] = []

class UploadResponse(BaseModel):
    file_name: str
    status: str
    chunks: int

class CitationResponse(BaseModel):
    citations: List[dict]

class DeletePDFRequest(BaseModel):
    file_name: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF upload is supported.")

    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    result = DocumentProcessor.process(file_path)

    return UploadResponse(
        file_name=filename,
        status="processed",
        chunks=result["chunks"],
    )

@app.post("/compare")
async def compare(query_request: QueryRequest):
    content = compare_papers(query_request.query)
    return {"query": query_request.query, "result": content}

@app.post("/research")
async def research(query_request: QueryRequest):
    content = ResearchAgent.analyze(query_request.query)
    return {"query": query_request.query, "result": content}

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    answer, results = RAGPipeline.ask_with_sources(chat_request.query)

    citations = []
    seen = set()
    for match in results:
        paper_title = match.metadata.get("paper_title", "Unknown")
        section = match.metadata.get("section", "Unknown section")
        key = (paper_title, section)
        if key not in seen:
            citations.append({"paper": paper_title, "section": section})
            seen.add(key)

    history = []
    if chat_request.history:
        history = chat_request.history

    history.append({"speaker": "user", "text": chat_request.query})
    history.append({"speaker": "assistant", "text": answer})

    return {
        "query": chat_request.query,
        "answer": answer,
        "citations": citations,
        "history": history
    }

@app.post("/delete-pdf")
async def delete_pdf(delete_request: DeletePDFRequest):
    file_name = delete_request.file_name
    VectorStore.delete_by_source_file(file_name)

    file_path = os.path.join(UPLOAD_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"file_name": file_name, "status": "deleted"}

@app.post("/citations", response_model=CitationResponse)
async def citations(query_request: QueryRequest):
    results = RAGPipeline.ask(query_request.query)
    citations_response = verify_citation([])
    return CitationResponse(citations=citations_response)
