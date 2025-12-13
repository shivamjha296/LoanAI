"""
Sales Agent for BFSI Loan Chatbot
Handles loan negotiations, discusses customer needs, loan amount, tenure, and interest rates
"""

from datetime import datetime
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
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

# Loan Purpose Categories with special features
LOAN_PURPOSES = {
    "TRAVEL": {
        "category": "Travel Loan",
        "description": "Fund your dream vacation - domestic or international travel",
        "typical_amount_range": "₹50,000 - ₹5,00,000",
        "special_features": [
            "Flexible repayment options",
            "Quick approval within 24 hours",
            "No end-use verification required"
        ],
        "documents_required": ["Standard KYC", "Income proof"],
        "popular_destinations": ["Europe", "Maldives", "Dubai", "Thailand", "USA"]
    },
    "MEDICAL": {
        "category": "Medical Emergency Loan",
        "description": "Cover medical expenses for treatments, surgeries, or emergencies",
        "typical_amount_range": "₹1,00,000 - ₹15,00,000",
        "special_features": [
            "Instant approval for medical emergencies",
            "Moratorium period available",
            "Lower interest rates for medical treatments",
            "Flexible EMI during recovery period"
        ],
        "documents_required": ["Medical bills/estimate", "Hospital admission letter (if applicable)"],
        "covered_expenses": ["Surgery", "Hospitalization", "Diagnostic tests", "Medication", "Dental procedures"]
    },
    "WEDDING": {
        "category": "Wedding/Marriage Loan",
        "description": "Make your special day memorable without financial stress",
        "typical_amount_range": "₹2,00,000 - ₹25,00,000",
        "special_features": [
            "Higher loan amounts for wedding expenses",
            "Flexible tenure up to 6 years",
            "Pre-wedding loan disbursal option",
            "Covers all wedding-related expenses"
        ],
        "documents_required": ["Wedding card/invitation", "Venue booking confirmation"],
        "covered_expenses": ["Venue booking", "Catering", "Photography", "Decoration", "Jewelry", "Honeymoon"]
    },
    "RENOVATION": {
        "category": "Home Renovation Loan",
        "description": "Revamp your home with our specialized renovation loan",
        "typical_amount_range": "₹1,00,000 - ₹20,00,000",
        "special_features": [
            "Disbursement in stages as per project progress",
            "Extended tenure options",
            "Lower processing fees for home improvement",
            "No property mortgage required"
        ],
        "documents_required": ["Renovation estimate/quotation", "Property ownership proof"],
        "covered_expenses": ["Interior design", "Painting", "Flooring", "Kitchen/Bathroom upgrade", "Electrical/Plumbing work"]
    },
    "EDUCATION": {
        "category": "Education Loan",
        "description": "Invest in your future with education financing",
        "typical_amount_range": "₹50,000 - ₹10,00,000",
        "special_features": [
            "Moratorium period until course completion",
            "Covers tuition and living expenses",
            "Special rates for premier institutions"
        ],
        "documents_required": ["Admission letter", "Fee structure"],
        "covered_expenses": ["Tuition fees", "Books", "Equipment", "Accommodation"]
    },
    "DEBT_CONSOLIDATION": {
        "category": "Debt Consolidation Loan",
        "description": "Consolidate multiple loans into one easy EMI",
        "typical_amount_range": "₹1,00,000 - ₹25,00,000",
        "special_features": [
            "Lower EMI burden",
            "Single EMI instead of multiple payments",
            "Potential interest rate savings",
            "Simplified debt management"
        ],
        "documents_required": ["Existing loan statements", "Credit card statements"],
        "benefits": ["Reduce monthly outflow", "Improve credit score", "Better financial planning"]
    },
    "GENERAL": {
        "category": "General Purpose Personal Loan",
        "description": "Flexible personal loan for any legitimate purpose",
        "typical_amount_range": "₹50,000 - ₹35,00,000",
        "special_features": [
            "No end-use restrictions",
            "Instant approval for pre-approved customers",
            "Flexible tenure options"
        ],
        "documents_required": ["Standard KYC", "Income proof"],
        "use_cases": ["Emergency funds", "Business startup", "Vehicle down payment", "Relocation"]
    }
}


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


def get_loan_purpose_details(purpose_key: str, tool_context: ToolContext) -> dict:
    """
    Get detailed information about specific loan purpose category.
    Use this to educate customers about special loan types and their benefits.
    
    Args:
        purpose_key: The loan purpose key (TRAVEL, MEDICAL, WEDDING, RENOVATION, EDUCATION, DEBT_CONSOLIDATION, GENERAL)
        tool_context: The tool context for state management
    
    Returns:
        dict: Detailed information about the loan purpose
    """
    purpose_key = purpose_key.upper()
    
    if purpose_key not in LOAN_PURPOSES:
        return {
            "status": "error",
            "message": f"Invalid purpose key. Available options: {', '.join(LOAN_PURPOSES.keys())}"
        }
    
    purpose_info = LOAN_PURPOSES[purpose_key]
    
    # Store selected purpose in state
    tool_context.state["loan_purpose_category"] = purpose_key
    tool_context.state["loan_purpose_details"] = purpose_info
    
    return {
        "status": "success",
        "purpose_category": purpose_info["category"],
        "description": purpose_info["description"],
        "typical_amount_range": purpose_info["typical_amount_range"],
        "special_features": purpose_info["special_features"],
        "documents_required": purpose_info["documents_required"],
        "additional_info": {
            k: v for k, v in purpose_info.items() 
            if k not in ["category", "description", "typical_amount_range", "special_features", "documents_required"]
        }
    }


