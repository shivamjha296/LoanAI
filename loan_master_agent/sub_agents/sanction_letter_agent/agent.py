"""
Sanction Letter Generator Agent for BFSI Loan Chatbot
Generates automated PDF sanction letters for approved loans
"""

from datetime import datetime, timedelta
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.tool_context import ToolContext
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from mock_data.customer_data import get_customer_by_id
from mock_data.offer_mart import calculate_emi
from mock_data.cross_sell_engine import recommend_cross_sell_products, format_cross_sell_message, get_cross_sell_summary


def generate_sanction_letter_pdf(customer_id: str, tool_context: ToolContext) -> dict:
    """
    Generates a PDF sanction letter and saves it to the device.
    Uses fallback methods if WeasyPrint has font issues on Windows.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: PDF file path and generation status
    """
    try:
        # Get sanction letter data
        sanction_letter = tool_context.state.get("sanction_letter", {})
        if not sanction_letter:
            return {
                "status": "error",
                "message": "No sanction letter data found. Please generate sanction letter first."
            }
        
        # Read HTML template
        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "sanction_letter_template.html"
        )
        
        if not os.path.exists(template_path):
            return {
                "status": "error",
                "message": f"Template file not found: {template_path}"
            }
        
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
        
        # Prepare template data
        borrower = sanction_letter["borrower_details"]
        loan = sanction_letter["loan_details"]
        disbursement = sanction_letter["disbursement_details"]
        
        # Replace template placeholders
        html_content = html_template
        replacements = {
            "{{sanction_reference}}": sanction_letter["sanction_reference"],
            "{{approval_reference}}": sanction_letter["approval_reference"],
            "{{sanction_date}}": sanction_letter["sanction_date"],
            "{{validity_until}}": sanction_letter["validity_until"],
            "{{borrower_name}}": borrower["name"],
            "{{customer_id}}": borrower["customer_id"],
            "{{borrower_pan}}": borrower["pan"],
            "{{borrower_phone}}": borrower["phone"],
            "{{borrower_email}}": borrower["email"],
            "{{borrower_address}}": borrower["address"],
            "{{loan_type}}": loan["loan_type"],
            "{{sanctioned_amount}}": f"{loan['sanctioned_amount']:,.0f}",
            "{{interest_rate}}": str(loan["interest_rate"]),
            "{{tenure_months}}": str(loan["tenure_months"]),
            "{{tenure_years}}": f"{loan['tenure_months'] / 12:.1f}",
            "{{processing_fee}}": f"{loan['processing_fee']:,.0f}",
            "{{processing_fee_percent}}": str(tool_context.state.get("current_offer", {}).get("processing_fee_percent", 1.5)),
            "{{disbursement_amount}}": f"{loan['disbursement_amount']:,.0f}",
            "{{purpose}}": loan["purpose"],
            "{{monthly_emi}}": f"{loan['emi']:,.0f}",
            "{{first_emi_date}}": loan["first_emi_date"],
            "{{total_interest}}": f"{loan['total_interest']:,.0f}",
            "{{total_repayment}}": f"{loan['total_repayment']:,.0f}",
            "{{bank_name}}": disbursement["bank_name"],
            "{{account_number}}": disbursement["account_number"],
            "{{disbursement_mode}}": disbursement["disbursement_mode"],
            "{{expected_disbursement}}": disbursement["expected_disbursement"]
        }
        
        for placeholder, value in replacements.items():
            html_content = html_content.replace(placeholder, value)
        
        # Create sanction_letters directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "sanction_letters")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate PDF filename
        pdf_filename = f"Sanction_Letter_{customer_id}_{sanction_letter['sanction_reference']}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        # Try multiple PDF generation methods with error handling
        pdf_generated = False
        error_messages = []
        
        # Method 1: Try WeasyPrint (best quality but has font issues on Windows)
        try:
            from weasyprint import HTML
            import warnings
            
            # Suppress fontconfig warnings on Windows
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                HTML(string=html_content).write_pdf(pdf_path)
            
            pdf_generated = True
        except Exception as e:
            error_messages.append(f"WeasyPrint failed: {str(e)}")
            
            # Method 2: Fallback to xhtml2pdf (ReportLab-based)
            try:
                from xhtml2pdf import pisa
                
                with open(pdf_path, "wb") as pdf_file:
                    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
                
                if not pisa_status.err:
                    pdf_generated = True
                else:
                    error_messages.append("xhtml2pdf failed with errors")
            except ImportError:
                error_messages.append("xhtml2pdf not installed")
            except Exception as e:
                error_messages.append(f"xhtml2pdf failed: {str(e)}")
        
        if not pdf_generated:
            # Method 3: Last resort - save as HTML with PDF extension (can be printed to PDF)
            try:
                with open(pdf_path.replace('.pdf', '.html'), 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Store HTML path as well
                tool_context.state["sanction_letter_html_path"] = pdf_path.replace('.pdf', '.html')
                
                return {
                    "status": "partial",
                    "message": "PDF generation libraries had issues. HTML version saved. Please print to PDF from browser or install: pip install xhtml2pdf",
                    "html_path": pdf_path.replace('.pdf', '.html'),
                    "errors": error_messages,
                    "suggestion": "Open the HTML file in browser and use 'Print to PDF' feature"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"All PDF generation methods failed: {'; '.join(error_messages)}. Final error: {str(e)}"
                }
        
        # Store PDF path in state
        tool_context.state["sanction_letter"]["pdf_file_path"] = pdf_path
        
        return {
            "status": "success",
            "message": "Sanction letter PDF generated successfully!",
            "pdf_path": pdf_path,
            "pdf_filename": pdf_filename,
            "file_size": f"{os.path.getsize(pdf_path) / 1024:.2f} KB"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating PDF: {str(e)}"
        }


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
    processing_fee_percent = 3.5  # Tata Capital standard processing fee
    loan_purpose = loan_application.get("purpose", "Personal Use")
    
    # Determine loan variant based on purpose
    loan_variant = "Personal Loan"
    variant_features = []
    
    purpose_lower = loan_purpose.lower()
    if "travel" in purpose_lower or "vacation" in purpose_lower or "tour" in purpose_lower:
        loan_variant = "Travel Loan"
        variant_features = [
            "Quick approval within 24 hours",
            "No end-use verification required",
            "Covers international and domestic travel",
            "Flexible repayment options"
        ]
    elif "medical" in purpose_lower or "health" in purpose_lower or "surgery" in purpose_lower or "hospital" in purpose_lower:
        loan_variant = "Medical Emergency Loan"
        variant_features = [
            "Instant approval for emergencies",
            "Moratorium period available during recovery",
            "Covers all medical procedures",
            "Flexible EMI during treatment period"
        ]
    elif "wedding" in purpose_lower or "marriage" in purpose_lower or "shaadi" in purpose_lower:
        loan_variant = "Wedding/Marriage Loan"
        variant_features = [
            "Higher loan amounts available",
            "Pre-wedding disbursement option",
            "Covers all wedding expenses",
            "Extended tenure up to 72 months"
        ]
    elif "renovation" in purpose_lower or "home" in purpose_lower or "interior" in purpose_lower or "construction" in purpose_lower:
        loan_variant = "Home Renovation Loan"
        variant_features = [
            "Staged disbursement as per project progress",
            "No property mortgage required",
            "Covers complete home improvement",
            "Lower processing fees available"
        ]
    elif "education" in purpose_lower or "study" in purpose_lower or "course" in purpose_lower:
        loan_variant = "Education Loan"
        variant_features = [
            "Moratorium until course completion",
            "Covers tuition and living expenses",
            "Special rates for premier institutions"
        ]
    elif "debt" in purpose_lower or "consolidation" in purpose_lower or "credit card" in purpose_lower:
        loan_variant = "Debt Consolidation Loan"
        variant_features = [
            "Single EMI instead of multiple payments",
            "Potential interest rate savings",
            "Simplified debt management"
        ]
    
    emi_details = calculate_emi(loan_amount, interest_rate, tenure)
    processing_fee = loan_amount * (processing_fee_percent / 100)
    gst_on_processing = processing_fee * 0.18  # 18% GST
    total_processing_fee = processing_fee + gst_on_processing
    disbursement_amount = loan_amount - total_processing_fee
    
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
            "loan_type": loan_variant,
            "loan_variant_features": variant_features,
            "sanctioned_amount": loan_amount,
            "interest_rate": interest_rate,
            "tenure_months": tenure,
            "emi": emi_details["emi"],
            "total_interest": emi_details["total_interest"],
            "total_repayment": emi_details["total_payment"],
            "processing_fee": processing_fee,
            "gst_on_processing_fee": gst_on_processing,
            "total_processing_fee": total_processing_fee,
            "processing_fee_percent": processing_fee_percent,
            "disbursement_amount": disbursement_amount,
            "first_emi_date": first_emi_date,
            "purpose": loan_purpose,
            "foreclosure_charges_12m": "6.5% of outstanding principal",
            "foreclosure_charges_after_12m": "4.5% of outstanding principal",
            "part_prepayment_free": "Up to 25% after 12 months"
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
        "loan_variant": loan_variant,
        "variant_special_features": variant_features,
        "sanctioned_amount": f"₹{loan_amount:,.0f}",
        "interest_rate": f"{interest_rate}% p.a.",
        "tenure": f"{tenure} months",
        "monthly_emi": f"₹{emi_details['emi']:,.0f}",
        "processing_fee_breakdown": {
            "base_fee": f"₹{processing_fee:,.0f} (3.5% of loan amount)",
            "gst_18_percent": f"₹{gst_on_processing:,.0f}",
            "total_fee": f"₹{total_processing_fee:,.0f}"
        },
        "disbursement_amount": f"₹{disbursement_amount:,.0f}",
        "disbursement_account": f"{customer['bank_name']} - {customer['account_number'][-4:].rjust(len(customer['account_number']), 'X')}",
        "first_emi_date": first_emi_date,
        "repayment_terms": {
            "foreclosure_within_12_months": "6.5% of outstanding principal",
            "foreclosure_after_12_months": "4.5% of outstanding principal",
            "part_prepayment_free": "Up to 25% of outstanding principal (after 12 months)",
            "part_prepayment_charges": "Above 25%: Standard foreclosure charges apply"
        },
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
1. LOAN VALIDITY: This sanction letter is valid for 30 days from the date of issue.

2. DISBURSEMENT: Loan disbursement is subject to completion of all documentation
   and verification. Processing fee of 3.5% + GST will be deducted from loan amount.

3. REPAYMENT: EMI will be debited from the registered bank account on the due date.
   First EMI falls due after 45 days from disbursement.

4. FORECLOSURE CHARGES:
   - Within 12 months of loan disbursement: 6.5% of outstanding principal
   - After 12 months of loan disbursement: 4.5% of outstanding principal
   - Foreclosure allowed after payment of at least 6 EMIs

5. PART-PREPAYMENT:
   - Up to 25% of outstanding principal: Zero charges (after 12 months)
   - Above 25% of outstanding principal: Standard foreclosure charges apply
   - Minimum part-prepayment amount: ₹10,000
   - EMI amount remains same, tenure reduces proportionately

6. LATE PAYMENT CHARGES: 2% per month on overdue EMI amount plus GST.
   After 90 days overdue, loan may be classified as NPA.

7. INTEREST CALCULATION: Interest is calculated on reducing balance method.
   Effective Annual Percentage Rate (APR) includes processing fee and interest.

8. DEFAULT CONSEQUENCES: Non-payment will impact CIBIL score and future loan
   eligibility. Legal action may be initiated for recovery.

9. INSURANCE: Loan insurance is optional but recommended. Premium (if opted)
   will be added to EMI or deducted from loan amount.

10. BINDING AGREEMENT: All terms are as per the loan agreement to be signed
    at disbursement. This sanction is subject to credit policy and regulatory
    compliance.

───────────────────────────────────────────────────────────────────────────────
                         CHARGES BREAKDOWN
───────────────────────────────────────────────────────────────────────────────
Processing Fee:         3.5% of loan amount + GST (18%)
                        = ₹{loan['processing_fee']:,.0f}

Documentation Charges:  ₹500 (one-time, included in processing fee)
Stamp Duty:             As per state regulations (customer responsibility)
Cheque/ECS Bounce:      ₹500 per bounce
Duplicate Statement:    ₹100 per request
NOC Certificate:        ₹500 (after full repayment)
PDC Swap Charges:       ₹250 per swap

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


def offer_cross_sell_products(customer_id: str, tool_context: ToolContext) -> dict:
    """
    🎁 Contextual Cross-Sell Engine
    Offers relevant additional products after successful loan approval.
    
    Args:
        customer_id: The customer's unique ID
        tool_context: The tool context for state management
    
    Returns:
        dict: Cross-sell product recommendations
    """
    customer = get_customer_by_id(customer_id)
    loan_application = tool_context.state.get("loan_application", {})
    
    if not customer or not loan_application:
        return {
            "status": "error",
            "message": "Customer or loan application not found"
        }
    
    # Get recommended products
    products = recommend_cross_sell_products(customer, loan_application)
    
    # Format the message
    cross_sell_message = format_cross_sell_message(
        customer["name"],
        loan_application.get("loan_amount", 0),
        products
    )
    
    # Store in state
    tool_context.state["cross_sell_products"] = products
    tool_context.state["cross_sell_offered"] = True
    tool_context.state["cross_sell_message"] = cross_sell_message
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "cross_sell_offered",
        "products": [p["name"] for p in products],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    tool_context.state["interaction_history"] = current_history
    
    return {
        "status": "success",
        "message": cross_sell_message,
        "products": products,
        "summary": get_cross_sell_summary(products)
    }


def log_cross_sell_response(customer_id: str, interested: bool, product_name: str, tool_context: ToolContext) -> dict:
    """
    Logs customer's response to cross-sell offer.
    
    Args:
        customer_id: The customer's unique ID
        interested: Whether customer is interested
        product_name: Name of the product
        tool_context: The tool context for state management
    
    Returns:
        dict: Confirmation message
    """
    tool_context.state["cross_sell_accepted"] = interested
    tool_context.state["cross_sell_product_selected"] = product_name if interested else None
    
    # Add to interaction history
    current_history = tool_context.state.get("interaction_history", [])
    current_history.append({
        "action": "cross_sell_response",
        "interested": interested,
        "product": product_name,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    tool_context.state["interaction_history"] = current_history
    
    if interested:
        return {
            "status": "success",
            "message": f"Great! I'll send you detailed information about {product_name} via email and SMS. Our team will contact you within 24 hours to assist with the enrollment. 📧",
            "next_action": "email_details_sent"
        }
    else:
        return {
            "status": "success",
            "message": "No problem! The information is always available in your Tata Capital customer portal. You can explore it anytime. 👍",
            "next_action": "proceed_to_closure"
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


# Create the Sanction Letter Agent - Mr. Vikram Mehta
sanction_letter_agent = Agent(
    name="sanction_letter_agent",
    model=LiteLlm(model="mistral/mistral-large-2411"),
    description="Mr. Vikram Mehta - Documentation Officer who generates official sanction letters for approved loans",
    instruction="""
    You are Mr. Vikram Mehta, a meticulous and friendly Documentation Officer at Tata Capital.
    You take pride in creating perfect sanction letters and ensuring customers understand every detail of their loan.

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

    **Your Role - Working Invisibly as Priya Sharma:**

    You are a BACKEND AGENT. The customer only sees "Priya Sharma".
    NEVER introduce yourself. Continue seamlessly as Priya.
    Example: "Wonderful! Let me prepare your sanction letter..."

    **Your Documentation Process:**

    1. **Generate Official Sanction Letter (Professional & Accurate)**
       - Use generate_sanction_letter to create the official document data
       - Include all critical details: loan terms, EMI, disbursement info
       - Ensure every calculation is precise and verified
       - Celebrate: "Let me prepare your official sanction letter with all the details..."

    2. **Generate PDF Document (Save to Device)**
       - Immediately after generating sanction letter, use generate_sanction_letter_pdf
       - This creates a professional PDF and saves it to the 'sanction_letters' folder on the device
       - The PDF includes Tata Capital branding, all terms, and conditions
       - Inform customer: "I've generated your PDF sanction letter and saved it on your device!"

    3. **Provide PDF Preview (Clear & Accessible)**
       - Use get_sanction_letter_pdf to show the formatted content
       - Display all details clearly for customer review
       - Explain: "Here's a preview of your detailed sanction letter..."

    4. **Deliver to Customer (Multi-channel)**
       - Use send_sanction_letter to email and SMS the document
       - Confirm successful delivery
       - Provide the PDF file path and reference number
       - Reassure: "I've sent a copy to your registered email and mobile, PLUS saved it locally at: [file_path]"

    5. **Process Acceptance (Final Confirmation)**
       - Use accept_sanction when customer agrees to all terms
       - Explain next steps clearly: disbursement timeline, EMI start date
       - Provide all support contact information
       - Celebrate the milestone: "Perfect! Your loan is now fully processed and ready for disbursement!"

    6. **🎁 Offer Contextual Cross-Sell (Value-Added Products) - NEW!**
       - After successful acceptance, use offer_cross_sell_products
       - Present 1-2 relevant products based on customer profile
       - Be warm and helpful, NOT pushy: "Quick tip for you..."
       - Give customer full choice to accept, decline, or get details via email
       - Examples: Loan protection insurance, Credit card, Fixed deposit, Home loan, SIP
       - Use log_cross_sell_response to record customer's interest
       - If customer is interested: Send details via email
       - If customer declines: Respect their choice and proceed
       - IMPORTANT: This is optional and should ENHANCE the experience, not pressure

    7. **Summarize Complete Journey (Comprehensive Overview)**
       - Use get_loan_summary to show the entire loan journey
       - Display timeline of all steps completed
       - Highlight key milestones
       - Celebrate successful completion with genuine enthusiasm!

    **Sanction Letter Contents You Ensure:**
    - Complete customer details (name, ID, contact, address)
    - Loan amount sanctioned and tenure
    - Interest rate (% p.a.) and monthly EMI
    - Processing fee and net disbursement amount
    - First EMI date and payment schedule
    - Complete terms and conditions
    - Disbursement bank account details
    - Validity period of the sanction
    - Official reference numbers

    **Your Communication Style as Priya:**
    - NEVER introduce yourself (customer knows Priya)
    - Be detail-oriented and clear
    - Show enthusiasm about completion
    - Make all terms transparent
    - Provide clear next steps

    **Important Guidelines:**
    - Generate letter only after approval
    - Triple-check all details
    - Ensure customer understands terms
    - Explain disbursement timeline clearly
    - End on highly positive note

    **Professional Closing:**
    After acceptance:
    - Offer cross-sell products in friendly way
    - Provide disbursement timeline
    - Explain first EMI date
    - Give support information
    - Thank customer

    Remember: You work INVISIBLY as Priya. This is the final touchpoint. Make it memorable
    and ensure complete clarity and satisfaction.
    """,
    tools=[
        generate_sanction_letter,
        generate_sanction_letter_pdf,
        get_sanction_letter_pdf,
        send_sanction_letter,
        accept_sanction,
        offer_cross_sell_products,  # 🎁 NEW: Cross-sell engine
        log_cross_sell_response,     # 📊 NEW: Track cross-sell response
        get_loan_summary
    ],
)
