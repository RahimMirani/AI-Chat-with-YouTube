# Project Overview: YouTube Chat-with-Video Chrome Extension

This document outlines the phased development plan for creating a Chrome extension that allows users to chat with a YouTube video.

## Phase 1: Core Backend - Transcript Processing and Q&A

This phase focuses on creating a service that can understand a YouTube video and answer questions about it, without timestamp awareness.

1.  **Project Setup:**
    *   Create a main project directory `youtube-rag`.
    *   Inside, create two subdirectories: `backend` and `extension`.
    *   Set up a Python virtual environment inside the `backend` directory.

2.  **Backend Dependencies:**
    *   `FastAPI`: For the web server.
    *   `LangChain` (`langchain`): Core framework for the RAG pipeline.
    *   `youtube-transcript-api`: To fetch video transcripts.
    *   `langchain-openai`: LLM provider library.
    *   `faiss-cpu`: Vector store library for local development.
    *   `uvicorn`: To run the FastAPI server.
    *   `python-dotenv`: To manage API keys.

3.  **Transcript Fetcher (`backend/transcript.py`):**
    *   A module with a function that takes a YouTube video URL or ID and returns the full transcript.

4.  **RAG Pipeline (`backend/rag_pipeline.py`):**
    *   **Text Chunking:** Split the transcript into smaller, overlapping chunks using LangChain's `RecursiveCharacterTextSplitter`.
    *   **Embedding and Vector Store:** Use an embedding model (e.g., OpenAI's `text-embedding-ada-002`) to convert text chunks into vectors and store them in a FAISS vector store.
    *   **Retriever:** Create a retriever from the vector store to find relevant chunks for a query.
    *   **QA Chain:** Construct a `RetrievalQA` chain to generate answers based on the retrieved context.

5.  **API Server (`backend/main.py`):**
    *   `POST /api/process_video`: Receives a `video_id`, fetches the transcript, builds the vector store, and caches it.
    *   `POST /api/chat`: Receives a `video_id` and a `question`, queries the RAG chain, and returns the answer.

## Phase 2: Enhancing the Backend with Timestamp Awareness

This phase makes the AI aware of the user's current position in the video.

1.  **Timestamped Chunks:**
    *   Modify the text chunking process to include start and end time metadata for each chunk.

2.  **Context-Aware Retrieval:**
    *   Filter or boost the relevance of retrieved chunks based on their proximity to the user's current timestamp.

3.  **Smarter Prompting:**
    *   Update the QA chain's prompt to include the user's timestamp, providing more context to the LLM.

4.  **Update API:**
    *   The `/api/chat` endpoint will be updated to accept a `timestamp` parameter.

## Phase 3: Chrome Extension Frontend

This phase involves building the user-facing part of the extension.

1.  **Manifest File (`extension/manifest.json`):**
    *   Define the extension's name, version, permissions (`activeTab`, `scripting`), and declare content and background scripts.

2.  **Content Script (`extension/content.js`):**
    *   Injects the chat UI into the YouTube page.
    *   Listens for user input in the chat box.
    *   Gets the video's current timestamp.
    *   Communicates with the background script.

3.  **Background Script (`extension/background.js`):**
    *   Acts as a middleman between the content script and the backend API.
    *   Handles `process_video` and `chat` API calls.
    *   Forwards backend responses to the content script.

4.  **UI (`extension/chat.html`, `extension/style.css`):**
    *   The HTML and CSS for the chat window that will be injected onto the page. 