def list_all_loan_purposes(tool_context: ToolContext) -> dict:
    """
    List all available loan purpose categories.
    Use this to help customers choose the right loan type.
    
    Returns:
        dict: List of all loan purposes with brief descriptions
    """
    purposes_summary = []
    
    for key, info in LOAN_PURPOSES.items():
        purposes_summary.append({
            "purpose_key": key,
            "category": info["category"],
            "description": info["description"],
            "typical_range": info["typical_amount_range"]
        })
    
    return {
        "status": "success",
        "total_categories": len(purposes_summary),
        "loan_purposes": purposes_summary,
        "message": "We offer specialized loans for various needs. Each category has unique features and benefits."
    }


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


# Create the Sales Agent - Mr. Rajesh Kumar
sales_agent = Agent(
    name="sales_agent",
    model=LiteLlm(model="mistral/mistral-large-2411"),
    description="Mr. Rajesh Kumar - Loan Specialist who negotiates loan terms, discusses customer needs, amount, tenure and interest rates",
    instruction="""
    You are Mr. Rajesh Kumar, a friendly and experienced Loan Specialist at Tata Capital Personal Loans.
    You have a warm, consultative approach and genuinely care about finding the best loan solution for each customer.

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

    **Your Role - Working Invisibly as Priya Sharma:**

    You are a BACKEND AGENT. The customer only sees "Priya Sharma".
    NEVER introduce yourself. Continue seamlessly as Priya.
    
    **IMMEDIATE ACTION REQUIRED:**
    When activated, IMMEDIATELY use get_customer_loan_offer tool.
    Do NOT just say you will check - ACTUALLY execute the tool first.
    
    **FORMATTING RULES:**
    - Use clear line breaks (\n\n) between sections
    - Format numbers: ₹2,00,000 (with commas)
    - Use bullet points (•) for lists
    - Keep tables aligned and readable
    - One EMI option per line with tenure clearly marked
    
    Example: "Let me show you the best offers available..."

    1. **Understand Customer Needs (Build Rapport)**
       - Ask about the purpose of the loan with genuine interest
         Example: "That sounds exciting! What are you planning to use the loan for?"
       - Understand how much they need and their comfortable EMI range
       - Be empathetic and conversational - make them feel comfortable

    2. **Present Personalized Loan Offers**
       - Use get_customer_loan_offer to fetch their exclusive pre-approved offer
       - Present it enthusiastically: "Great news! I have some excellent offers for you..."
       - Highlight special offers and benefits
       - Explain interest rates and fees in simple terms

    3. **EMI Calculations & Guidance**
       - Use calculate_loan_emi to show exact EMI for their requested amount
       - Use show_emi_comparison to compare different tenure options
       - Guide them: "Let me show you how this breaks down month by month..."
       - Help them choose based on their budget and goals

    4. **Professional Negotiation & Advice**
       - If requested amount exceeds pre-approved limit, explain options tactfully
       - Suggest optimal loan amounts based on their salary
       - Golden rule: Keep EMI under 50% of monthly salary for comfort
       - Be transparent about eligibility and approval chances

    5. **Initiate Application (Seamless Handoff)**
       - Once customer agrees, use initiate_loan_application
       - Celebrate: "Excellent! I've initiated your application..."
       - AUTOMATICALLY continue: "Now let me verify your details..."
       - DO NOT mention other teams
       - After initiation, IMMEDIATELY return for automatic continuation

    **Your Communication Style as Priya:**
    - NEVER introduce yourself (customer knows Priya)
    - Be conversational, friendly, professional
    - Use customer's name frequently
    - Provide exact numbers
    - Simple language, no jargon
    - Show enthusiasm
    - Be transparent

    **Important Guidelines:**
    - Never pressure customers
    - Verify understanding
    - Confirm details before applying
    - After initiation, AUTOMATICALLY transfer to next stage
    - DO NOT mention teams or handoffs

    Remember: You work INVISIBLY as Priya. Customer sees only Priya. After completing,
    IMMEDIATELY return control for automatic workflow continuation.
    """,
    tools=[
        get_customer_loan_offer,
        calculate_loan_emi,
        get_tenure_options,
        initiate_loan_application,
        show_emi_comparison
    ],
)
