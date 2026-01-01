import os
import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

def ingest_data():
    """
    Ingests data from the data source, processes it, and stores it in a vector store.
    """
    # Determine the project root dynamically
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..', '..')

    data_dir_name = os.getenv("DATA_PATH", "data")
    data_path = os.path.join(project_root, data_dir_name)

    if not os.path.exists(data_path):
        print(f"Error: Data directory not found at {data_path}")
        return

    all_documents = []
    supported_extensions = {
        ".md": UnstructuredMarkdownLoader,
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
    }

    print(f"Loading data from {data_path}...")
    for ext, Loader in supported_extensions.items():
        for file_path in glob.glob(os.path.join(data_path, f"*{ext}")):
            print(f"  Loading {file_path} using {Loader.__name__}")
            try:
                loader = Loader(file_path)
                all_documents.extend(loader.load())
            except Exception as e:
                print(f"  Error loading {file_path}: {e}")

    if not all_documents:
        print(f"No documents found or loaded from {data_path} with supported extensions.")
        return

    print(f"Loaded {len(all_documents)} document(s).")

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(all_documents)
    print(f"Split documents into {len(texts)} chunks.")

    print("Creating embeddings. This may take a moment...")
    embedding_model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    print("Creating vector store...")
    vector_store_path = os.path.join(project_root, os.getenv("VECTOR_STORE_PATH", "db"))
    
    # Ensure the directory for the vector store exists
    os.makedirs(vector_store_path, exist_ok=True)
    
    vector_store = FAISS.from_documents(texts, embeddings)
    vector_store.save_local(vector_store_path)
    print(f"Vector store created and saved at {vector_store_path}")

if __name__ == "__main__":
    ingest_data()
