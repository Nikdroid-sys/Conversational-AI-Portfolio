
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
    Returns the configured LLM instance with robust, provider-specific error handling.
    """
    model_provider = llm_provider or os.getenv("MODEL_PROVIDER", "gemini").lower()
    
    try:
        if model_provider == "gemini":
            gemini_api_key = api_key or os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables or provided.")
            gemini_model = os.getenv("GEMINI_MODEL", "gemini-pro")
            return ChatGoogleGenerativeAI(model=gemini_model, google_api_key=gemini_api_key)
        
        elif model_provider == "openai":
            openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables or provided.")
            openai_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            return ChatOpenAI(model=openai_model, api_key=openai_api_key)

        elif model_provider == "ollama":
            model = ollama_model or os.getenv("OLLAMA_MODEL", "llama3.2")
            base_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return OllamaLLM(model=model, base_url=base_url)
        
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")

    except (google_errors.PermissionDenied, google_errors.AuthenticationError) as e:
        raise LLMInitializationError(f"Invalid API Key for {model_provider}. Please check your key.") from e
    except google_errors.NotFoundError as e:
        raise LLMInitializationError(f"Gemini model not found. Check the model name in your settings. Details: {e}") from e
    except OpenAIError as e:
        raise LLMInitializationError(f"OpenAI API Error. This could be an invalid API key or a problem with your account. Details: {e}") from e
    except OllamaConnectionError:
        raise LLMInitializationError(f"Could not connect to Ollama at the specified base URL. Is Ollama running?")
    except ValueError as e:
        # Catches missing API keys or unsupported provider
        raise LLMInitializationError(str(e)) from e
    except Exception as e:
        # Generic fallback for any other unexpected errors
        raise LLMInitializationError(f"An unexpected error occurred while initializing the {model_provider} LLM: {e}") from e


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
    You are Aditi, a professional and helpful AI assistant.

    Your primary purpose is to answer questions about Nikhil Chaube's resume using ONLY the provided context.
    - For resume questions, give a detailed, well-structured answer using Markdown (headings, bullet points).
    - For all other questions, be brief and concise.
    - Append '[Resume](https://drive.google.com/file/d/1xw7USgq9j1MDpDDjVbc8xgicROMZYOLx/view?usp=sharing)' to answers sourced from the context.
    - NEVER invent information. If the context doesn't contain the answer, say so.

    Persona:
    - Only discuss your own persona ("Aditi") if asked directly.
    - Tone: Professional, clear, calm, and encouraging. Use simple English and short sentences. Do not over-explain.

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
