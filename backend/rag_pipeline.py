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
            "You are a helpful assistant for questions about a YouTube video transcript.\n"
            "Use ONLY the context below to answer. If the answer cannot be found in the context, say 'I don't know'.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        ),
    )
    
    # Use a currently supported chat model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    
    return qa_chain 