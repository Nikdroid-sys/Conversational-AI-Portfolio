import os
from dotenv import load_dotenv

# LangChain Core & Chains
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Vector Store & Embeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# LLM Providers
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM

# Error Handling
import google.genai.errors as google_errors
from openai import APIError as OpenAIError
from requests.exceptions import ConnectionError as OllamaConnectionError

# Load environment variables
load_dotenv()

class LLMInitializationError(Exception):
    """Custom exception for errors during LLM initialization."""
    pass

def get_llm(llm_provider=None, api_key=None, ollama_model=None, ollama_base_url=None):
    """
    Returns the configured LLM instance with 2026-stable model versions.
    """
    model_provider = llm_provider or os.getenv("MODEL_PROVIDER", "gemini").lower()
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    try:
        if model_provider == "gemini":
            gemini_api_key = api_key or os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY not found.")
            
            # FIX: Using gemini-2.5-flash to avoid the 404 error in Feb 2026
            # We force version='v1' to ensure it uses the stable production endpoint
            return ChatGoogleGenerativeAI(
                model=gemini_model, 
                google_api_key=gemini_api_key,
                temperature=0.3
            )
        
        elif model_provider == "openai":
            openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found.")
            # Modern 2026 OpenAI models
            openai_model = os.getenv("OPENAI_MODEL", "gpt-4.5-turbo")
            return ChatOpenAI(model=openai_model, api_key=openai_api_key)

        elif model_provider == "ollama":
            model = ollama_model or os.getenv("OLLAMA_MODEL", "llama3.3")
            base_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return OllamaLLM(model=model, base_url=base_url)
        
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")

    except (google_errors.PermissionDenied, google_errors.AuthenticationError) as e:
        raise LLMInitializationError(f"Gemini Auth failed. Check your API key.") from e
    except OpenAIError as e:
        raise LLMInitializationError(f"OpenAI error: {e}") from e
    except OllamaConnectionError:
        raise LLMInitializationError("Ollama is not running. Check local server.")
    except Exception as e:
        raise LLMInitializationError(f"Initialization Error ({model_provider}): {e}")

def get_rag_chain(llm_provider=None, api_key=None, ollama_model=None, ollama_base_url=None):
    """
    Creates the complete RAG chain with Aditi persona and vector retrieval.
    """
    # 1. Path & Resource Setup (Optimized for Local & Hugging Face)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Moves up from backend/app/core to backend/
    project_root = os.path.abspath(os.path.join(current_dir, "../../")) 

    # Define absolute paths for both resources
    vector_store_path = os.path.join(project_root, 'db')
    data_path = os.path.join(project_root, 'data')

    # Debugging logs
    print(f"DEBUG: Searching for vector store at: {vector_store_path}")
    
    # 2. Path Validation
    if not os.path.exists(vector_store_path):
        print(f"❌ ERROR: DB folder not found at {vector_store_path}")
        if os.path.exists(project_root):
            print(f"DEBUG: Files in project root ({project_root}) are: {os.listdir(project_root)}")
        raise FileNotFoundError(f"FAISS index not found at {vector_store_path}. Run ingestion first.")
    else:
        print(f"✅ SUCCESS: DB folder found at {vector_store_path}")
    # 2. Setup Embeddings & Retriever
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        vector_store_path, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 3. Prompt Template (Optimized for Gemini 2.x/3.x)
    template = """
    <system>
    You are Aditi, a professional AI assistant for Nikhil Chaube. 
    - Use the provided context to answer questions about Nikhil's resume.
    - Be detailed and use Markdown for resume questions.
    - If the answer isn't in the context, say so.
    - If the answer is sourced from the context, append the special tag `[RESUME]` at the very end of your response.
    </system>

    <context>
    {context}
    </context>

    <question>
    {question}
    </question>
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = get_llm(llm_provider, api_key, ollama_model, ollama_base_url)

    # 4. Chain Architecture
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Sequence: Retrieve -> Format -> Prompt -> LLM -> Parse
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

if __name__ == '__main__':
    try:
        # Defaults to Gemini unless env MODEL_PROVIDER is changed
        chain = get_rag_chain()
        print("Aditi Online. Testing...\n")
        
        for chunk in chain.stream("What are Nikhil's main skills?"):
            print(chunk, end="", flush=True)
            
    except Exception as e:
        print(f"\n[ERROR]: {e}")