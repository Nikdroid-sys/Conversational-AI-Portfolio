
import os
import hashlib
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_project_root():
    """Returns the project root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_vector_store_path():
    """Returns the path to the vector store."""
    project_root = get_project_root()
    vector_store_dir_name = os.getenv("VECTOR_STORE_PATH", "db")
    return os.path.join(project_root, vector_store_dir_name)

def get_data_hash_path():
    """Returns the path to the data hash file."""
    return os.path.join(get_vector_store_path(), "data.hash")

def calculate_data_hash():
    """Calculates a hash of the data directory's contents."""
    project_root = get_project_root()
    data_dir = os.path.join(project_root, 'data')
    hasher = hashlib.md5()
    
    if not os.path.exists(data_dir):
        return hasher.hexdigest()

    for root, _, files in os.walk(data_dir):
        for file in sorted(files):
            if file.endswith('.md'):
                path = os.path.join(root, file)
                hasher.update(file.encode())
                with open(path, 'rb') as f:
                    hasher.update(f.read())
    return hasher.hexdigest()

def ingest_data():
    """
    Ingests data from the data directory if changes are detected.
    """
    vector_store_path = get_vector_store_path()
    data_hash_path = get_data_hash_path()
    
    new_hash = calculate_data_hash()
    
    old_hash = None
    if os.path.exists(data_hash_path):
        with open(data_hash_path, 'r') as f:
            old_hash = f.read()

    if new_hash == old_hash and os.path.exists(vector_store_path):
        print("No changes in data directory. Ingestion skipped.")
        return
        
    print("Changes detected in data directory. Performing full re-ingestion.")
    
    project_root = get_project_root()
    data_dir = os.path.join(project_root, 'data')
    embedding_model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    if not os.path.exists(data_dir) or not any(f.endswith('.md') for f in os.listdir(data_dir)):
        if os.path.exists(vector_store_path):
            import shutil
            shutil.rmtree(vector_store_path)
        print("No markdown files to ingest. Vector store cleared.")
        os.makedirs(vector_store_path, exist_ok=True) # create db dir
        with open(data_hash_path, 'w') as f:
            f.write(new_hash)
        return

    loader = DirectoryLoader(data_dir, glob="**/*.md", show_progress=True)
    documents = loader.load()

    for doc in documents:
        # Extract the filename from the full path
        source_filename = os.path.basename(doc.metadata['source'])
        doc.metadata['source'] = source_filename

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = FAISS.from_documents(texts, embeddings)
    vector_store.save_local(vector_store_path)
    
    with open(data_hash_path, 'w') as f:
        f.write(new_hash)
        
    print("Full re-ingestion complete.")

if __name__ == '__main__':
    ingest_data()
