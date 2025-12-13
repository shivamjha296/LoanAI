"""
Verification Agent for BFSI Loan Chatbot
Confirms KYC details (phone, address, identity) from dummy CRM server
"""

from datetime import datetime
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from mock_data.crm_data import get_kyc_data, verify_phone, verify_address, get_kyc_status


def fetch_kyc_details(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Fetches KYC details for a customer from CRM system.
    ⚡ PARALLEL PROCESSING: Uses pre-fetched data if available
    
    Args:
        customer_id: The customer's unique ID (e.g., "CUST001")
        tool_context: The tool context for state management
    
    Returns:
        dict: Customer's KYC information including verification status
    """
    # ⚡ Check if data was pre-fetched in parallel
    prefetched_kyc = tool_context.state.get("_prefetched_kyc")
    
    if prefetched_kyc and prefetched_kyc.get("status") == "success":
        kyc_data = prefetched_kyc
        # Mark as instant retrieval
        retrieval_time = "Instant (Pre-fetched)"
    else:
        # Fetch normally if not pre-fetched
        kyc_data = get_kyc_data(customer_id)
        retrieval_time = "Standard"
    
    if not kyc_data:
        return {
            "status": "error",
            "message": "Customer not found in CRM system"
        }
    
    # Store KYC data in state
    tool_context.state["kyc_data"] = kyc_data
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "kyc_details_fetched",
        "customer_id": customer_id,
        "kyc_status": kyc_data["kyc_status"],
        "retrieval_method": retrieval_time,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    tool_context.state["interaction_history"] = current_history
    
    # Format address for display
    address = kyc_data["address"]
    formatted_address = f"{address['line1']}, {address['line2']}, {address['city']}, {address['state']} - {address['pincode']}"
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "name": kyc_data["name"],
        "phone": kyc_data["phone"],
        "phone_verified": kyc_data["phone_verified"],
        "address": formatted_address,
        "address_verified": kyc_data["address_verified"],
        "pan_number": kyc_data["pan_number"],
        "pan_verified": kyc_data["pan_verified"],
        "aadhar_number": kyc_data["aadhar_number"],
        "aadhar_verified": kyc_data["aadhar_verified"],
        "email_verified": kyc_data["email_verified"],
        "kyc_status": kyc_data["kyc_status"],
        "kyc_completion_date": kyc_data.get("kyc_completion_date", "Not completed"),
        "_retrieval_time": retrieval_time
    }


def verify_customer_phone(customer_id: str, phone: str, tool_context: ToolContext) -> dict:
    """
    Verifies if the provided phone number matches CRM records.
    
    Args:
        customer_id: The customer's unique ID
        phone: Phone number to verify (10 digits)
        tool_context: The tool context for state management
    
    Returns:
        dict: Verification result
    """
    result = verify_phone(customer_id, phone)
    
    # Update verification status in state
    if result.get("verified"):
        tool_context.state["phone_verified"] = True
        
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "phone_verified",
            "customer_id": customer_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
    
    return result


def verify_customer_address(customer_id: str, pincode: str, tool_context: ToolContext) -> dict:
    """
    Verifies if the provided pincode matches CRM address records.
    
    Args:
        customer_id: The customer's unique ID
        pincode: 6-digit pincode to verify
        tool_context: The tool context for state management
    
    Returns:
        dict: Verification result
    """
    result = verify_address(customer_id, pincode)
    
    # Update verification status in state
    if result.get("verified"):
        tool_context.state["address_verified"] = True
        
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "address_verified",
            "customer_id": customer_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
    
    return result


def get_verification_status(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Gets overall KYC verification status for a customer.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Complete verification status summary
    """
    return get_kyc_status(customer_id)


def complete_kyc_verification(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Marks KYC verification as complete after all checks pass.
    This allows the application to proceed to underwriting.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: KYC completion status and next steps
    """
    kyc_data = get_kyc_data(customer_id)
    
    if not kyc_data:
        return {
            "status": "error",
            "message": "Customer not found in CRM system"
        }
    
    # Check if all required verifications are complete
    required_checks = [
        ("Phone", kyc_data["phone_verified"]),
        ("Address", kyc_data["address_verified"]),
        ("PAN", kyc_data["pan_verified"]),
        ("Aadhar", kyc_data["aadhar_verified"])
    ]
    
    failed_checks = [check[0] for check in required_checks if not check[1]]
    
    if failed_checks:
        return {
            "status": "error",
            "message": f"KYC verification incomplete. Failed checks: {', '.join(failed_checks)}",
            "failed_verifications": failed_checks,
            "can_proceed": False
        }
    
    # Update state
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tool_context.state["kyc_verified"] = True
    tool_context.state["kyc_completion_time"] = current_time
    tool_context.state["application_status"] = "KYC_VERIFIED"
    
    # Update loan application if exists
    if "loan_application" in tool_context.state:
        tool_context.state["loan_application"]["status"] = "KYC_VERIFIED"
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "kyc_verification_complete",
        "customer_id": customer_id,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": "KYC verification completed successfully!",
        "customer_id": customer_id,
        "customer_name": kyc_data["name"],
        "verification_summary": {
            "phone": "✓ Verified",
            "address": "✓ Verified",
            "pan": "✓ Verified",
            "aadhar": "✓ Verified"
        },
        "next_step": "Application will now proceed to credit evaluation and underwriting"
    }


def request_document_update(
    customer_id: str,
    document_type: str,
    reason: str,
    tool_context: ToolContext
) -> dict:
    """
    Requests customer to update a specific document for verification.
    
    Args:
        customer_id: The customer's unique ID
        document_type: Type of document (phone, address, pan, aadhar)
        reason: Reason for update request
        tool_context: The tool context for state management
    
    Returns:
        dict: Document update request details
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    update_request = {
        "request_id": f"DOC{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "customer_id": customer_id,
        "document_type": document_type,
        "reason": reason,
        "requested_at": current_time,
        "status": "PENDING"
    }
    
    # Store request in state
    pending_updates = tool_context.state.get("pending_document_updates", [])
    pending_updates.append(update_request)
    tool_context.state["pending_document_updates"] = pending_updates
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "document_update_requested",
        "document_type": document_type,
        "reason": reason,
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": f"Document update request created for {document_type}",
        "request_id": update_request["request_id"],
        "document_type": document_type,
        "reason": reason,
        "instructions": get_update_instructions(document_type)
    }


def get_update_instructions(document_type: str) -> str:
    """Get instructions for updating a specific document type."""
    instructions = {
        "phone": "Please provide your current mobile number registered with your bank.",
        "address": "Please provide your current address proof (Utility bill, Bank statement, or Rent agreement).",
        "pan": "Please provide a clear photo of your PAN card.",
        "aadhar": "Please provide a clear photo of your Aadhar card (front and back)."
    }
    return instructions.get(document_type, "Please provide the requested document.")


# Create the Verification Agent - Mr. Soham Patel
verification_agent = Agent(
    name="verification_agent",
    model=LiteLlm(model="mistral/mistral-large-2411"),
    description="Mr. Soham Patel - KYC Verification Officer who confirms identity and document details from CRM",
    instruction="""
    You are Mr. Soham Patel, a friendly and efficient KYC Verification Officer at Tata Capital.
    You handle identity verification with professionalism and care, making the process smooth and reassuring for customers.

    <customer_info>
    Customer ID: {customer_id}
    Name: {customer_name}
    </customer_info>

    <kyc_data>
    {kyc_data}
    </kyc_data>

    <loan_application>
    {loan_application}
    </loan_application>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    **Your Role - Working Invisibly as Priya Sharma:**

    You are a BACKEND AGENT. The customer only sees "Priya Sharma".
    NEVER introduce yourself. Continue seamlessly as Priya.
    Example: "Let me quickly verify your details..."

    1. **Fetch and Review KYC Details (Quick & Efficient)**
       - Use fetch_kyc_details to get customer's information from our CRM system
       - Check existing verification status
       - Reassure: "Let me quickly pull up your details from our system..."

    2. **Verify Customer Identity (Professional & Friendly)**
       - Confirm phone number matches our records
       - Verify address details (at minimum the pincode)
       - Check PAN and Aadhar verification status
       - Explain each step: "I just need to confirm a few details with you for security purposes..."

    3. **Handle Incomplete KYC (Helpful & Clear)**
       - If any verification is pending, explain what's needed kindly
       - Use request_document_update for missing/incorrect documents
       - Provide crystal clear instructions
       - Be encouraging: "Don't worry, this is a simple step that helps us keep your account secure!"

    4. **Complete Verification (Celebrate & Handoff)**
       - Once all checks pass, use complete_kyc_verification
       - Celebrate: "Perfect! Your details are verified!"
       - AUTOMATICALLY continue: "Now let me check your credit profile..."
       - DO NOT mention other teams
       - After completion, IMMEDIATELY return for automatic continuation

    **Verification Process You Follow:**
    1. First, fetch KYC details from CRM system
    2. If KYC status is already "COMPLETED", express delight and proceed to complete_kyc_verification
    3. If KYC status is "PARTIAL", identify which verifications are missing
    4. Request necessary documents/updates with clear instructions
    5. Once all verifications pass, mark as complete and celebrate!

    **Your Communication Style as Priya:**
    - NEVER introduce yourself (customer knows Priya)
    - Professional yet friendly
    - Make process feel simple and quick
    - Explain why verification matters
    - Use reassuring language
    - After completion, AUTOMATICALLY transfer to next stage
    - DO NOT mention other teams

    **Important Guidelines:**
    - Never skip verification steps
    - Confirm customer identity
    - Be clear about needed documents
    - Reassure data security
    - After completion, IMMEDIATELY return for automatic continuation

    Remember: You work INVISIBLY as Priya. Customer sees only Priya. After completing,
    IMMEDIATELY return control for automatic workflow continuation.
    """,
    tools=[
        fetch_kyc_details,
        verify_customer_phone,
        verify_customer_address,
        get_verification_status,
        complete_kyc_verification,
        request_document_update
    ],
)
