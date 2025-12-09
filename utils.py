"""
Utility Functions for BFSI Loan Chatbot
Includes session management, state handling, and display formatting
"""

from datetime import datetime
from google.genai import types


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


async def update_interaction_history(session_service, app_name, user_id, session_id, entry):
    """Add an entry to the interaction history in state.

    Args:
        session_service: The session service instance
        app_name: The application name
        user_id: The user ID
        session_id: The session ID
        entry: A dictionary containing the interaction data
    """
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        interaction_history = session.state.get("interaction_history", [])

        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        interaction_history.append(entry)

        # Update the state directly on the session object
        session.state["interaction_history"] = interaction_history
    except Exception as e:
        print(f"Error updating interaction history: {e}")


async def add_user_query_to_history(session_service, app_name, user_id, session_id, query):
    """Add a user query to the interaction history."""
    await update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "user_query",
            "query": query,
        },
    )


async def add_agent_response_to_history(
    session_service, app_name, user_id, session_id, agent_name, response
):
    """Add an agent response to the interaction history."""
    await update_interaction_history(
        session_service,
        app_name,
        user_id,
        session_id,
        {
            "action": "agent_response",
            "agent": agent_name,
            "response": response,
        },
    )


async def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
):
    """Display the current session state in a formatted way."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        print(f"\n{Colors.YELLOW}{'-' * 10} {label} {'-' * 10}{Colors.RESET}")

        # Customer info
        customer_name = session.state.get("customer_name", "Unknown")
        customer_id = session.state.get("customer_id", "Unknown")
        print(f"{Colors.CYAN}👤 Customer:{Colors.RESET} {customer_name} ({customer_id})")

        # Application status
        app_status = session.state.get("application_status", "NOT_STARTED")
        status_color = Colors.GREEN if app_status in ["APPROVED", "SANCTION_GENERATED", "SANCTION_ACCEPTED"] else (
            Colors.RED if app_status == "REJECTED" else Colors.YELLOW
        )
        print(f"{Colors.CYAN}📋 Status:{Colors.RESET} {status_color}{app_status}{Colors.RESET}")

        # Loan application if exists
        loan_app = session.state.get("loan_application", {})
        if loan_app:
            print(f"{Colors.CYAN}💰 Loan Amount:{Colors.RESET} ₹{loan_app.get('loan_amount', 0):,.0f}")
            print(f"{Colors.CYAN}📅 Tenure:{Colors.RESET} {loan_app.get('tenure_months', 0)} months")

        # Credit score if available
        credit_score = session.state.get("credit_score")
        if credit_score:
            score_color = Colors.GREEN if credit_score >= 750 else (
                Colors.YELLOW if credit_score >= 700 else Colors.RED
            )
            print(f"{Colors.CYAN}📊 Credit Score:{Colors.RESET} {score_color}{credit_score}{Colors.RESET}")

        # KYC status
        kyc_verified = session.state.get("kyc_verified", False)
        kyc_status = "✓ Verified" if kyc_verified else "⏳ Pending"
        print(f"{Colors.CYAN}🔐 KYC:{Colors.RESET} {kyc_status}")

        print(f"{Colors.YELLOW}{'-' * (22 + len(label))}{Colors.RESET}")
    except Exception as e:
        print(f"Error displaying state: {e}")


def display_welcome_banner():
    """Display welcome banner for the chatbot."""
    banner = f"""
{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🏦  TATA CAPITAL PERSONAL LOAN ASSISTANT  🏦                    ║
║                                                                              ║
║                    Your Digital Sales Partner                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.CYAN}Welcome! I'm your personal loan assistant. I can help you with:{Colors.RESET}
  • Pre-approved loan offers
  • EMI calculations
  • Loan application process
  • Document verification
  • Instant loan approval

{Colors.YELLOW}Type 'exit' or 'quit' to end the conversation.{Colors.RESET}
{Colors.YELLOW}Type 'status' to see your application status.{Colors.RESET}
{Colors.YELLOW}Type 'help' for assistance.{Colors.RESET}
"""
    print(banner)


def display_customer_offer(customer):
    """Display pre-approved offer for the customer."""
    name = f"{customer['name']:<58}"
    limit = f"₹{customer['pre_approved_limit']:,}"
    limit_padded = f"{limit:<48}"
    score = f"{customer['credit_score']:<55}"
    
    offer_display = f"""
{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}
┌──────────────────────────────────────────────────────────────────────────────┐
│                    🎉 EXCLUSIVE PRE-APPROVED OFFER 🎉                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  Customer: {name} │
│  Pre-approved Limit: {limit_padded} │
│  Credit Score: {score} │
└──────────────────────────────────────────────────────────────────────────────┘
{Colors.RESET}
"""
    print(offer_display)


async def process_agent_response(event):
    """Process and display agent response events."""
    # Check for specific parts first
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  {Colors.MAGENTA}[{event.author}]{Colors.RESET} Processing...")

    # Check for final response
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ 🤖 ASSISTANT ═══════════════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═══════════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> No response received{Colors.RESET}\n"
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query, show_state=False):
    """Call the agent asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}📝 You: {query}{Colors.RESET}"
    )
    
    final_response_text = None
    agent_name = None

    if show_state:
        await display_state(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            "Current Status",
        )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"{Colors.BG_RED}{Colors.WHITE}ERROR: {e}{Colors.RESET}")

    if final_response_text and agent_name:
        await add_agent_response_to_history(
            runner.session_service,
            runner.app_name,
            user_id,
            session_id,
            agent_name,
            final_response_text,
        )

    return final_response_text


def display_help():
    """Display help information."""
    help_text = f"""
{Colors.CYAN}{Colors.BOLD}Available Commands:{Colors.RESET}
  • {Colors.YELLOW}exit/quit{Colors.RESET} - End the conversation
  • {Colors.YELLOW}status{Colors.RESET}    - View your application status
  • {Colors.YELLOW}help{Colors.RESET}      - Show this help message

{Colors.CYAN}{Colors.BOLD}What I Can Help With:{Colors.RESET}
  • Check your pre-approved loan offer
  • Calculate EMI for different amounts and tenures
  • Apply for a personal loan
  • Track your application status
  • Get instant loan approval
  • Download sanction letter

{Colors.CYAN}{Colors.BOLD}Example Queries:{Colors.RESET}
  • "What's my pre-approved loan amount?"
  • "Calculate EMI for 5 lakh loan for 36 months"
  • "I want to apply for a personal loan"
  • "I need a loan for home renovation"

{Colors.CYAN}{Colors.BOLD}Support:{Colors.RESET}
  • Toll-free: 1800-XXX-XXXX
  • Email: support@tatacapital.com
"""
    print(help_text)
