from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from voice_agent import VoiceAIAgent
import tempfile
import os
from typing import Dict, Any

app = FastAPI(title="Healthcare Voice AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

agent = VoiceAIAgent()

@app.get("/")
async def read_root():
    """Serve the main page"""
    return FileResponse("static/index.html")

@app.post("/process-audio/", response_model=Dict[str, Any])
async def process_audio(audio_file: UploadFile = File(...)):
    """
    Process an audio file and return the structured response.
    
    Args:
        audio_file (UploadFile): The audio file to process
        
    Returns:
        Dict containing transcript, language, intent, response, and confidence score
    """
    try:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file.flush()

            result = agent.process_audio(temp_file.name)
            
            # Clean up the temporary file
            os.unlink(temp_file.name)
            
            return result
            
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 