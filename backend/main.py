from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from transcript import get_transcript
from rag_pipeline import ChatPipeline

app = FastAPI()

class ChatRequest(BaseModel):
    video_id: str
    question: str
    timestamp: float | None = None

@app.get("/")
def read_root():
    return {"status": "ok", "message": "YouTube RAG backend is running"}

@app.post("/api/chat")
def chat_with_video(request: ChatRequest):
    transcript = get_transcript(request.video_id)
    if not transcript or "Error" in transcript or "No transcript found" in transcript:
        raise HTTPException(
            status_code=404, 
            detail="Transcript not found or could not be fetched for this video."
        )

    pipeline = ChatPipeline(transcript)
    pipeline.build_qa_chain()
    answer = pipeline.ask_question(request.question)

    if not answer:
        raise HTTPException(
            status_code=500, 
            detail="The AI pipeline could not generate an answer."
        )

    return {"answer": answer} 



