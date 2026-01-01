import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.core.rag import get_rag_chain
from app.core.ingestion import ingest_data


app = FastAPI(
    title="Conversational AI Portfolio",
    description="A RAG-based chatbot that answers questions about Nikhil Chaube's resume.",
    version="0.1.0",
)

@app.on_event("startup")
async def startup_event():
    # Construct the full path to the vector store
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    vector_store_dir_name = os.getenv("VECTOR_STORE_PATH", "db")
    vector_store_path = os.path.join(project_root, vector_store_dir_name)

    if not os.path.exists(vector_store_path):
        print("--- Vector store not found. Running ingestion script. ---")
        ingest_data()
        print("--- Ingestion complete. ---")


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


@app.get("/")
def read_root():
    return {"message": "Welcome to the Conversational AI Portfolio API!"}


@app.post("/chat")
async def chat(request: ChatRequest):
    rag_chain = get_rag_chain()
    return StreamingResponse(rag_chain.stream(request.query), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
