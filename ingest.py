import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
DATA_PATH = "data/"
VECTOR_STORE_PATH = "faiss_index"

def create_vector_store():
    documents = []
    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)
        if file.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith('.txt'):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
            
    if not documents:
        print("No documents found to process.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(docs)} chunks.")

    embeddings = OpenAIEmbeddings()

    print("Creating FAISS vector store...")
    db = FAISS.from_documents(docs, embeddings)
    
    db.save_local(VECTOR_STORE_PATH)
    print(f"Vector store created and saved at {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    create_vector_store()
