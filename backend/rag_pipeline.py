import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

load_dotenv()

class ChatPipeline:
    def __init__(self, transcript: list):
        self.transcript = transcript
        self.qa_chain = None

    def _build_vector_store(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        
        texts = [item.text for item in self.transcript]
        metadatas = [{'start': item.start, 'duration': item.duration} for item in self.transcript]
        documents = text_splitter.create_documents(texts, metadatas=metadatas)
        
        embeddings = OpenAIEmbeddings()
        
        vector_store = FAISS.from_documents(documents, embeddings)
        return vector_store

    def build_qa_chain(self):
        vector_store = self._build_vector_store()
        
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        retriever = vector_store.as_retriever()
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )

    def ask_question(self, question: str):
        if not self.qa_chain:
            return "QA chain has not been built. Please call build_qa_chain() first."

        response = self.qa_chain.invoke({"query": question})
        return response.get("result") 