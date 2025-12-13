
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

class ChatResponse(BaseModel):
    response: str
    agent: Optional[str] = None

class StateResponse(BaseModel):
    session_id: str
    state: Dict[str, Any]

# Helper to get initial state (reused from main.py logic)
def get_initial_state(customer_id: str) -> dict:
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {}
        
    offer_result = get_pre_approved_offer(customer_id)
    offer = offer_result.get("offer", {}) if offer_result["status"] == "success" else {}
    
    # Get campaign data
    campaign_data = get_campaign_data(customer_id)
    campaign = campaign_data.get("campaign", {})
    journey = campaign_data.get("journey", {})
    credit_score = customer.get("credit_score", 750)
    
    # 🧠 Smart Persuasion Strategy (LLM-driven, dynamic)
    persuasion_context = f"""
CUSTOMER CONTEXT FOR INTELLIGENT ADAPTATION:
- Credit Score: {credit_score} ({"Excellent" if credit_score >= 800 else "Good" if credit_score >= 750 else "Fair" if credit_score >= 700 else "Needs Improvement"})
- Income: ₹{customer.get('monthly_salary', 0):,}/month ({"High" if customer.get('monthly_salary', 0) >= 100000 else "Medium" if customer.get('monthly_salary', 0) >= 50000 else "Budget-conscious"})
- Campaign: {campaign.get('source', 'Direct')} - {campaign.get('keyword', 'personal loan')}
- Intent: {campaign.get('intent', 'GENERAL_PURPOSE')}
- Urgency: {campaign.get('urgency_level', 'MEDIUM')}
- Customer Type: {campaign_data.get('customer_type', 'FIRST_TIME')}
- Payment History: {journey.get('payment_history', 'N/A')}

ADAPT YOUR APPROACH INTELLIGENTLY:
- If urgent need → Emphasize speed ("2-hour approval, 24-hour disbursement")
- If repeat customer → Show appreciation ("As a valued customer for X years...")
- If high credit score → Highlight premium rates ("Your excellent score qualifies you for our best 10.99% rate")
- If budget-conscious → Focus on EMI affordability ("Just ₹X/month - less than dining expenses")
- If skeptical/researcher → Provide transparency ("Complete breakdown, zero hidden charges")
- If first-time borrower → Be educational and patient
"""
    
    # 💡 Personalized Opening
    personalized_opening = get_personalized_opening(customer_id, customer["name"], campaign_data)
    
    return {
        # Customer information
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "customer_phone": customer["phone"],
        "customer_email": customer["email"],
        "customer_city": customer["city"],
        "customer_salary": customer["monthly_salary"],
        "customer_occupation": customer["occupation"],
        "customer_employer": customer["employer"],
        "customer_pan": customer["pan_number"],
        "customer_bank": customer["bank_name"],
        "customer_account": customer["account_number"],
        
        # Pre-approved offer
        "pre_approved_limit": customer["pre_approved_limit"],
        "credit_score": customer["credit_score"],
        "current_offer": offer,
        
        # 🎯 Pre-Conversation Intelligence
        "campaign_source": campaign.get("source", "Direct"),
        "campaign_keyword": campaign.get("keyword", "personal loan"),
        "customer_intent": campaign.get("intent", "GENERAL_PURPOSE"),
        "urgency_level": campaign.get("urgency_level", "MEDIUM"),
        "customer_type": campaign_data.get("customer_type", "FIRST_TIME"),
        "relationship_tenure_years": journey.get("relationship_tenure_years", 0),
        "payment_history": journey.get("payment_history", "N/A"),
        "current_loans_count": len(journey.get("current_loans", [])),
        "previous_interactions_count": len(journey.get("previous_interactions", [])),
        "offer_expiry_hours": campaign.get("offer_expiry_hours", 48),
        
        # 🧠 Persuasion Strategy (Smart, LLM-driven)
        "persuasion_strategy": persuasion_context,
        "personalized_opening": personalized_opening,
        
        # ⚠️ Objection Handling
        "objection_handling_context": "No objections detected yet. Monitor customer responses.",
        "detected_objections": [],
        
        # 💚 Emotional Intelligence
        "current_sentiment": {"status": "neutral", "primary_sentiment": "NEUTRAL"},
        "sentiment_adaptive_strategy": "No strong sentiment detected. Maintain professional, balanced tone.",
        "sentiment_history": [],
        
        # Application tracking
        "loan_application": {},
        "application_status": "NOT_STARTED",
        "application_initiated": False,
        
        # Verification status
        "kyc_verified": False,
        "kyc_data": {},
        
        # Underwriting status
        "eligibility_evaluation": {},
        "loan_approved": False,
        
        # Sanction letter
        "sanction_letter": {},
        
        # Interaction tracking
        "interaction_history": [],
        "offer_shown": False,
    }

@app.get("/api/customers", response_model=List[Customer])
async def get_customers():
    """Get list of available mock customers."""
    customer_list = []
    for cust_id, data in CUSTOMERS.items():
        customer_list.append(Customer(
            id=cust_id,
            name=data["name"],
            city=data["city"],
            monthly_salary=data["monthly_salary"],
            credit_score=data["credit_score"],
            pre_approved_limit=data["pre_approved_limit"]
        ))
    return customer_list

@app.post("/api/session", response_model=StateResponse)
async def create_session(request: SessionInitRequest):
    """Initialize a new session for a customer."""
    customer_id = request.customer_id
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
        
    initial_state = get_initial_state(customer_id)
    user_id = customer_id.lower()
    
    # Create session
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        state=initial_state,
    )
    
    return StateResponse(session_id=new_session.id, state=new_session.state)

@app.get("/api/state/{session_id}", response_model=StateResponse)
async def get_state(session_id: str, user_id: str):
    """Get current state of a session."""
    try:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        return StateResponse(session_id=session.id, state=session.state)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Session not found: {str(e)}")

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
        
        content = types.Content(role="user", parts=[types.Part(text=request.message)])
        
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
