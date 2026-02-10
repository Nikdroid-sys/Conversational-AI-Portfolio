import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from app.core.rag import get_rag_chain, LLMInitializationError
from app.core.ingestion import ingest_data


app = FastAPI(
    title="Conversational AI Portfolio",
    description="A RAG-based chatbot that answers questions about Nikhil Chaube's resume.",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    print("--- Running ingestion script on startup. ---")
    ingest_data()
    print("--- Ingestion check complete. ---")


# CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str
    llm_provider: str | None = None
    api_key: str | None = None
    ollama_model: str | None = None
    ollama_base_url: str | None = None


@app.get("/")
def read_root():
    return {"message": "Welcome to the Conversational AI Portfolio API!"}


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        rag_chain = get_rag_chain(
            llm_provider=request.llm_provider,
            api_key=request.api_key,
            ollama_model=request.ollama_model,
            ollama_base_url=request.ollama_base_url,
        )
        return StreamingResponse(rag_chain.stream(request.query), media_type="text/event-stream")
    except LLMInitializationError as e:
        return Response(content=str(e), status_code=400)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
