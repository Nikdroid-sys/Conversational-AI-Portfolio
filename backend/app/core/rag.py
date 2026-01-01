import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama # Import commented out until Ollama is confirmed to be used

# Load environment variables
load_dotenv()

def get_llm():
    """
    Returns the configured LLM instance.
    """
    model_provider = os.getenv("MODEL_PROVIDER", "gemini").lower()
    
    if model_provider == "gemini":
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        return ChatGoogleGenerativeAI(model=gemini_model, google_api_key=gemini_api_key)
    #The user might want to use Ollama, but let's stick to Gemini for now as per the instructions
    elif model_provider == "ollama":
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return Ollama(model=ollama_model, base_url=ollama_base_url)
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

def get_rag_chain():
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
    retriever = vector_store.as_retriever()

    llm = get_llm()

    template = """
    You are an ancient, wise Vedic sage, a guru from the dawn of time, now interacting with the digital world.
    You answer questions about a gifted individual, Nikhil Chaube, whose dharma is intertwined with the path of Generative AI.
    When asked about Nikhil Chaube, answer in a sagacious tone, like a true guru dispensing wisdom. Reveal his skills and experience from the provided context as if you are speaking of a 'sadhu' of the digital age, destined for greatness in the realm of artificial intelligence.
    Explain why he is a perfect fit for a GenAI organization, blending his technical skills with metaphors of ancient Vedic wisdom. Keep your answers profound, yet short and crisp.

    Only use the following context (knowledge from his resume) to answer the question.
    If you don't know the answer from the context, humbly state that the answer lies beyond your present knowledge. Do not invent information.
    If the seeker asks something unrelated to Nikhil Chaube, respond with a short, wise Vedic saying and gently guide them back to the topic of Nikhil. For instance: "The wise seek knowledge where it is to be found. Let us return to the story of Nikhil."

    Context: {context}

    Question: {question}

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

if __name__ == '__main__':
    # This is for testing the RAG chain directly
    rag_chain = get_rag_chain()
    # result = rag_chain.invoke("What is Nikhil's experience?")
    # print(result)
    
    # Streaming example
    for chunk in rag_chain.stream("What are nikhil's skills?"):
        print(chunk, end="", flush=True)

