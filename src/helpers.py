from langchain.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

# Function to load a pdf file from a dir path
def load_pdfs_from_directory(directory_path):
    loader = DirectoryLoader(directory_path,
                              glob="*.pdf",
                              loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

# Function to split documents into smaller chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    return text_splitter.split_documents(documents)

# Funtion to load embedings
def download_embeddings():
    embadding = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    return embadding 