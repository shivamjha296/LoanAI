"""
Sanction Letter Generator Agent for BFSI Loan Chatbot
Generates automated PDF sanction letters for approved loans
"""

from datetime import datetime, timedelta
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from mock_data.customer_data import get_customer_by_id
from mock_data.offer_mart import calculate_emi


def generate_sanction_letter(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Generates a sanction letter for approved loan.
    Creates PDF document with all loan details and terms.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Sanction letter details and download link
    """
    current_time = datetime.now()
    
    # Check if loan is approved
    if not tool_context.state.get("loan_approved", False):
        return {
            "status": "error",
            "message": "Loan is not approved. Cannot generate sanction letter."
        }
    
    # Get all required details from state
    loan_application = tool_context.state.get("loan_application", {})
    approval_reference = tool_context.state.get("approval_reference", "")
    current_offer = tool_context.state.get("current_offer", {})
    
    if not loan_application:
        return {
            "status": "error",
            "message": "Loan application details not found."
        }
    
    # Get customer details
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"status": "error", "message": "Customer not found"}
    
    # Calculate EMI and other details
    loan_amount = loan_application.get("loan_amount", 0)
    tenure = loan_application.get("tenure_months", 60)
    interest_rate = current_offer.get("interest_rate", 12.0)
    processing_fee_percent = current_offer.get("processing_fee_percent", 1.5)
    
    emi_details = calculate_emi(loan_amount, interest_rate, tenure)
    processing_fee = loan_amount * (processing_fee_percent / 100)
    disbursement_amount = loan_amount - processing_fee
    
    # Generate sanction letter reference
    sanction_ref = f"SL{current_time.strftime('%Y%m%d%H%M%S')}"
    
    # Calculate dates
    sanction_date = current_time.strftime("%d-%m-%Y")
    validity_date = (current_time + timedelta(days=30)).strftime("%d-%m-%Y")
    first_emi_date = (current_time + timedelta(days=45)).strftime("%d-%m-%Y")
    
    # Create sanction letter content
    sanction_letter = {
        "sanction_reference": sanction_ref,
        "approval_reference": approval_reference,
        "sanction_date": sanction_date,
        "validity_until": validity_date,
        
        "borrower_details": {
            "name": customer["name"],
            "customer_id": customer_id,
            "pan": customer["pan_number"],
            "address": f"{customer['city']}",
            "phone": customer["phone"],
            "email": customer["email"]
        },
        
        "loan_details": {
            "loan_type": "Personal Loan",
            "sanctioned_amount": loan_amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure,
            "emi": emi_details["emi"],
            "total_interest": emi_details["total_interest"],
            "total_repayment": emi_details["total_payment"],
            "processing_fee": processing_fee,
            "disbursement_amount": disbursement_amount,
            "first_emi_date": first_emi_date,
            "purpose": loan_application.get("purpose", "Personal Use")
        },
        
        "disbursement_details": {
            "bank_name": customer["bank_name"],
            "account_number": customer["account_number"],
            "disbursement_mode": "NEFT/IMPS",
            "expected_disbursement": "Within 24-48 hours of document submission"
        }
    }
    
    # Store in state
    tool_context.state["sanction_letter"] = sanction_letter
    tool_context.state["sanction_reference"] = sanction_ref
    tool_context.state["application_status"] = "SANCTION_GENERATED"
    
    if "loan_application" in tool_context.state:
        tool_context.state["loan_application"]["status"] = "SANCTION_GENERATED"
        tool_context.state["loan_application"]["sanction_reference"] = sanction_ref
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "sanction_letter_generated",
        "sanction_reference": sanction_ref,
        "sanctioned_amount": loan_amount,
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": "Sanction letter generated successfully!",
        "sanction_reference": sanction_ref,
        "sanction_date": sanction_date,
        "validity_until": validity_date,
        "borrower_name": customer["name"],
        "sanctioned_amount": f"₹{loan_amount:,.0f}",
        "interest_rate": f"{interest_rate}% p.a.",
        "tenure": f"{tenure} months",
        "monthly_emi": f"₹{emi_details['emi']:,.0f}",
        "processing_fee": f"₹{processing_fee:,.0f}",
        "disbursement_amount": f"₹{disbursement_amount:,.0f}",
        "disbursement_account": f"{customer['bank_name']} - {customer['account_number'][-4:].rjust(len(customer['account_number']), 'X')}",
        "first_emi_date": first_emi_date,
        "download_link": f"[Download Sanction Letter PDF - {sanction_ref}]"
    }


def get_sanction_letter_pdf(sanction_reference: str, tool_context: ToolContext) -> dict:
    """
    Generates and returns the PDF content of sanction letter.
    
    Args:
        sanction_reference: The sanction letter reference number
        tool_context: The tool context for state management
    
    Returns:
        dict: PDF generation status and formatted content
    """
    sanction_letter = tool_context.state.get("sanction_letter", {})
    
    if not sanction_letter:
        return {
            "status": "error",
            "message": "Sanction letter not found. Please generate it first."
        }
    
    if sanction_letter.get("sanction_reference") != sanction_reference:
        return {
            "status": "error",
            "message": "Invalid sanction reference number."
        }
    
    # Format the sanction letter as text (would be PDF in production)
    borrower = sanction_letter["borrower_details"]
    loan = sanction_letter["loan_details"]
    disbursement = sanction_letter["disbursement_details"]
    
    letter_content = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           TATA CAPITAL LIMITED                                 ║
║                      PERSONAL LOAN SANCTION LETTER                             ║
╠══════════════════════════════════════════════════════════════════════════════╣

Sanction Reference: {sanction_letter['sanction_reference']}
Approval Reference: {sanction_letter['approval_reference']}
Date: {sanction_letter['sanction_date']}
Valid Until: {sanction_letter['validity_until']}

───────────────────────────────────────────────────────────────────────────────
                              BORROWER DETAILS
───────────────────────────────────────────────────────────────────────────────
Name:           {borrower['name']}
Customer ID:    {borrower['customer_id']}
PAN:            {borrower['pan']}
Location:       {borrower['address']}
Contact:        {borrower['phone']}
Email:          {borrower['email']}

───────────────────────────────────────────────────────────────────────────────
                               LOAN DETAILS
───────────────────────────────────────────────────────────────────────────────
Loan Type:              {loan['loan_type']}
Sanctioned Amount:      ₹{loan['sanctioned_amount']:,.0f}
Interest Rate:          {loan['interest_rate']}% per annum (Reducing Balance)
Loan Tenure:            {loan['tenure_months']} months
Monthly EMI:            ₹{loan['emi']:,.0f}
Total Interest:         ₹{loan['total_interest']:,.0f}
Total Repayment:        ₹{loan['total_repayment']:,.0f}
Processing Fee:         ₹{loan['processing_fee']:,.0f}
Net Disbursement:       ₹{loan['disbursement_amount']:,.0f}
First EMI Due Date:     {loan['first_emi_date']}
Loan Purpose:           {loan['purpose']}

───────────────────────────────────────────────────────────────────────────────
                           DISBURSEMENT DETAILS
───────────────────────────────────────────────────────────────────────────────
Bank Name:              {disbursement['bank_name']}
Account Number:         {disbursement['account_number']}
Disbursement Mode:      {disbursement['disbursement_mode']}
Expected Timeline:      {disbursement['expected_disbursement']}

───────────────────────────────────────────────────────────────────────────────
                          TERMS AND CONDITIONS
───────────────────────────────────────────────────────────────────────────────
1. This sanction letter is valid for 30 days from the date of issue.
2. Loan disbursement is subject to completion of all documentation.
3. EMI will be debited from the registered bank account on the due date.
4. Prepayment is allowed after 6 EMIs with 2% foreclosure charges.
5. Late payment charges: 2% per month on overdue EMI amount.
6. All terms are as per the loan agreement to be signed at disbursement.

───────────────────────────────────────────────────────────────────────────────
                            NEXT STEPS
───────────────────────────────────────────────────────────────────────────────
1. Review and accept the sanction letter terms
2. Complete e-Sign of loan agreement
3. Set up auto-debit mandate (e-NACH)
4. Loan amount will be credited to your account

For any queries, contact: 1800-XXX-XXXX (Toll Free)
Email: support@tatacapital.com

╚══════════════════════════════════════════════════════════════════════════════╝
                    This is a system generated document
               © {datetime.now().year} Tata Capital Limited. All rights reserved.
"""
    
    return {
        "status": "success",
        "message": "Sanction letter PDF generated",
        "sanction_reference": sanction_reference,
        "pdf_content": letter_content,
        "file_name": f"Sanction_Letter_{sanction_reference}.pdf"
    }


def send_sanction_letter(
    customer_id: str,
    send_email: bool,
    send_sms: bool,
    tool_context: ToolContext
) -> dict:
    """
    Sends the sanction letter to customer via email and/or SMS.
    
    Args:
        customer_id: The customer's unique ID
        send_email: Whether to send via email
        send_sms: Whether to send SMS notification
        tool_context: The tool context for state management
    
    Returns:
        dict: Delivery status for each channel
    """
    sanction_letter = tool_context.state.get("sanction_letter", {})
    
    if not sanction_letter:
        return {
            "status": "error",
            "message": "Sanction letter not found. Please generate it first."
        }
    
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"status": "error", "message": "Customer not found"}
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    delivery_status = []
    
    if send_email:
        # Simulate email sending
        delivery_status.append({
            "channel": "Email",
            "recipient": customer["email"],
            "status": "Sent",
            "timestamp": current_time
        })
    
    if send_sms:
        # Simulate SMS sending
        delivery_status.append({
            "channel": "SMS",
            "recipient": customer["phone"],
            "status": "Sent",
            "message": f"Your Tata Capital Personal Loan of ₹{sanction_letter['loan_details']['sanctioned_amount']:,.0f} is sanctioned. Ref: {sanction_letter['sanction_reference']}",
            "timestamp": current_time
        })
    
    # Update state
    tool_context.state["sanction_letter_sent"] = True
    tool_context.state["delivery_status"] = delivery_status
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "sanction_letter_sent",
        "channels": [d["channel"] for d in delivery_status],
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": "Sanction letter sent successfully!",
        "sanction_reference": sanction_letter["sanction_reference"],
        "delivery_status": delivery_status
    }


