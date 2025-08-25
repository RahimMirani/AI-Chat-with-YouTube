import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

def create_rag_pipeline(transcript: list):
    """
    Creates a Retrieval-Augmented Generation (RAG) pipeline from a video transcript.
    Expects a list of dicts with keys: 'text', 'start', 'duration'.
    """
    
    # Concatenate transcript into a single string to create coherent chunks
    all_text = "\n".join([item.get('text', '') for item in transcript if item.get('text')])
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150
    )
    documents = text_splitter.create_documents([all_text])

    # Build the vector store with an explicit embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(documents, embeddings)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "fetch_k": 20}
    )
    
    # Use a grounded prompt to encourage citing only context
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a helpful assistant for answering questions about the YouTube video a user is watching through transcript. Your goal is to expand the user knowledge on the video and answer their questions.\n"
            "For the questions that are generic and not talked about in the video but user asks, you can answer with a general answer. But do not make up information of fake answers or information that is not in the video.\n"
            "Use the context below to answer the targeted questions for the user. If the answer cannot be found in the context and its unrelated to the video, politly say you don't know.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        ),
    )
    
    # Use a currently supported chat model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    
    return qa_chain 