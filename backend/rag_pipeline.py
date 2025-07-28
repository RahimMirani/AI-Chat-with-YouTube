import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

load_dotenv()

class ChatPipeline:
    def __init__(self, transcript: str):
        self.transcript = transcript
        self.qa_chain = None

    def build_vector_store(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        docs = text_splitter.split_text(self.transcript)
        
        embeddings = OpenAIEmbeddings()
        
        vector_store = FAISS.from_texts(docs, embeddings)
        return vector_store 