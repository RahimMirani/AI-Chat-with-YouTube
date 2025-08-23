import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

load_dotenv()

def create_rag_pipeline(transcript: list):
    """
    Creates a Retrieval-Augmented Generation (RAG) pipeline from a video transcript.
    """
    
    # Create documents with metadata
    texts = [item['text'] for item in transcript]
    metadatas = [{'start': item['start'], 'duration': item['duration']} for item in transcript]
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    documents = text_splitter.create_documents(texts, metadatas=metadatas)
    
    # Build the vector store
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(documents, embeddings)
    
    # Create the QA chain
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )
    
    return qa_chain 