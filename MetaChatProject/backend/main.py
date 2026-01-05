from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from service import stream_chat_response
import asyncio

app = FastAPI(title="MetaChat API")

# Enable CORS for Web, Mobile, and Desktop clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    voice: str = "female"

@app.get("/")
async def root():
    return {"status": "ok", "message": "MetaChat API is running"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to receive a user message and return a streaming response.
    """
    return StreamingResponse(stream_chat_response(request.message, request.language, request.voice), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    # Host 0.0.0.0 is important for Android emulator/other devices to access
    uvicorn.run(app, host="0.0.0.0", port=8000)
