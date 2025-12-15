from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from app.core.embeddings import get_embedding_model
import os

VECTOR_DB_PATH = "data/vectorstore"

def build_vector_db():
    documents = []
    docs_path = "data/documents"

    for file in os.listdir(docs_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(docs_path, file))
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = get_embedding_model()
    vectordb = FAISS.from_documents(chunks, embeddings)

    vectordb.save_local(VECTOR_DB_PATH)

    return vectordb

def load_vector_db():
    embeddings = get_embedding_model()
    return FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
