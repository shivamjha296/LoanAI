
import asyncio
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from loan_master_agent.agent import loan_master_agent
from mock_data.customer_data import get_customer_by_id
from mock_data.offer_mart import get_pre_approved_offer

load_dotenv(override=True)

async def debug_run():
    customer_id = "CUST001" # Rajesh Kumar
    app_name = "DebugApp"
    user_id = customer_id.lower()
    
    session_service = InMemorySessionService()
    
    # Initial state setup (same as server.py)
    customer = get_customer_by_id(customer_id)
    offer_result = get_pre_approved_offer(customer_id)
    offer = offer_result.get("offer", {}) if offer_result["status"] == "success" else {}
    
    initial_state = {
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "customer_phone": customer["phone"],
        "customer_email": customer["email"],
        "customer_city": customer["city"],
        "customer_salary": customer["monthly_salary"],
        "pre_approved_limit": customer["pre_approved_limit"],
        "credit_score": customer["credit_score"],
        "current_offer": offer,
        "loan_application": {},
        "application_status": "NOT_STARTED",
        "interaction_history": [],
        "offer_shown": False,
    }
    
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        state=initial_state,
    )
    
    runner = Runner(
        agent=loan_master_agent,
        app_name=app_name,
        session_service=session_service,
    )
    
    print("--- Sending: I want a personal loan ---")
    content1 = types.Content(role="user", parts=[types.Part(text="I want a personal loan")])
    async for event in runner.run_async(user_id=user_id, session_id=session.id, new_message=content1):
        if event.is_final_response():
            print(f"Response 1: {event.content.parts[0].text}")

    print("\n--- Sending: For home renovation ---")
    content2 = types.Content(role="user", parts=[types.Part(text="For home renovation")])
    async for event in runner.run_async(user_id=user_id, session_id=session.id, new_message=content2):
        if event.is_final_response():
            print(f"Response 2: {event.content.parts[0].text}")

if __name__ == "__main__":
    asyncio.run(debug_run())
