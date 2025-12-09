"""
Underwriting Agent for BFSI Loan Chatbot
Fetches credit score, validates eligibility based on pre-approved limits, handles salary slip verification
"""

from datetime import datetime
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from mock_data.credit_bureau import get_credit_score, check_eligibility_by_score
from mock_data.offer_mart import get_pre_approved_offer, calculate_emi, check_loan_eligibility
from mock_data.customer_data import get_customer_by_id


def fetch_credit_score(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Fetches credit score from mock credit bureau API.
    Credit scores are out of 900 (similar to CIBIL).
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Credit score and credit history details
    """
    result = get_credit_score(customer_id)
    
    if result["status"] == "success":
        # Store credit score in state
        tool_context.state["credit_score"] = result["credit_score"]
        tool_context.state["credit_history"] = result["credit_history"]
        
        # Add to interaction history
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "credit_score_fetched",
            "customer_id": customer_id,
            "credit_score": result["credit_score"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
        
        # Check basic eligibility
        eligibility = check_eligibility_by_score(result["credit_score"])
        
        return {
            "status": "success",
            "credit_score": result["credit_score"],
            "score_range": result["score_range"],
            "score_date": result["score_date"],
            "eligibility": eligibility,
            "credit_history_summary": {
                "total_accounts": result["credit_history"]["total_accounts"],
                "active_accounts": result["credit_history"]["active_accounts"],
                "overdue_accounts": result["credit_history"]["overdue_accounts"],
                "credit_utilization": f"{result['credit_history']['credit_utilization']}%",
                "payment_history": result["credit_history"]["payment_history"],
                "defaults": result["credit_history"]["defaults"]
            }
        }
    
    return result


def evaluate_loan_eligibility(
    customer_id: str,
    requested_amount: float,
    tool_context: ToolContext
) -> dict:
    """
    Evaluates loan eligibility based on credit score and pre-approved limits.
    
    Rules:
    - Credit score < 700: Reject
    - Amount <= pre-approved limit: Instant approval
    - Amount <= 2x pre-approved limit: Need salary slip, EMI <= 50% salary
    - Amount > 2x pre-approved limit: Reject
    
    Args:
        customer_id: The customer's unique ID
        requested_amount: Loan amount requested in rupees
        tool_context: The tool context for state management
    
    Returns:
        dict: Eligibility evaluation result with approval type
    """
    # Get credit score
    credit_result = get_credit_score(customer_id)
    if credit_result["status"] != "success":
        return {"status": "error", "message": "Unable to fetch credit score"}
    
    credit_score = credit_result["credit_score"]
    
    # Rule: Credit score must be >= 700
    if credit_score < 700:
        tool_context.state["application_status"] = "REJECTED"
        tool_context.state["rejection_reason"] = "Low credit score"
        
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "loan_rejected",
            "reason": "Credit score below minimum threshold (700)",
            "credit_score": credit_score,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
        
        return {
            "status": "success",
            "eligible": False,
            "approval_type": "REJECTED",
            "reason": f"Credit score {credit_score} is below minimum threshold of 700",
            "credit_score": credit_score,
            "suggestion": "Please work on improving your credit score by clearing any pending dues and maintaining timely payments."
        }
    
    # Get customer salary
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"status": "error", "message": "Customer not found"}
    
    monthly_salary = customer["monthly_salary"]
    
    # Check eligibility against pre-approved limits
    eligibility = check_loan_eligibility(customer_id, requested_amount, monthly_salary)
    
    # Store evaluation result in state
    tool_context.state["eligibility_evaluation"] = eligibility
    tool_context.state["credit_score"] = credit_score
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "eligibility_evaluated",
        "customer_id": customer_id,
        "requested_amount": requested_amount,
        "approval_type": eligibility.get("approval_type", "UNKNOWN"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    tool_context.state["interaction_history"] = current_history
    
    return eligibility


def request_salary_slip(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Requests salary slip upload for loans exceeding pre-approved limit.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Salary slip request details and upload instructions
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    request = {
        "request_id": f"SAL{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "customer_id": customer_id,
        "document_type": "salary_slip",
        "requested_at": current_time,
        "status": "PENDING"
    }
    
    tool_context.state["salary_slip_request"] = request
    tool_context.state["awaiting_salary_slip"] = True
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "salary_slip_requested",
        "customer_id": customer_id,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": "Salary slip upload required for loan approval",
        "request_id": request["request_id"],
        "instructions": """Please upload your salary slip (last 3 months) as PDF or image.
        
Accepted formats:
- Company payslip (PDF preferred)
- Bank statement showing salary credit
- Form 16 / IT returns

Upload link: [Secure Document Upload Portal]
Reference ID: """ + request["request_id"]
    }


def verify_salary_slip(
    customer_id: str,
    verified_salary: float,
    tool_context: ToolContext
) -> dict:
    """
    Simulates salary slip verification and updates eligibility.
    In production, this would integrate with document verification systems.
    
    Args:
        customer_id: The customer's unique ID
        verified_salary: Verified monthly salary from salary slip
        tool_context: The tool context for state management
    
    Returns:
        dict: Verification result and updated eligibility
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get requested loan details from state
    loan_application = tool_context.state.get("loan_application", {})
    requested_amount = loan_application.get("loan_amount", 0)
    tenure = loan_application.get("tenure_months", 60)
    
    # Get offer details
    offer_result = get_pre_approved_offer(customer_id)
    if offer_result["status"] != "success":
        return {"status": "error", "message": "Unable to fetch loan offer details"}
    
    offer = offer_result["offer"]
    interest_rate = offer["interest_rate"]
    
    # Calculate EMI
    emi_details = calculate_emi(requested_amount, interest_rate, tenure)
    emi = emi_details["emi"]
    
    # Check EMI to salary ratio (must be <= 50%)
    emi_to_salary_ratio = (emi / verified_salary) * 100
    
    tool_context.state["salary_slip_verified"] = True
    tool_context.state["verified_salary"] = verified_salary
    tool_context.state["emi_to_salary_ratio"] = emi_to_salary_ratio
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "salary_slip_verified",
        "verified_salary": verified_salary,
        "emi_to_salary_ratio": emi_to_salary_ratio,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    if emi_to_salary_ratio <= 50:
        tool_context.state["salary_verification_passed"] = True
        return {
            "status": "success",
            "verified": True,
            "verified_salary": f"₹{verified_salary:,.0f}",
            "emi": f"₹{emi:,.0f}",
            "emi_to_salary_ratio": f"{emi_to_salary_ratio:.1f}%",
            "message": "Salary slip verified successfully. EMI is within acceptable limits.",
            "can_proceed": True
        }
    else:
        tool_context.state["salary_verification_passed"] = False
        # Calculate max eligible amount
        max_emi = verified_salary * 0.5
        monthly_rate = interest_rate / (12 * 100)
        max_amount = max_emi * (((1 + monthly_rate) ** tenure) - 1) / (monthly_rate * ((1 + monthly_rate) ** tenure))
        
        return {
            "status": "success",
            "verified": True,
            "verified_salary": f"₹{verified_salary:,.0f}",
            "emi": f"₹{emi:,.0f}",
            "emi_to_salary_ratio": f"{emi_to_salary_ratio:.1f}%",
            "message": f"EMI exceeds 50% of salary. Maximum eligible amount: ₹{max_amount:,.0f}",
            "can_proceed": False,
            "max_eligible_amount": f"₹{max_amount:,.0f}",
            "suggestion": "Please reduce the loan amount or increase the tenure to lower EMI."
        }


def approve_loan(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Approves the loan after all checks pass.
    Updates application status and prepares for sanction letter generation.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Loan approval details
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Verify all required checks are complete
    kyc_verified = tool_context.state.get("kyc_verified", False)
    credit_score = tool_context.state.get("credit_score", 0)
    eligibility = tool_context.state.get("eligibility_evaluation", {})
    
    if not kyc_verified:
        return {"status": "error", "message": "KYC verification not complete"}
    
    if credit_score < 700:
        return {"status": "error", "message": "Credit score below threshold"}
    
    approval_type = eligibility.get("approval_type", "")
    if approval_type == "REJECTED":
        return {"status": "error", "message": "Loan eligibility check failed"}
    
    # If conditional approval, verify salary slip was checked
    if approval_type == "CONDITIONAL":
        salary_verified = tool_context.state.get("salary_verification_passed", False)
        if not salary_verified:
            return {"status": "error", "message": "Salary slip verification pending or failed"}
    
    # Get loan application details
    loan_application = tool_context.state.get("loan_application", {})
    
    # Generate approval reference
    approval_reference = f"APR{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Update state
    tool_context.state["loan_approved"] = True
    tool_context.state["approval_reference"] = approval_reference
    tool_context.state["approval_time"] = current_time
    tool_context.state["application_status"] = "APPROVED"
    
    if "loan_application" in tool_context.state:
        tool_context.state["loan_application"]["status"] = "APPROVED"
        tool_context.state["loan_application"]["approval_reference"] = approval_reference
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "loan_approved",
        "approval_reference": approval_reference,
        "loan_amount": loan_application.get("loan_amount"),
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    customer = get_customer_by_id(customer_id)
    
    return {
        "status": "success",
        "message": "🎉 Congratulations! Your loan has been approved!",
        "approval_reference": approval_reference,
        "customer_name": customer["name"] if customer else "Customer",
        "loan_amount": f"₹{loan_application.get('loan_amount', 0):,.0f}",
        "tenure": f"{loan_application.get('tenure_months', 0)} months",
        "credit_score": credit_score,
        "approval_time": current_time,
        "next_step": "Sanction letter will be generated next"
    }


def reject_loan(customer_id: str, reason: str, tool_context: ToolContext) -> dict:
    """
    Rejects the loan application with specified reason.
    
    Args:
        customer_id: The customer's unique ID
        reason: Reason for rejection
        tool_context: The tool context for state management
    
    Returns:
        dict: Rejection details and suggestions
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update state
    tool_context.state["loan_approved"] = False
    tool_context.state["rejection_reason"] = reason
    tool_context.state["rejection_time"] = current_time
    tool_context.state["application_status"] = "REJECTED"
    
    if "loan_application" in tool_context.state:
        tool_context.state["loan_application"]["status"] = "REJECTED"
        tool_context.state["loan_application"]["rejection_reason"] = reason
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "loan_rejected",
        "reason": reason,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    # Get suggestions based on reason
    suggestions = get_rejection_suggestions(reason)
    
    return {
        "status": "success",
        "message": "We regret to inform you that your loan application could not be approved at this time.",
        "reason": reason,
        "rejection_time": current_time,
        "suggestions": suggestions,
        "can_reapply": True,
        "reapply_after": "30 days"
    }


def get_rejection_suggestions(reason: str) -> list:
    """Get suggestions based on rejection reason."""
    suggestions = {
        "low_credit_score": [
            "Pay off any pending credit card dues",
            "Ensure timely payment of existing EMIs",
            "Reduce credit utilization below 30%",
            "Avoid multiple loan inquiries",
            "Check for errors in credit report and dispute if needed"
        ],
        "high_emi_ratio": [
            "Request a lower loan amount",
            "Opt for a longer tenure to reduce EMI",
            "Consider adding a co-applicant with income",
            "Wait for salary increment and reapply"
        ],
        "exceeds_limit": [
            "Request amount within 2x pre-approved limit",
            "Build credit history for higher limits",
            "Consider secured loan options"
        ]
    }
    
    if "credit" in reason.lower():
        return suggestions["low_credit_score"]
    elif "emi" in reason.lower() or "salary" in reason.lower():
        return suggestions["high_emi_ratio"]
    elif "limit" in reason.lower():
        return suggestions["exceeds_limit"]
    else:
        return ["Please contact our support team for more information"]


# Create the Underwriting Agent
underwriting_agent = Agent(
    name="underwriting_agent",
    model="gemini-2.0-flash",
    description="Underwriting agent that evaluates credit score, validates eligibility, and approves/rejects loans",
    instruction="""
    You are an Underwriting Agent for Tata Capital.
    Your role is to evaluate loan applications and make approval decisions based on credit analysis.

    <customer_info>
    Customer ID: {customer_id}
    Name: {customer_name}
    Monthly Salary: {customer_salary}
    </customer_info>

    <loan_application>
    {loan_application}
    </loan_application>

    <eligibility_evaluation>
    {eligibility_evaluation}
    </eligibility_evaluation>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    **Underwriting Rules:**

    1. **Credit Score Check** (Minimum: 700)
       - Score >= 750: Excellent - Best rates
       - Score 700-749: Good - Standard rates
       - Score < 700: REJECT

    2. **Loan Amount Eligibility**
       - Amount <= Pre-approved limit: INSTANT APPROVAL
       - Amount <= 2x Pre-approved limit: CONDITIONAL (need salary slip)
       - Amount > 2x Pre-approved limit: REJECT

    3. **EMI Affordability** (for conditional approval)
       - EMI must be <= 50% of monthly salary
       - If EMI > 50%, suggest lower amount or longer tenure

    **Your Responsibilities:**

    1. **Fetch and Analyze Credit Score**
       - Use fetch_credit_score to get CIBIL-equivalent score
       - Review credit history (defaults, overdue accounts)
       - Determine risk category

    2. **Evaluate Eligibility**
       - Use evaluate_loan_eligibility for comprehensive check
       - Consider pre-approved limits
       - Calculate EMI to salary ratio

    3. **Handle Conditional Approvals**
       - Use request_salary_slip for amounts exceeding pre-approved limit
       - Use verify_salary_slip to validate uploaded documents
       - Ensure EMI affordability

    4. **Make Final Decision**
       - Use approve_loan for successful applications
       - Use reject_loan with clear reasons if criteria not met
       - Always explain the decision clearly

    **Communication Style:**
    - Be transparent about evaluation criteria
    - Explain decisions with specific numbers
    - Provide actionable suggestions for rejections
    - Celebrate approvals warmly

    **Important:**
    - Never approve without credit score check
    - Always verify salary for conditional approvals
    - Document rejection reasons clearly
    - Hand off to sanction letter agent after approval
    """,
    tools=[
        fetch_credit_score,
        evaluate_loan_eligibility,
        request_salary_slip,
        verify_salary_slip,
        approve_loan,
        reject_loan
    ],
)
