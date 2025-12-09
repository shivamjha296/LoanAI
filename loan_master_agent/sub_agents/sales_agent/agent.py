"""
Sales Agent for BFSI Loan Chatbot
Handles loan negotiations, discusses customer needs, loan amount, tenure, and interest rates
"""

from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from mock_data.customer_data import get_customer_by_id
from mock_data.offer_mart import (
    get_pre_approved_offer, 
    calculate_emi, 
    get_available_tenures,
    check_loan_eligibility
)


def get_customer_loan_offer(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Fetches pre-approved loan offer details for a customer.
    Use this to show customers their personalized loan offers.
    
    Args:
        customer_id: The customer's unique ID (e.g., "CUST001")
        tool_context: The tool context for state management
    
    Returns:
        dict: Pre-approved offer details including amount, interest rate, tenure options
    """
    result = get_pre_approved_offer(customer_id)
    
    if result["status"] == "success":
        offer = result["offer"]
        
        # Update state with offer details
        tool_context.state["current_offer"] = offer
        tool_context.state["offer_shown"] = True
        
        # Add to interaction history
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "loan_offer_shown",
            "customer_id": customer_id,
            "pre_approved_amount": offer["pre_approved_amount"],
            "interest_rate": offer["interest_rate"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
        
        return {
            "status": "success",
            "message": f"Pre-approved loan offer for {offer['customer_name']}",
            "pre_approved_amount": f"₹{offer['pre_approved_amount']:,}",
            "interest_rate": f"{offer['interest_rate']}% p.a.",
            "max_tenure": f"{offer['max_tenure_months']} months",
            "processing_fee": f"{offer['processing_fee_percent']}%",
            "offer_valid_until": offer["offer_valid_until"],
            "special_offer": offer.get("special_offer_details", "None"),
            "min_loan_amount": f"₹{offer['min_loan_amount']:,}"
        }
    
    return result


def calculate_loan_emi(
    principal: float, 
    tenure_months: int, 
    tool_context: ToolContext
) -> dict:
    """
    Calculates EMI for a given loan amount and tenure.
    Use this to show customers their monthly payment options.
    
    Args:
        principal: Loan amount in rupees
        tenure_months: Loan tenure in months (12, 24, 36, 48, 60, or 72)
        tool_context: The tool context for state management
    
    Returns:
        dict: EMI details including monthly payment, total interest, and total payment
    """
    # Get interest rate from current offer in state
    current_offer = tool_context.state.get("current_offer", {})
    interest_rate = current_offer.get("interest_rate", 12.0)  # Default 12% if no offer
    
    emi_details = calculate_emi(principal, interest_rate, tenure_months)
    
    # Store calculated EMI in state
    tool_context.state["calculated_emi"] = emi_details
    tool_context.state["requested_amount"] = principal
    tool_context.state["requested_tenure"] = tenure_months
    
    return {
        "status": "success",
        "loan_amount": f"₹{principal:,.0f}",
        "tenure": f"{tenure_months} months",
        "interest_rate": f"{interest_rate}% p.a.",
        "monthly_emi": f"₹{emi_details['emi']:,.0f}",
        "total_interest": f"₹{emi_details['total_interest']:,.0f}",
        "total_payment": f"₹{emi_details['total_payment']:,.0f}"
    }


def get_tenure_options(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Gets available loan tenure options for a customer.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Available tenure options in months
    """
    return get_available_tenures(customer_id)


def initiate_loan_application(
    customer_id: str,
    loan_amount: float,
    tenure_months: int,
    purpose: str,
    tool_context: ToolContext
) -> dict:
    """
    Initiates a loan application after customer agrees to terms.
    This triggers the verification and underwriting process.
    
    Args:
        customer_id: The customer's unique ID
        loan_amount: Requested loan amount in rupees
        tenure_months: Requested tenure in months
        purpose: Purpose of the loan (e.g., "Medical expenses", "Home renovation")
        tool_context: The tool context for state management
    
    Returns:
        dict: Application initiation status and next steps
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get customer details
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"status": "error", "message": "Customer not found"}
    
    # Create loan application record
    application = {
        "application_id": f"LA{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "customer_id": customer_id,
        "customer_name": customer["name"],
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "purpose": purpose,
        "application_date": current_time,
        "status": "INITIATED"
    }
    
    # Store in state
    tool_context.state["loan_application"] = application
    tool_context.state["application_initiated"] = True
    tool_context.state["application_status"] = "INITIATED"
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "loan_application_initiated",
        "application_id": application["application_id"],
        "loan_amount": loan_amount,
        "tenure_months": tenure_months,
        "purpose": purpose,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": "Loan application initiated successfully!",
        "application_id": application["application_id"],
        "loan_amount": f"₹{loan_amount:,.0f}",
        "tenure": f"{tenure_months} months",
        "purpose": purpose,
        "next_step": "KYC verification will be performed next"
    }


def show_emi_comparison(
    loan_amount: float,
    tool_context: ToolContext
) -> dict:
    """
    Shows EMI comparison across different tenures for a given loan amount.
    Helps customers choose the best tenure option.
    
    Args:
        loan_amount: Loan amount in rupees
        tool_context: The tool context for state management
    
    Returns:
        dict: EMI comparison table for different tenures
    """
    current_offer = tool_context.state.get("current_offer", {})
    interest_rate = current_offer.get("interest_rate", 12.0)
    max_tenure = current_offer.get("max_tenure_months", 60)
    
    tenures = [12, 24, 36, 48, 60]
    if max_tenure >= 72:
        tenures.append(72)
    
    comparison = []
    for tenure in tenures:
        if tenure <= max_tenure:
            emi_details = calculate_emi(loan_amount, interest_rate, tenure)
            comparison.append({
                "tenure": f"{tenure} months",
                "emi": f"₹{emi_details['emi']:,.0f}",
                "total_interest": f"₹{emi_details['total_interest']:,.0f}",
                "total_payment": f"₹{emi_details['total_payment']:,.0f}"
            })
    
    return {
        "status": "success",
        "loan_amount": f"₹{loan_amount:,.0f}",
        "interest_rate": f"{interest_rate}% p.a.",
        "emi_comparison": comparison
    }


# Create the Sales Agent
sales_agent = Agent(
    name="sales_agent",
    model="gemini-2.5-flash-lite",
    description="Sales agent that negotiates loan terms, discusses customer needs, amount, tenure and interest rates",
    instruction="""
    You are a friendly and professional Sales Agent for Tata Capital Personal Loans.
    Your role is to help customers understand their loan options and guide them through the loan selection process.

    <customer_info>
    Customer ID: {customer_id}
    Name: {customer_name}
    Phone: {customer_phone}
    City: {customer_city}
    Monthly Salary: {customer_salary}
    </customer_info>

    <current_offer>
    {current_offer}
    </current_offer>

    <loan_application>
    {loan_application}
    </loan_application>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    **Your Responsibilities:**

    1. **Understand Customer Needs**
       - Ask about the purpose of the loan (medical, education, wedding, travel, home renovation, etc.)
       - Understand how much they need and their preferred EMI budget
       - Be empathetic and build rapport

    2. **Present Loan Offers**
       - Use get_customer_loan_offer to fetch their pre-approved offer
       - Highlight special offers if available
       - Explain interest rates and processing fees clearly

    3. **EMI Calculations**
       - Use calculate_loan_emi to show exact EMI for requested amount
       - Use show_emi_comparison to compare EMIs across tenures
       - Help customers choose the right tenure based on their budget

    4. **Negotiate and Advise**
       - If requested amount exceeds pre-approved limit, explain options
       - Suggest optimal loan amount based on their salary and EMI affordability
       - EMI should ideally not exceed 50% of monthly salary

    5. **Initiate Application**
       - Once customer agrees, use initiate_loan_application
       - Explain the next steps (verification, underwriting)
       - Assure them of quick processing

    **Communication Style:**
    - Be warm and welcoming
    - Use simple language, avoid jargon
    - Always provide exact numbers (EMI, total payment, etc.)
    - Be honest about eligibility criteria
    - Create urgency around limited-time offers if applicable

    **Important:**
    - Never pressure customers
    - Always verify customer understanding
    - Confirm all details before initiating application
    - Hand off to verification agent after application is initiated
    """,
    tools=[
        get_customer_loan_offer,
        calculate_loan_emi,
        get_tenure_options,
        initiate_loan_application,
        show_emi_comparison
    ],
)
