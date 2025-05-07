from src.helpers import load_pdfs_from_directory , split_documents , download_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data = load_pdfs_from_directory(directory_path = "data/")
text_chunks = split_documents(extracted_data)
embeddings = download_embeddings()


# Initialize Pinecone and create an index
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-bot"
pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

# Uplode the documents to Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents = text_chunks,
    embedding = embeddings,
    index_name=index_name
)
