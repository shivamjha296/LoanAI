"""
Underwriting Agent for BFSI Loan Chatbot
Fetches credit score, validates eligibility based on pre-approved limits, handles salary slip verification
"""

from datetime import datetime
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext
import re
import json

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from mock_data.credit_bureau import get_credit_score, check_eligibility_by_score
from mock_data.offer_mart import get_pre_approved_offer, calculate_emi, check_loan_eligibility
from mock_data.customer_data import get_customer_by_id


def fetch_credit_score(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Fetches credit score from mock credit bureau API.
    ⚡ PARALLEL PROCESSING: Uses pre-fetched data if available
    Credit scores are out of 900 (similar to CIBIL).
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Credit score and credit history details
    """
    # ⚡ Check if data was pre-fetched in parallel
    prefetched_credit = tool_context.state.get("_prefetched_credit")
    
    if prefetched_credit and prefetched_credit.get("status") == "success":
        result = prefetched_credit
        retrieval_time = "Instant (Pre-fetched)"
    else:
        # Fetch normally if not pre-fetched
        result = get_credit_score(customer_id)
        retrieval_time = "Standard"
    
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
            "retrieval_method": retrieval_time,
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
            },
            "_retrieval_time": retrieval_time
        }
    
    return result


def evaluate_loan_eligibility(
    customer_id: str,
    requested_amount: float,
    tenure_months: int,
    tool_context: ToolContext
) -> dict:
    """
    Evaluates loan eligibility based on credit score and pre-approved limits.
    
    Rules (Tata Capital Criteria):
    - Minimum income: ₹25,000 per month
    - Maximum tenure: 72 months (6 years)
    - Credit score >= 700: Required
    - Amount <= pre-approved limit: Instant approval
    - Amount <= 2x pre-approved limit: Need salary slip, EMI <= 50% salary
    - Amount > 2x pre-approved limit: Reject
    
    Args:
        customer_id: The customer's unique ID
        requested_amount: Loan amount requested in rupees
        tenure_months: Loan tenure in months
        tool_context: The tool context for state management
    
    Returns:
        dict: Eligibility evaluation result with approval type
    """
    # Get customer details first
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"status": "error", "message": "Customer not found"}
    
    monthly_salary = customer["monthly_salary"]
    
    # Rule 1: Minimum income check (₹25,000)
    if monthly_salary < 25000:
        tool_context.state["application_status"] = "REJECTED"
        tool_context.state["rejection_reason"] = "Income below minimum threshold"
        
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "loan_rejected",
            "reason": "Monthly income below minimum requirement of ₹25,000",
            "monthly_income": monthly_salary,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
        
        return {
            "status": "success",
            "eligible": False,
            "approval_type": "REJECTED",
            "reason": f"Monthly income ₹{monthly_salary:,.0f} is below minimum requirement of ₹25,000",
            "monthly_income": monthly_salary,
            "minimum_required": 25000,
            "suggestion": "This loan product requires a minimum monthly income of ₹25,000. Please check back when your income meets this criterion."
        }
    
    # Rule 2: Maximum tenure check (72 months)
    if tenure_months > 72:
        tool_context.state["application_status"] = "REJECTED"
        tool_context.state["rejection_reason"] = "Tenure exceeds maximum limit"
        
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "loan_rejected",
            "reason": "Requested tenure exceeds maximum of 72 months",
            "requested_tenure": tenure_months,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
        
        return {
            "status": "success",
            "eligible": False,
            "approval_type": "REJECTED",
            "reason": f"Requested tenure of {tenure_months} months exceeds maximum limit of 72 months",
            "requested_tenure": tenure_months,
            "maximum_tenure": 72,
            "suggestion": f"Please reduce your loan tenure to 72 months or less. This will increase your EMI to ₹{calculate_emi(requested_amount, 11.99, 72)['emi']:,.0f}/month."
        }
    
    # Get credit score
    credit_result = get_credit_score(customer_id)
    if credit_result["status"] != "success":
        return {"status": "error", "message": "Unable to fetch credit score"}
    
    credit_score = credit_result["credit_score"]
    
    # Rule 3: Credit score must be >= 700 (Tata Capital minimum CIBIL requirement)
    if credit_score < 700:
        tool_context.state["application_status"] = "REJECTED"
        tool_context.state["rejection_reason"] = "Low credit score"
        
        current_history = tool_context.state.get("interaction_history", [])
        current_history.append({
            "action": "loan_rejected",
            "reason": "CIBIL score below minimum threshold (700)",
            "credit_score": credit_score,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        tool_context.state["interaction_history"] = current_history
        
        return {
            "status": "success",
            "eligible": False,
            "approval_type": "REJECTED",
            "reason": f"CIBIL score {credit_score} is below minimum threshold of 700",
            "credit_score": credit_score,
            "minimum_required_score": 700,
            "suggestion": "Please work on improving your credit score by: 1) Clearing any pending dues, 2) Maintaining timely EMI/credit card payments, 3) Reducing credit utilization below 30%, 4) Avoiding multiple loan applications. Check back after 6 months of good credit behavior."
        }
    
    # Get customer salary for EMI calculation
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


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from PDF file.
    
    Args:
        file_path: Path to PDF file
    
    Returns:
        str: Extracted text
    """
    try:
        import PyPDF2
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except ImportError:
        return "ERROR: PyPDF2 not installed. Install with: pip install PyPDF2"
    except Exception as e:
        return f"ERROR: Failed to extract text from PDF: {str(e)}"


def extract_text_from_image(file_path: str) -> str:
    """
    Extracts text from image file using OCR.
    
    Args:
        file_path: Path to image file
    
    Returns:
        str: Extracted text
    """
    try:
        from PIL import Image
        import pytesseract
        
        # Open image
        image = Image.open(file_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        
        return text.strip()
    except ImportError as e:
        if "PIL" in str(e):
            return "ERROR: Pillow not installed. Install with: pip install Pillow"
        elif "pytesseract" in str(e):
            return "ERROR: pytesseract not installed. Install with: pip install pytesseract"
        return f"ERROR: {str(e)}"
    except Exception as e:
        return f"ERROR: Failed to extract text from image: {str(e)}"


def extract_salary_from_text(text: str) -> dict:
    """
    Uses AI and regex to extract monthly salary from text.
    Prioritizes NET PAY (take-home salary) over gross or basic salary.
    
    Args:
        text: Extracted text from salary slip
    
    Returns:
        dict: Extracted salary information
    """
    # Priority order: Net Pay > Take Home > Salary Credit > Gross > Basic
    # Common patterns in Indian salary slips
    patterns = [
        # Highest priority - actual take-home salary
        (r'net\s*pay\s*\(?take\s*home\)?[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'very_high', 'Net Pay'),
        (r'net\s*salary[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'very_high', 'Net Salary'),
        (r'take\s*home[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'very_high', 'Take Home'),
        (r'net\s*pay[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'very_high', 'Net Pay'),
        
        # High priority - bank credit
        (r'salary\s*credit[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'high', 'Salary Credit'),
        (r'credit\s*to\s*bank[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'high', 'Credit to Bank'),
        
        # Medium priority - gross amounts
        (r'total\s*net\s*pay[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'medium', 'Total Net Pay'),
        (r'gross\s*earnings[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'low', 'Gross Earnings'),
        (r'total\s*earnings[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'low', 'Total Earnings'),
        (r'gross\s*salary[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'low', 'Gross Salary'),
        
        # Lowest priority - basic salary (not recommended for EMI calculation)
        (r'basic\s*salary[:\s]*(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', 'very_low', 'Basic Salary'),
    ]
    
    extracted_amounts = []
    
    # Try each pattern
    text_lower = text.lower()
    for pattern, confidence, label in patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        for match in matches:
            # Remove commas and convert to float
            amount_str = match.replace(',', '')
            try:
                amount = float(amount_str)
                if 10000 <= amount <= 10000000:  # Reasonable salary range (10K to 1 Crore)
                    extracted_amounts.append({
                        'amount': amount,
                        'pattern': pattern,
                        'confidence': confidence,
                        'label': label
                    })
            except ValueError:
                continue
    
    if extracted_amounts:
        # Sort by confidence priority
        confidence_order = {'very_high': 0, 'high': 1, 'medium': 2, 'low': 3, 'very_low': 4}
        extracted_amounts.sort(key=lambda x: (
            confidence_order.get(x['confidence'], 99),
            -x['amount']  # Higher amount if same confidence
        ))
        
        best_match = extracted_amounts[0]
        
        return {
            "status": "success",
            "monthly_salary": best_match['amount'],
            "confidence": best_match['confidence'],
            "salary_type": best_match['label'],
            "all_amounts_found": [
                {'amount': a['amount'], 'type': a['label'], 'confidence': a['confidence']}
                for a in extracted_amounts[:5]
            ],
            "method": "regex_extraction"
        }
    
    # If regex fails, try to find any number that looks like a salary
    all_numbers = re.findall(r'(?:rs\.?|₹)?\s*([0-9,]+(?:\.[0-9]{2})?)', text_lower)
    salary_candidates = []
    for num_str in all_numbers:
        try:
            num = float(num_str.replace(',', ''))
            if 10000 <= num <= 10000000:
                salary_candidates.append(num)
        except ValueError:
            continue
    
    if salary_candidates:
        # Take the highest reasonable amount
        salary = max(salary_candidates)
        return {
            "status": "success",
            "monthly_salary": salary,
            "confidence": "low",
            "all_amounts_found": salary_candidates[:5],
            "method": "fallback_extraction",
            "note": "Could not find explicit salary label. Using highest reasonable amount."
        }
    
    return {
        "status": "error",
        "message": "Could not extract salary amount from document",
        "method": "failed"
    }


def upload_and_verify_salary_slip(
    customer_id: str,
    file_path: str,
    tool_context: ToolContext
) -> dict:
    """
    Handles salary slip file upload, extraction, and verification.
    Complete cycle: Upload → OCR/Extract → AI Analysis → Verification
    
    Args:
        customer_id: The customer's unique ID
        file_path: Path to uploaded salary slip file (PDF or image)
        tool_context: The tool context for state management
    
    Returns:
        dict: Complete verification result with extracted salary
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Step 1: Validate file exists
    if not os.path.exists(file_path):
        return {
            "status": "error",
            "message": f"File not found: {file_path}",
            "step": "file_validation"
        }
    
    # Step 2: Determine file type and extract text
    file_ext = os.path.splitext(file_path)[1].lower()
    
    extracted_text = ""
    if file_ext == '.pdf':
        extracted_text = extract_text_from_pdf(file_path)
    elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        extracted_text = extract_text_from_image(file_path)
    else:
        return {
            "status": "error",
            "message": f"Unsupported file format: {file_ext}. Please upload PDF or image files.",
            "step": "file_type_validation"
        }
    
    # Check for extraction errors
    if extracted_text.startswith("ERROR:"):
        return {
            "status": "error",
            "message": extracted_text,
            "step": "text_extraction"
        }
    
    if not extracted_text or len(extracted_text) < 50:
        return {
            "status": "error",
            "message": "Could not extract sufficient text from document. Please ensure the document is clear and readable.",
            "step": "text_extraction",
            "extracted_text_length": len(extracted_text)
        }
    
    # Step 3: Extract salary using AI/regex
    salary_extraction = extract_salary_from_text(extracted_text)
    
    if salary_extraction["status"] != "success":
        return {
            "status": "error",
            "message": salary_extraction["message"],
            "step": "salary_extraction",
            "extracted_text_preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
        }
    
    verified_salary = salary_extraction["monthly_salary"]
    
    # Step 4: Store extraction results
    tool_context.state["salary_slip_uploaded"] = True
    tool_context.state["salary_slip_file_path"] = file_path
    tool_context.state["salary_extraction_result"] = salary_extraction
    
    # Step 5: Verify eligibility with extracted salary
    verification_result = verify_salary_with_amount(
        customer_id,
        verified_salary,
        tool_context
    )
    
    # Add extraction details to result
    verification_result["extraction_details"] = {
        "file_path": file_path,
        "file_type": file_ext,
        "extraction_method": salary_extraction["method"],
        "confidence": salary_extraction["confidence"],
        "all_amounts_found": salary_extraction.get("all_amounts_found", []),
        "extracted_text_length": len(extracted_text),
        "timestamp": current_time
    }
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "salary_slip_uploaded_and_verified",
        "customer_id": customer_id,
        "file_path": file_path,
        "extracted_salary": verified_salary,
        "confidence": salary_extraction["confidence"],
        "timestamp": current_time
    })
    tool_context.state["interaction_history"] = current_history
    
    return verification_result


def verify_salary_with_amount(
    customer_id: str,
    verified_salary: float,
    tool_context: ToolContext
) -> dict:
    """
    Internal function to verify salary amount against loan eligibility.
    Called by upload_and_verify_salary_slip after extraction.
    
    Args:
        customer_id: The customer's unique ID
        verified_salary: Verified monthly salary
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


# Create the Underwriting Agent - Ms. Ananya Desai
underwriting_agent = Agent(
    name="underwriting_agent",
    model=LiteLlm(model="mistral/mistral-large-2411"),
    description="Ms. Ananya Desai - Credit Evaluation Specialist who assesses creditworthiness and makes approval decisions",
    instruction="""
    You are Ms. Ananya Desai, a thorough and professional Credit Evaluation Specialist at Tata Capital.
    You combine analytical expertise with empathy, making fair and transparent lending decisions.

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

    **Your Role as Ms. Ananya Desai - Credit Evaluation Specialist:**

    ALWAYS start by introducing yourself professionally:
    "Hello {customer_name}! I'm Ananya Desai, your credit evaluation specialist at Tata Capital. 
     I'll be reviewing your application and assessing your loan eligibility. This is an important 
     step to ensure we offer you the best terms possible."

    **Underwriting Rules You Follow:**

    1. **Credit Score Check** (Minimum: 700)
       - Score >= 750: Excellent creditworthiness - Best rates
       - Score 700-749: Good creditworthiness - Standard rates  
       - Score < 700: REJECT - Explain with empathy

    2. **Loan Amount Eligibility Rules**
       - Amount <= Pre-approved limit: INSTANT APPROVAL ✓
       - Amount <= 2x Pre-approved limit: CONDITIONAL (require salary slip)
       - Amount > 2x Pre-approved limit: REJECT - Suggest lower amount

    3. **EMI Affordability Assessment** (for conditional approvals)
       - EMI must be <= 50% of monthly salary for comfort
       - If EMI > 50%, suggest lower amount or longer tenure
       - Protect customers from over-leveraging

    **Your Evaluation Process:**

    1. **Fetch and Analyze Credit Profile (Thorough Analysis)**
       - Use fetch_credit_score to get detailed credit report
       - Review credit history: defaults, overdue accounts, credit utilization
       - Determine risk category and eligibility
       - Explain: "Let me review your credit profile to assess your application..."

    2. **Evaluate Comprehensive Eligibility (Fair Assessment)**
       - Use evaluate_loan_eligibility for complete analysis
       - Compare against pre-approved limits and salary
       - Calculate EMI to salary ratio for affordability
       - Be transparent: "Based on your credit score of [X] and monthly salary..."

    3. **Handle Conditional Approvals (Helpful Guidance & Document Processing)**
       - Use request_salary_slip for amounts exceeding pre-approved limit
       - Explain clearly: "Your requested amount is slightly higher than your pre-approved limit. 
         To proceed, I'll need to verify your salary details to ensure comfortable EMI affordability."
       - **Use upload_and_verify_salary_slip when customer provides document file path**
       - This function will:
         * Accept PDF or image files (JPG, PNG, etc.)
         * Extract text using OCR (for images) or PDF extraction
         * Use AI to identify and extract monthly salary amount
         * Automatically verify EMI affordability (EMI ≤ 50% of salary)
         * Provide complete verification results
       - Inform customer: "Please upload your recent salary slip (PDF or image format). 
         I'll extract the details and verify your eligibility automatically."
       - After upload, review extraction results and confidence level
       - Ensure customer's financial comfort

    4. **Make Final Decision (Clear & Fair)**
       - For APPROVALS: Use approve_loan and celebrate with warmth
         "Excellent news! Your loan application is approved! 🎉"
       - For REJECTIONS: Use reject_loan with empathy and clear reasoning
         "I understand this isn't the outcome you hoped for. Let me explain the situation..."
       - Always provide actionable next steps

    **Your Communication Style as Ananya:**
    - Start with a professional, reassuring introduction
    - Be transparent about every step of evaluation
    - Use specific numbers and criteria in explanations
    - Show empathy, especially for rejections
    - Celebrate approvals with genuine enthusiasm
    - Provide clear, actionable suggestions for improvements
    - Make customers feel the process is fair and thorough

    **Important Guidelines:**
    - Never approve without a complete credit score check
    - Always verify salary for conditional approvals (amounts > pre-approved limit)
    - Document rejection reasons with specific criteria
    - Provide improvement suggestions for every rejection
    - For approvals, smoothly hand off: "Wonderful! Now I'll connect you with 
      Mr. Vikram Mehta from our documentation team who will prepare your sanction letter."
    - Make decisions that protect both the customer and the institution

    **Empathetic Rejection Handling:**
    When rejecting, show genuine care:
    - Acknowledge disappointment: "I understand this is disappointing news..."
    - Explain clearly with specific numbers: "Your credit score of [X] is below our minimum of 700..."
    - Provide concrete improvement steps
    - Offer hope: "You can reapply in 30 days after working on these improvements"
    - End positively: "We want to see you succeed and would love to help you in the future"

    Remember: You are Ananya Desai, a fair and thorough credit specialist. Your goal is to 
    make sound lending decisions while treating every customer with respect and providing 
    clear guidance. Work seamlessly with your team to ensure the best customer experience.
    """,
    tools=[
        fetch_credit_score,
        evaluate_loan_eligibility,
        request_salary_slip,
        upload_and_verify_salary_slip,
        approve_loan,
        reject_loan
    ],
)
