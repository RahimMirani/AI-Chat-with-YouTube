import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate

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
        
        #split the transcript into chunks, and add metadata, for timestamps and duration
        texts = [item.text for item in self.transcript]
        metadatas = [{'start': item.start, 'duration': item.duration} for item in self.transcript]
        documents = text_splitter.create_documents(texts, metadatas=metadatas)
        
        #Embedding model to convert text into vector
        embeddings = OpenAIEmbeddings()
        
        #Creating the vector store
        vector_store = FAISS.from_documents(documents, embeddings)
        return vector_store

    def build_qa_chain(self, timestamp: float | None):
        vector_store = self._build_vector_store()
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        retriever = vector_store.as_retriever()

        template = """
        You are a helpful AI assistant for a YouTube video.
        You are watching the video along with the user.
        The user is currently at the {timestamp} mark.
        Use the following pieces of context from the video transcript to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}
        
        Helpful Answer:"""

        prompt = PromptTemplate(
            template=template, input_variables=["context", "question", "timestamp"]
        )

        self.qa_chain = LLMChain(llm=llm, prompt=prompt)
        self.retriever = retriever


    def ask_question(self, question: str, timestamp: float | None):
        if not self.qa_chain:
            return "QA chain has not been built. Please call build_qa_chain() first."
        
        if timestamp:
            docs = self.retriever.get_relevant_documents(question)
            context = " ".join([doc.page_content for doc in docs])
            
            timestamp_str = f"{int(timestamp // 60)} minutes and {int(timestamp % 60)} seconds"

            response = self.qa_chain.invoke({
                "context": context,
                "question": question,
                "timestamp": timestamp_str
            })
            return response.get("text")
        else:
            # Fallback for when no timestamp is provided
            # This uses the old, simpler RetrievalQA logic for now.
            # We can remove this later if we decide all questions must have a timestamp.
            fallback_chain = RetrievalQA.from_chain_type(
                llm=self.qa_chain.llm, # reuse the llm
                chain_type="stuff",
                retriever=self.retriever
            )
            response = fallback_chain.invoke({"query": question})
            return response.get("result") 