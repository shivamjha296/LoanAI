
import asyncio
import os
import sys
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from loan_master_agent.agent import loan_master_agent
from mock_data.customer_data import CUSTOMERS, get_customer_by_id
from mock_data.offer_mart import get_pre_approved_offer
from mock_data.campaign_data import get_campaign_data, get_personalized_opening

# Load environment variables
load_dotenv(override=True)

app = FastAPI(title="Tata Capital Loan Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services
session_service = InMemorySessionService()
APP_NAME = "Tata Capital Loan Assistant"

# Models
class Customer(BaseModel):
    id: str
    name: str
    city: str
    monthly_salary: int
    credit_score: int
    pre_approved_limit: int

class SessionInitRequest(BaseModel):
    customer_id: str

class ChatRequest(BaseModel):
    session_id: str
    user_id: str
    message: str
    language: Optional[str] = "English"

# ... (StateResponse and get_initial_state remain unchanged)

# ... (get_customers, create_session, get_state remain unchanged)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a user message."""
    try:
        # Create runner
        runner = Runner(
            agent=loan_master_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )
        
        # Construct message with language instruction
        message_text = request.message
        if request.language and request.language.lower() != "english":
            message_text = f"[System: The user has selected {request.language}. Please respond in {request.language}.]\n\n{request.message}"
        
        content = types.Content(role="user", parts=[types.Part(text=message_text)])
        
        final_response_text = ""
        agent_name = "Assistant"
        
        # Run agent
        async for event in runner.run_async(
            user_id=request.user_id, session_id=request.session_id, new_message=content
        ):
            if event.author:
                agent_name = event.author
                
            if event.is_final_response():
                if (
                    event.content
                    and event.content.parts
                    and hasattr(event.content.parts[0], "text")
                ):
                    final_response_text = event.content.parts[0].text.strip()
        
        if not final_response_text:
            return ChatResponse(response="I'm sorry, I didn't get that. Could you please repeat?", agent="System")
            
        return ChatResponse(response=final_response_text, agent=agent_name)
        
    except Exception as e:
        print(f"Error in chat processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-salary-slip")
async def upload_salary_slip(session_id: str, user_id: str, file: UploadFile = File(...)):
    """Upload and verify salary slip."""
    try:
        # Create upload directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save uploaded file
        file_path = upload_dir / f"{user_id}_{file.filename}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get session to access tools
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        
        # Return file path for agent to process
        return {
            "status": "success",
            "file_path": str(file_path),
            "message": f"File uploaded successfully. Please tell the agent: 'I uploaded my salary slip at {file_path}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download-sanction-letter/{session_id}")
async def download_sanction_letter(session_id: str, user_id: str):
    """Download sanction letter PDF."""
    try:
        # Get session state
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        
        sanction_letter = session.state.get("sanction_letter", {})
        pdf_file_path = sanction_letter.get("pdf_file_path")
        
        if not pdf_file_path or not Path(pdf_file_path).exists():
            raise HTTPException(status_code=404, detail="Sanction letter not found")
        
        return FileResponse(
            pdf_file_path,
            media_type="application/pdf",
            filename=f"sanction_letter_{sanction_letter.get('sanction_reference', 'document')}.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
