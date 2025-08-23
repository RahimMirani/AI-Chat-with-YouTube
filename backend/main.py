from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from transcript import get_transcript
from rag_pipeline import create_rag_pipeline

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory cache for processed pipelines ---
PIPELINE_CACHE = {}

# --- Pydantic Models ---
class ProcessRequest(BaseModel):
    video_id: str

class ChatRequest(BaseModel):
    video_id: str
    question: str
    timestamp: float | None = None

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "ok", "message": "YouTube RAG backend is running"}

@app.post("/api/process_video")
def process_video(request: ProcessRequest):
    if request.video_id in PIPELINE_CACHE:
        return {"status": "ok", "message": "Video already processed."}

    transcript = get_transcript(request.video_id)
    if not isinstance(transcript, list):
        raise HTTPException(status_code=404, detail="Transcript not found or is invalid.")
    
    try:
        qa_chain = create_rag_pipeline(transcript)
        PIPELINE_CACHE[request.video_id] = qa_chain
        return {"status": "ok", "message": "Video processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process video: {e}")


@app.post("/api/chat")
def chat_with_video(request: ChatRequest):
    if request.video_id not in PIPELINE_CACHE:
        raise HTTPException(status_code=404, detail="Video not processed. Please process the video first.")

    qa_chain = PIPELINE_CACHE[request.video_id]
    
    question = request.question
    if request.timestamp:
        timestamp_str = f"{int(request.timestamp // 60)}m {int(request.timestamp % 60)}s"
        question = f"At the {timestamp_str} mark, a user asked: {request.question}"

    try:
        response = qa_chain.invoke({"query": question})
        
        # Handle different LangChain response structures
        if isinstance(response, dict):
            # Try different possible keys that LangChain might use
            answer = response.get("result") or response.get("answer") or response.get("output") or str(response)
        elif isinstance(response, str):
            # Direct string response
            answer = response
        else:
            # Fallback: convert to string
            answer = str(response)
            
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {e}") 



