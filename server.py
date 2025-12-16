
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
import hashlib
import litellm

from loan_master_agent.agent import loan_master_agent
from mock_data.customer_data import CUSTOMERS, get_customer_by_id
from mock_data.offer_mart import get_pre_approved_offer
from mock_data.campaign_data import get_campaign_data, get_personalized_opening
from email_utils import send_email_with_attachment, send_sanction_letter_for_session

# Load environment variables
load_dotenv(override=True)

# Configure litellm for Mistral compatibility with short tool call IDs
import litellm
litellm.drop_params = True  # Drop unsupported parameters
os.environ["LITELLM_DROP_PARAMS"] = "True"

# Patch ADK's tool call ID generation at the genai level
from google import genai
original_content_init = genai.types.Content.__init__ if hasattr(genai.types.Content, '__init__') else None

# Monkey patch to fix tool call IDs for Mistral at multiple levels
original_completion = litellm.completion
tool_call_id_map = {}  # Map long IDs to short IDs

def generate_short_id(long_id: str) -> str:
    """Generate or retrieve a consistent 9-char ID for a long tool call ID."""
    if long_id not in tool_call_id_map:
        tool_call_id_map[long_id] = hashlib.md5(long_id.encode()).hexdigest()[:9]
    return tool_call_id_map[long_id]

def patched_completion(*args, **kwargs):
    """Wrapper to ensure tool call IDs are Mistral-compatible (9 chars max)."""
    # Fix tool call IDs in REQUEST (messages being sent TO Mistral)
    if 'messages' in kwargs:
        for message in kwargs['messages']:
            if isinstance(message, dict):
                # Fix tool_calls in assistant messages
                if message.get('tool_calls'):
                    for tool_call in message['tool_calls']:
                        if 'id' in tool_call and len(tool_call['id']) > 9:
                            tool_call['id'] = generate_short_id(tool_call['id'])
                # Fix tool_call_id in tool result messages
                if message.get('tool_call_id') and len(message['tool_call_id']) > 9:
                    message['tool_call_id'] = generate_short_id(message['tool_call_id'])
    
    result = original_completion(*args, **kwargs)
    
    # Fix tool call IDs in RESPONSE (from Mistral)
    if hasattr(result, 'choices') and result.choices:
        for choice in result.choices:
            if hasattr(choice, 'message') and hasattr(choice.message, 'tool_calls') and choice.message.tool_calls:
                for tool_call in choice.message.tool_calls:
                    if hasattr(tool_call, 'id') and len(tool_call.id) > 9:
                        short_id = generate_short_id(tool_call.id)
                        tool_call.id = short_id
    
    return result

litellm.completion = patched_completion

# Utility function to generate short tool call IDs for Mistral
def generate_short_tool_call_id(original_id: str) -> str:
    """Generate a 9-character tool call ID from the original ID for Mistral compatibility."""
    # Use first 9 characters of MD5 hash (alphanumeric)
    hash_obj = hashlib.md5(original_id.encode())
    return hash_obj.hexdigest()[:9]

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

class ChatResponse(BaseModel):
    response: str
    agent: str
    session_id: str

class StateResponse(BaseModel):
    state: Dict[str, Any]

@app.get("/api/customers")
async def get_customers():
    """Get all available customers."""
    return [
        {
            "id": customer_data["customer_id"],
            "name": customer_data["name"],
            "city": customer_data["city"],
            "monthly_salary": customer_data["monthly_salary"],
            "credit_score": customer_data["credit_score"],
            "pre_approved_limit": customer_data["pre_approved_limit"]
        }
        for customer_id, customer_data in CUSTOMERS.items()
    ]