def accept_sanction(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Records customer's acceptance of sanction letter terms.
    This is the final step before disbursement.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Acceptance confirmation and next steps
    """
    sanction_letter = tool_context.state.get("sanction_letter", {})
    
    if not sanction_letter:
        return {
            "status": "error",
            "message": "Sanction letter not found."
        }
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update state
    tool_context.state["sanction_accepted"] = True
    tool_context.state["acceptance_time"] = current_time
    tool_context.state["application_status"] = "SANCTION_ACCEPTED"
    
    if "loan_application" in tool_context.state:
        tool_context.state["loan_application"]["status"] = "SANCTION_ACCEPTED"
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "sanction_accepted",
        "sanction_reference": sanction_letter["sanction_reference"],
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    customer = get_customer_by_id(customer_id)
    
    return {
        "status": "success",
        "message": "🎉 Thank you for accepting the sanction letter!",
        "sanction_reference": sanction_letter["sanction_reference"],
        "acceptance_time": current_time,
        "next_steps": [
            "1. E-Sign the loan agreement (link will be sent via email)",
            "2. Complete e-NACH mandate for EMI auto-debit",
            "3. Loan will be disbursed within 24-48 hours",
            f"4. Amount of ₹{sanction_letter['loan_details']['disbursement_amount']:,.0f} will be credited to your {customer['bank_name']} account"
        ],
        "support_contact": "1800-XXX-XXXX (Toll Free)"
    }


def get_loan_summary(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Provides complete loan journey summary.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Complete loan application summary
    """
    loan_application = tool_context.state.get("loan_application", {})
    sanction_letter = tool_context.state.get("sanction_letter", {})
    customer = get_customer_by_id(customer_id)
    
    if not loan_application:
        return {
            "status": "error",
            "message": "No loan application found"
        }
    
    summary = {
        "status": "success",
        "customer_name": customer["name"] if customer else "Customer",
        "application_id": loan_application.get("application_id", "N/A"),
        "application_date": loan_application.get("application_date", "N/A"),
        "current_status": tool_context.state.get("application_status", "UNKNOWN"),
        "loan_details": {
            "amount": f"₹{loan_application.get('loan_amount', 0):,.0f}",
            "tenure": f"{loan_application.get('tenure_months', 0)} months",
            "purpose": loan_application.get("purpose", "N/A")
        },
        "verification_status": {
            "kyc": "✓ Verified" if tool_context.state.get("kyc_verified") else "⏳ Pending",
            "credit_check": "✓ Completed" if tool_context.state.get("credit_score") else "⏳ Pending",
        },
        "journey_timeline": []
    }
    
    # Build timeline from interaction history
    for interaction in tool_context.state.get("interaction_history", []):
        action = interaction.get("action", "")
        timestamp = interaction.get("timestamp", "")
        
        action_map = {
            "loan_offer_shown": "📋 Loan offer presented",
            "loan_application_initiated": "📝 Application initiated",
            "kyc_verification_complete": "✅ KYC verified",
            "credit_score_fetched": f"📊 Credit score checked ({interaction.get('credit_score', 'N/A')})",
            "loan_approved": "🎉 Loan approved",
            "sanction_letter_generated": "📄 Sanction letter generated",
            "sanction_accepted": "✍️ Sanction accepted",
            "loan_rejected": f"❌ Application declined ({interaction.get('reason', 'N/A')})"
        }
        
        if action in action_map:
            summary["journey_timeline"].append({
                "event": action_map[action],
                "timestamp": timestamp
            })
    
    if sanction_letter:
        summary["sanction_details"] = {
            "reference": sanction_letter.get("sanction_reference", "N/A"),
            "sanctioned_amount": f"₹{sanction_letter['loan_details']['sanctioned_amount']:,.0f}",
            "emi": f"₹{sanction_letter['loan_details']['emi']:,.0f}",
            "first_emi_date": sanction_letter['loan_details']['first_emi_date']
        }
    
    return summary


# Create the Sanction Letter Agent
sanction_letter_agent = Agent(
    name="sanction_letter_agent",
    model="gemini-2.5-flash-lite",
    description="Agent that generates automated PDF sanction letters for approved loans",
    instruction="""
    You are the Sanction Letter Generator Agent for Tata Capital.
    Your role is to create and deliver official sanction letters for approved personal loans.

    <customer_info>
    Customer ID: {customer_id}
    Name: {customer_name}
    </customer_info>

    <loan_application>
    {loan_application}
    </loan_application>

    <sanction_letter>
    {sanction_letter}
    </sanction_letter>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    **Your Responsibilities:**

    1. **Generate Sanction Letter**
       - Use generate_sanction_letter after loan approval
       - Include all loan terms, EMI details, and disbursement info
       - Ensure all calculations are accurate

    2. **Provide PDF Copy**
       - Use get_sanction_letter_pdf to create downloadable document
       - Format professionally with all required details
       - Include terms and conditions

    3. **Deliver to Customer**
       - Use send_sanction_letter to email and SMS
       - Confirm delivery status
       - Provide download link

    4. **Process Acceptance**
       - Use accept_sanction when customer agrees to terms
       - Explain next steps clearly
       - Provide support contact information

    5. **Summarize Journey**
       - Use get_loan_summary for complete overview
       - Show timeline of all steps
       - Celebrate successful completion!

    **Sanction Letter Contents:**
    - Customer details
    - Loan amount and tenure
    - Interest rate and EMI
    - Processing fee and disbursement amount
    - First EMI date
    - Terms and conditions
    - Disbursement account details

    **Communication Style:**
    - Be congratulatory and positive
    - Explain all terms clearly
    - Make next steps crystal clear
    - Provide support contacts

    **Important:**
    - Only generate after loan approval
    - Verify all details before generating
    - Ensure customer understands terms
    - End conversation on a positive note
    """,
    tools=[
        generate_sanction_letter,
        get_sanction_letter_pdf,
        send_sanction_letter,
        accept_sanction,
        get_loan_summary
    ],
)
