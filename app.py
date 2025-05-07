from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from pinecone.grpc import PineconeGRPC as Pinecone

from src.helpers import  download_embeddings

from dotenv import load_dotenv
import os

from src.prompt import *


app = Flask(__name__)

load_dotenv()   

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GENAI_API_KEY = os.getenv('GENAI_API_KEY')

embeddings = download_embeddings()


index_name = "medical-bot"
docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name
)
retriver = docsearch.as_retriever(search_type="similarity" , search_kwargs={"k": 3})



prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    google_api_key=GENAI_API_KEY,
    model="gemini-2.0-flash",
    temperature=0.1,
    max_output_tokens=512,
)

# Combine retrieved docs into prompt
combine_documents_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=prompt
)

# Ensure that 'retriver' is properly initialized
# Example: retriver = docsearch.as_retriever()  # Make sure this line is present and correct

# Retrieval chain using RetrievalQA
reg_chain = create_retrieval_chain(retriver, combine_documents_chain)  # Corrected function name

# query = "What is the best way to treat a cold?"
# result = reg_chain.invoke({"input": query})

# print("Answer:", result['answer'])


@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    if question:
        # Use the retrieval chain to get the answer
        result = reg_chain.invoke({"input": question})
        answer = result['answer']
        print(answer)
        return str(answer)
    else:
        return "Please ask a question."
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)