@app.post("/api/session")
@app.post("/api/init-session")
async def create_session(request: SessionInitRequest):
    """Initialize a new chat session for a customer."""
    try:
        customer = get_customer_by_id(request.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Generate session ID
        session_id = f"session_{request.customer_id}_{int(asyncio.get_event_loop().time())}"
        
        # Get campaign data and offers
        campaign_data = get_campaign_data(request.customer_id)
        offers = get_pre_approved_offer(request.customer_id)
        
        # Get personalized opening
        personalized_opening = get_personalized_opening(
            request.customer_id,
            customer["name"],
            campaign_data
        )
        
        # Create initial state with parallel processing pre-fetch
        from mock_data.crm_data import get_kyc_data
        from mock_data.credit_bureau import get_credit_score
        
        # Pre-fetch data in parallel
        kyc_data = get_kyc_data(request.customer_id)
        credit_data = get_credit_score(request.customer_id)
        
        initial_state = {
            "customer_id": request.customer_id,
            "customer_name": customer["name"],
            "customer_phone": customer.get("phone", "N/A"),
            "customer_city": customer["city"],
            "customer_salary": customer["monthly_salary"],
            "pre_approved_limit": customer["pre_approved_limit"],
            "credit_score": customer["credit_score"],
            "current_offer": offers.get("offer_1", {}),
            "loan_application": {},
            "application_status": "NOT_STARTED",
            "interaction_history": [],
            "campaign_source": campaign_data.get("source", "Direct"),
            "customer_intent": campaign_data.get("intent", "GENERAL"),
            "urgency_level": campaign_data.get("urgency_level", "MEDIUM"),
            "campaign_keyword": campaign_data.get("keyword", "personal loan"),
            "customer_type": campaign_data.get("customer_type", "NEW_CUSTOMER"),
            "relationship_tenure_years": campaign_data.get("relationship_tenure_years", 0),
            "payment_history": campaign_data.get("payment_history", "N/A"),
            "current_loans_count": campaign_data.get("current_loans_count", 0),
            "previous_interactions_count": campaign_data.get("previous_interactions_count", 0),
            "offer_expiry_hours": campaign_data.get("offer_expiry_hours", 120),
            "persuasion_strategy": "",
            "personalized_opening": personalized_opening,
            "objection_handling_context": "",
            "sentiment_adaptive_strategy": "",
            "history": [],
            "kyc_data": {},  # Initialize empty kyc_data to prevent context variable errors
            "eligibility_evaluation": {},  # Initialize empty eligibility_evaluation
            "sanction_letter": {},  # Initialize empty sanction_letter
            "_prefetched_kyc": kyc_data,
            "_prefetched_credit": credit_data,
            "_parallel_processing_enabled": True,
        }
        
        # Create session
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.customer_id,
            session_id=session_id,
            state=initial_state
        )
        
        return {
            "session_id": session_id,
            "customer_id": request.customer_id,
            "customer_name": customer["name"],
            "greeting": personalized_opening
        }
    except Exception as e:
        print(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/state/{session_id}")
async def get_state(session_id: str, user_id: str):
    """Get current session state."""
    try:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"state": session.state if hasattr(session, 'state') else {}}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a user message."""
    try:
        # Check if session exists, if not create it automatically
        existing_session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        if existing_session is None:
            print(f"Session not found, creating new session: {request.session_id}")
            # Auto-create session with default state
            customer = get_customer_by_id(request.user_id)
            if customer:
                campaign_data = get_campaign_data(request.user_id)
                offers = get_pre_approved_offer(request.user_id)
                from mock_data.crm_data import get_kyc_data
                from mock_data.credit_bureau import get_credit_score
                
                kyc_data = get_kyc_data(request.user_id)
                credit_data = get_credit_score(request.user_id)
                personalized_opening = get_personalized_opening(
                    request.user_id,
                    customer["name"],
                    campaign_data
                )
                
                initial_state = {
                    "customer_id": request.user_id,
                    "customer_name": customer["name"],
                    "customer_phone": customer.get("phone", "N/A"),
                    "customer_city": customer["city"],
                    "customer_salary": customer["monthly_salary"],
                    "pre_approved_limit": customer["pre_approved_limit"],
                    "credit_score": customer["credit_score"],
                    "current_offer": offers.get("offer_1", {}),
                    "loan_application": {},
                    "application_status": "NOT_STARTED",
                    "interaction_history": [],
                    "campaign_source": campaign_data.get("source", "Direct"),
                    "customer_intent": campaign_data.get("intent", "GENERAL"),
                    "urgency_level": campaign_data.get("urgency_level", "MEDIUM"),
                    "campaign_keyword": campaign_data.get("keyword", "personal loan"),
                    "customer_type": campaign_data.get("customer_type", "NEW_CUSTOMER"),
                    "relationship_tenure_years": campaign_data.get("relationship_tenure_years", 0),
                    "payment_history": campaign_data.get("payment_history", "N/A"),
                    "current_loans_count": campaign_data.get("current_loans_count", 0),
                    "previous_interactions_count": campaign_data.get("previous_interactions_count", 0),
                    "offer_expiry_hours": campaign_data.get("offer_expiry_hours", 120),
                    "persuasion_strategy": "",
                    "personalized_opening": personalized_opening,
                    "objection_handling_context": "",
                    "sentiment_adaptive_strategy": "",
                    "history": [],
                    "kyc_data": {},
                    "eligibility_evaluation": {},
                    "sanction_letter": {},
                    "_prefetched_kyc": kyc_data,
                    "_prefetched_credit": credit_data,
                    "_parallel_processing_enabled": True,
                }
                
                await session_service.create_session(
                    app_name=APP_NAME,
                    user_id=request.user_id,
                    session_id=request.session_id,
                    state=initial_state
                )
                print(f"Session created successfully: {request.session_id}")
        
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
            return ChatResponse(
                response="I'm sorry, I didn't get that. Could you please repeat?",
                agent="System",
                session_id=request.session_id
            )
            
        return ChatResponse(
            response=final_response_text,
            agent=agent_name,
            session_id=request.session_id
        )
        
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
        
        if session is None:
            print(f"ERROR: Session not found for session_id={session_id}, user_id={user_id}")
            raise HTTPException(status_code=404, detail="Session not found")
        
        sanction_letter = session.state.get("sanction_letter", {})
        print(f"DEBUG: sanction_letter data: {sanction_letter}")
        
        pdf_file_path = sanction_letter.get("pdf_file_path")
        print(f"DEBUG: pdf_file_path from state: {pdf_file_path}")
        
        if not pdf_file_path:
            print(f"ERROR: pdf_file_path is None or empty in session state")
            
            # Try to find PDF by looking for existing files with customer_id
            sanction_ref = sanction_letter.get("sanction_reference", "")
            if sanction_ref:
                pdf_dir = Path("sanction_letters")
                pattern = f"Sanction_Letter_{user_id}_{sanction_ref}.pdf"
                possible_path = pdf_dir / pattern
                print(f"DEBUG: Checking for PDF at: {possible_path}")
                
                if possible_path.exists():
                    print(f"SUCCESS: Found PDF file at fallback location: {possible_path}")
                    pdf_file_path = str(possible_path)
                    # Update state for future requests
                    sanction_letter["pdf_file_path"] = pdf_file_path
                    session.state["sanction_letter"] = sanction_letter
                else:
                    print(f"ERROR: PDF file not found even at fallback location")
                    raise HTTPException(
                        status_code=404,
                        detail=f"Sanction letter PDF not found. Please ask the agent to generate the PDF using the 'generate_sanction_letter_pdf' function."
                    )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="Sanction letter PDF path not found in session state. Please generate the sanction letter first."
                )
        
        if not Path(pdf_file_path).exists():
            print(f"ERROR: PDF file does not exist at path: {pdf_file_path}")
            raise HTTPException(status_code=404, detail=f"Sanction letter PDF file not found at: {pdf_file_path}")
        
        print(f"SUCCESS: Returning PDF file from: {pdf_file_path}")
        return FileResponse(
            pdf_file_path,
            media_type="application/pdf",
            filename=f"sanction_letter_{sanction_letter.get('sanction_reference', 'document')}.pdf"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in download_sanction_letter: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error downloading sanction letter: {str(e)}")


@app.post("/api/send-sanction-letter/{session_id}")
async def send_sanction_letter(session_id: str, user_id: str):
    """Send the sanction letter PDF via SMTP to the customer's email.

    Requires SMTP credentials in environment: `SMTP_EMAIL` and `SMTP_PASSWORD`.
    """
    try:
        # Get session state
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        if session is None:
            raise HTTPException(status_code=404, detail="Session not found")

        state = session.state if hasattr(session, 'state') else {}

        sanction_letter = state.get("sanction_letter", {})
        pdf_file_path = sanction_letter.get("pdf_file_path")
        if not pdf_file_path or not Path(pdf_file_path).exists():
            raise HTTPException(status_code=404, detail="Sanction letter PDF not found for this session")

        # Determine recipient email
        to_email = state.get("customer_email")
        if not to_email:
            # fallback to customer record
            customer = get_customer_by_id(state.get("customer_id"))
            to_email = customer.get("email") if customer else None

        if not to_email:
            raise HTTPException(status_code=400, detail="Customer email not available")

        smtp_user = os.getenv("SMTP_EMAIL")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "465"))

        if not smtp_user or not smtp_password:
            raise HTTPException(status_code=500, detail="SMTP_EMAIL and SMTP_PASSWORD must be set in environment")

        subject = f"Sanction Letter - {sanction_letter.get('sanction_reference', '')}"
        body = (
            f"Dear {state.get('customer_name', '')},\n\n"
            "Please find attached your sanction letter for the loan application.\n\n"
            "Regards,\nTata Capital Loan Assistant"
        )

        # Send email
        send_email_with_attachment(
            smtp_user=smtp_user,
            smtp_password=smtp_password,
            to_email=to_email,
            subject=subject,
            body=body,
            attachment_path=pdf_file_path,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
        )

        return {"status": "sent", "to": to_email}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error sending sanction letter: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Admin API Endpoints
@app.get("/api/admin/customers")
async def get_admin_customers():
    """Get all customers for admin panel."""
    from mock_data.customer_data import CUSTOMERS
    return [
        {
            "id": customer_data["customer_id"],
            "name": customer_data["name"],
            "age": customer_data.get("age", "N/A"),
            "city": customer_data["city"],
            "credit_score": customer_data["credit_score"],
            "pre_approved_limit": customer_data["pre_approved_limit"],
            "monthly_salary": customer_data["monthly_salary"],
        }
        for customer_id, customer_data in CUSTOMERS.items()
    ]

@app.get("/api/admin/offers")
async def get_admin_offers():
    """Get all offers from offer mart."""
    from mock_data.offer_mart import LOAN_OFFERS
    offers = []
    for customer_id, offer_data in LOAN_OFFERS.items():
        offers.append({
            "customer_id": customer_id,
            "amount": offer_data.get("pre_approved_amount", 0),
            "interest_rate": offer_data.get("interest_rate", 0),
            "tenure_options": f"{offer_data.get('max_tenure_months', 0)} months",
            "processing_fee": int(offer_data.get("pre_approved_amount", 0) * offer_data.get("processing_fee_percent", 0) / 100),
        })
    return offers

@app.get("/api/admin/kyc")
async def get_admin_kyc():
    """Get all KYC data from CRM."""
    from mock_data.crm_data import CRM_DATA
    return [
        {
            "customer_id": customer_id,
            "name": kyc_data.get("name", "N/A"),
            "pan_number": kyc_data.get("pan_number", "N/A"),
            "aadhar_number": kyc_data.get("aadhar_number", "N/A"),
            "phone_verified": kyc_data.get("phone_verified", False),
            "kyc_status": kyc_data.get("kyc_status", "PENDING"),
        }
        for customer_id, kyc_data in CRM_DATA.items()
    ]

@app.get("/api/admin/credit")
async def get_admin_credit():
    """Get all credit scores from credit bureau."""
    from mock_data.credit_bureau import CREDIT_SCORES
    return [
        {
            "customer_id": customer_id,
            "credit_score": credit_data.get("credit_score", 0),
            "score_range": credit_data.get("score_range", "N/A"),
            "total_accounts": credit_data.get("credit_history", {}).get("total_accounts", 0),
            "active_accounts": credit_data.get("credit_history", {}).get("active_accounts", 0),
            "payment_history": credit_data.get("credit_history", {}).get("payment_history", "N/A"),
        }
        for customer_id, credit_data in CREDIT_SCORES.items()
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
