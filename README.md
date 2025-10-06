# AI Chat with YouTube Videos

Chat with any YouTube video in real-time using a Retrieval-Augmented Generation (RAG) pipeline. This Chrome extension injects a chat interface directly into the YouTube page, allowing you to ask questions about the video and get answers based on its transcript.

<img width="1815" height="798" alt="image" src="https://github.com/user-attachments/assets/6aaf1d89-b83f-435a-961f-193f3a50f2e1" />


## Features

- **Real-time Chat**: Interact with a chatbot to ask questions about the YouTube video you are watching.
- **Context-Aware Answers**: The chatbot uses the video's transcript to provide accurate and relevant answers.
- **Timestamp Awareness**: When you ask a question, the current video timestamp is used to provide more contextual answers.
- **Seamless UI**: The chat interface is injected directly into the YouTube page for a smooth user experience.

## How It Works

The project consists of a Python backend that powers the RAG pipeline and a Chrome extension that serves as the frontend.


1.  The **Chrome Extension** is injected into a YouTube video page.
2.  When you click "Get Started", the extension sends the video ID to the **FastAPI Backend**.
3.  The backend fetches the video's transcript using the **YouTube Transcript API**.
4.  A **RAG pipeline** is created using LangChain:
    - The transcript is chunked and embedded using **OpenAI's embeddings**.
    - The embeddings are stored in a **FAISS vector store**.
5.  When you ask a question, the backend retrieves relevant context from the vector store and uses **OpenAI's GPT model** to generate an answer.
6.  The answer is sent back to the extension and displayed in the chat UI.


## Tech Stack

-   **Frontend**: JavaScript, HTML, CSS (as a Chrome Extension)
-   **Backend**: Python, FastAPI
-   **AI/ML**: LangChain, OpenAI, FAISS

## Prerequisites

-   Python 3.8+
-   Google Chrome
-   An OpenAI API Key

## Installation and Setup

### 1. Backend Setup

First, set up the Python backend server:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/youtube-rag-chat.git
cd youtube-rag-chat/backend

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# 3. Install the required dependencies
pip install -r requirements.txt

# 4. Create a .env file in the `backend` directory
touch .env

# 5. Add your OpenAI API key to the .env file
echo 'OPENAI_API_KEY="your_openai_api_key"' > .env

# 6. Run the backend server
uvicorn main:app --reload
```

The backend server will be running at `http://127.0.0.1:8000`.

### 2. Frontend Setup

Next, load the Chrome extension:

1.  Open Google Chrome and navigate to `chrome://extensions`.
2.  Enable **Developer mode** using the toggle switch in the top-right corner.
3.  Click the **Load unpacked** button.
4.  Select the `extension` folder from the cloned repository.
5.  The "YouTube RAG Chat" extension should now appear in your list of extensions.

## How to Use

1.  Make sure the backend server is running.
2.  Open any YouTube video in your Chrome browser.
3.  The chat interface will appear on the right side of the page.
4.  Click **Get Started** to process the video.
5.  Once the processing is complete, you can start asking questions about the video!

Please start if you found the repo usefel!
