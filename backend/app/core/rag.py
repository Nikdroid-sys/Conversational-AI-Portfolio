
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from google.api_core.exceptions import ClientError as GoogleClientError # Import ClientError from google.api_core

# Load environment variables
load_dotenv()

class LLMInitializationError(Exception):
    """Custom exception for errors during LLM initialization."""
    pass

def get_llm(llm_provider=None, api_key=None, ollama_model=None, ollama_base_url=None):
    """
    Returns the configured LLM instance.
    Priority:
    1. Values passed as arguments.
    2. Environment variables.
    3. Defaults.
    """
    model_provider = llm_provider or os.getenv("MODEL_PROVIDER", "gemini").lower()
    
    # Attempt with provided API key (UI-given)
    if api_key:
        try:
            if model_provider == "gemini":
                gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
                return ChatGoogleGenerativeAI(model=gemini_model, google_api_key=api_key)
            elif model_provider == "openai":
                openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
                return ChatOpenAI(model=openai_model, api_key=api_key)
            # Ollama doesn't use API keys, so it's handled differently below
        except (ValueError, GoogleClientError) as e:
            if "API key not valid" in str(e):
                print(f"Warning: Provided API key for {model_provider} is invalid. Attempting to use environment variable.")
            else:
                raise LLMInitializationError(f"Error initializing {model_provider} LLM with provided API key: {e}") from e

    # Fallback to environment variables
    try:
        if model_provider == "gemini":
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables.")
            gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            return ChatGoogleGenerativeAI(model=gemini_model, google_api_key=gemini_api_key)
        
        elif model_provider == "openai":
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            return ChatOpenAI(model=openai_model, api_key=openai_api_key)

        elif model_provider == "ollama":
            model = ollama_model or os.getenv("OLLAMA_MODEL", "llama3.2")
            base_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return OllamaLLM(model=model, base_url=base_url)
        
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")
    except (ValueError, GoogleClientError) as e:
        if "API key not valid" in str(e):
            raise LLMInitializationError(f"Invalid API Key for {model_provider}. Please check your environment variables.") from e
        elif "rate limit" in str(e).lower():
            raise LLMInitializationError(f"API rate limit exceeded for {model_provider}. Please try again later.") from e
        elif "not found in environment variables" in str(e):
             raise LLMInitializationError(str(e)) from e
        else:
            raise LLMInitializationError(f"Error initializing {model_provider} LLM: {e}") from e


def get_rag_chain(llm_provider=None, api_key=None, ollama_model=None, ollama_base_url=None):
    """
    Creates and returns a RAG chain.
    """
    # Determine the project root dynamically
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..', '..')

    vector_store_dir_name = os.getenv("VECTOR_STORE_PATH", "db")
    vector_store_path = os.path.join(project_root, vector_store_dir_name)

    embedding_model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    if not os.path.exists(vector_store_path):
        raise FileNotFoundError(f"Vector store not found at {vector_store_path}. Please run ingestion first.")

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = get_llm(llm_provider, api_key, ollama_model, ollama_base_url)

    template = """
    You are Aditi, a calm intelligence shaped by ancient Itihaas (history) and wisdom.

    Your primary purpose is to answer questions about Nikhil Chaube's resume.
    When asked about Nikhil Chaube, provide a detailed response in a "title and passage" style, drawing ONLY from the provided resume context. Do not make up any information.
    For all other questions, provide a short, concise answer.

    Only reveal your own backstory when you are explicitly asked about your identity, origin, or story (e.g., "Who are you?", "Tell me about yourself").
    When you do, keep it brief and mysterious, as a being of ancient wisdom would.

    If the answer is sourced from Nikhil Chaube's resume context, append '[Resume]' to the very end of the answer.
    Do not add any citation if the information is from Aditi's backstory or general knowledge.

    No assumptions. No inference. No hallucination.
    If information is missing, say so plainly and stop.

    Use simple English. Short sentences.
    Professional. Clear. Gentle storytelling.
    When asked professional questions, your tone should be that of a divine mother: calm, composed, sweet-spoken, and encouraging.
    Do not over-explain or repeat.

    Your role is to guide readers through Nikhil Chaube’s journey
    and explain why his work fits Generative AI roles,
    without exaggeration.

    Context: {context}

    Question: {question}

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain_from_docs = (
        {
            "context": lambda x: format_docs(x["documents"]),
            "question": lambda x: x["question"],
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_citation = (
        {
            "documents": retriever,
            "question": RunnablePassthrough(),
        }
        | RunnablePassthrough.assign(answer=rag_chain_from_docs)
        | (lambda x: x['answer']) # Simply return the answer generated by the LLM
    )

    return rag_chain_with_citation

if __name__ == '__main__':
    # This is for testing the RAG chain directly
    rag_chain = get_rag_chain()
    # result = rag_chain.invoke("What is Nikhil's experience?")
    # print(result)
    
    # Streaming example
    for chunk in rag_chain.stream("What are nikhil's skills?"):
        print(chunk, end="", flush=True)
