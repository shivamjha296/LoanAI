"""
BFSI Personal Loan Chatbot - Main Application
Tata Capital Digital Sales Assistant

This is the entry point for the multi-agent loan sales system.
Run this file to start the interactive chatbot.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from loan_master_agent.agent import loan_master_agent
from mock_data.customer_data import CUSTOMERS, get_customer_by_id
from mock_data.offer_mart import get_pre_approved_offer
from utils import (
    add_user_query_to_history,
    call_agent_async,
    display_welcome_banner,
    display_customer_offer,
    display_state,
    display_help,
    Colors
)

# Load environment variables FIRST before importing agents
load_dotenv(override=True)

# Verify Mistral API key is set
mistral_api_key = os.getenv('MISTRAL_API_KEY')
if not mistral_api_key or mistral_api_key == 'your_mistral_api_key_here':
    print(f"{Colors.RED}Error: MISTRAL_API_KEY not set in .env file{Colors.RESET}")
    print(f"{Colors.YELLOW}Please add your Mistral API key to the .env file:{Colors.RESET}")
    print(f"MISTRAL_API_KEY=your_actual_api_key")
    print(f"{Colors.YELLOW}Get your API key from: https://console.mistral.ai/{Colors.RESET}")
    sys.exit(1)

# Enable LiteLLM debug mode if needed (uncomment to debug API issues)
# import litellm
# litellm.set_verbose = True


def select_customer():
    """Allow user to select a customer from the mock database."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}Available Test Customers:{Colors.RESET}")
    print(f"{Colors.YELLOW}{'='*80}{Colors.RESET}")
    
    for idx, (cust_id, customer) in enumerate(CUSTOMERS.items(), 1):
        score_color = Colors.GREEN if customer['credit_score'] >= 750 else (
            Colors.YELLOW if customer['credit_score'] >= 700 else Colors.RED
        )
        print(f"  {idx}. {Colors.CYAN}{customer['name']:<20}{Colors.RESET} | "
              f"ID: {cust_id} | "
              f"City: {customer['city']:<12} | "
              f"Salary: ₹{customer['monthly_salary']:,} | "
              f"Credit: {score_color}{customer['credit_score']}{Colors.RESET} | "
              f"Pre-approved: ₹{customer['pre_approved_limit']:,}")
    
    print(f"{Colors.YELLOW}{'='*80}{Colors.RESET}")
    
    while True:
        try:
            choice = input(f"\n{Colors.GREEN}Select customer (1-{len(CUSTOMERS)}) or enter Customer ID: {Colors.RESET}")
            
            # Check if it's a number
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(CUSTOMERS):
                    customer_id = list(CUSTOMERS.keys())[idx - 1]
                    return customer_id
            # Check if it's a customer ID
            elif choice.upper() in CUSTOMERS:
                return choice.upper()
            
            print(f"{Colors.RED}Invalid selection. Please try again.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number or customer ID.{Colors.RESET}")


def get_initial_state(customer_id: str) -> dict:
    """Create initial state for a customer session."""
    customer = get_customer_by_id(customer_id)
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


async def main_async():
    """Main async function to run the chatbot."""
    # Constants
    APP_NAME = "Tata Capital Loan Assistant"
    
    # Display welcome banner
    display_welcome_banner()
    
    # Select customer
    customer_id = select_customer()
    customer = get_customer_by_id(customer_id)
    
    print(f"\n{Colors.GREEN}✓ Selected Customer: {customer['name']} ({customer_id}){Colors.RESET}")
    
    # Display pre-approved offer
    display_customer_offer(customer)
    
    # Initialize session service
    session_service = InMemorySessionService()
    
    # Create initial state for the customer
    initial_state = get_initial_state(customer_id)
    
    # Create user ID from customer
    USER_ID = customer_id.lower()
    
    # Create session
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    SESSION_ID = new_session.id
    print(f"{Colors.GREEN}✓ Session created: {SESSION_ID}{Colors.RESET}")
    
    # Create runner with master agent
    runner = Runner(
        agent=loan_master_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    
    print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.CYAN}Chat started! Type your message below.{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*80}{Colors.RESET}\n")
    
    # Interactive conversation loop
    while True:
        try:
            user_input = input(f"{Colors.GREEN}You: {Colors.RESET}").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle exit commands
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                print(f"\n{Colors.CYAN}Thank you for using Tata Capital Loan Assistant!{Colors.RESET}")
                print(f"{Colors.CYAN}For any queries, call 1800-XXX-XXXX (Toll Free){Colors.RESET}")
                break
            
            # Handle help command
            if user_input.lower() == "help":
                display_help()
                continue
            
            # Handle status command
            if user_input.lower() == "status":
                await display_state(session_service, APP_NAME, USER_ID, SESSION_ID, "Application Status")
                continue
            
            # Add user query to history
            await add_user_query_to_history(
                session_service, APP_NAME, USER_ID, SESSION_ID, user_input
            )
            
            # Process through agent
            await call_agent_async(runner, USER_ID, SESSION_ID, user_input)
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.CYAN}Session ended. Thank you!{Colors.RESET}")
            break
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
    
    # Show final state
    print(f"\n{Colors.YELLOW}{'='*80}{Colors.RESET}")
    print(f"{Colors.YELLOW}SESSION SUMMARY{Colors.RESET}")
    print(f"{Colors.YELLOW}{'='*80}{Colors.RESET}")
    
    final_session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    
    print(f"{Colors.CYAN}Customer:{Colors.RESET} {final_session.state.get('customer_name')}")
    print(f"{Colors.CYAN}Final Status:{Colors.RESET} {final_session.state.get('application_status')}")
    
    loan_app = final_session.state.get("loan_application", {})
    if loan_app:
        print(f"{Colors.CYAN}Loan Amount:{Colors.RESET} ₹{loan_app.get('loan_amount', 0):,.0f}")
        print(f"{Colors.CYAN}Application ID:{Colors.RESET} {loan_app.get('application_id', 'N/A')}")
    
    sanction = final_session.state.get("sanction_letter", {})
    if sanction:
        print(f"{Colors.CYAN}Sanction Reference:{Colors.RESET} {sanction.get('sanction_reference', 'N/A')}")


def main():
    """Entry point for the application."""
    print(f"{Colors.CYAN}Starting Tata Capital Loan Assistant...{Colors.RESET}\n")
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
