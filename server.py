
import asyncio
import os
import sys
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from loan_master_agent.agent import loan_master_agent
from mock_data.customer_data import CUSTOMERS, get_customer_by_id
from mock_data.offer_mart import get_pre_approved_offer

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
