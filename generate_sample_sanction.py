"""
Quick script to generate a sample sanction letter PDF
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from loan_master_agent.sub_agents.sanction_letter_agent.agent import generate_sanction_letter_pdf
from google.adk.tools.tool_context import ToolContext
from datetime import datetime, timedelta

# Create a mock tool context with sample data
class MockToolContext:
    def __init__(self):
        self.state = {
            "customer_id": "CUST001",
            "customer_name": "Rajesh Kumar Singh",
            "loan_application": {
                "application_id": "LA20251214123456",
                "loan_amount": 500000,
                "tenure_months": 36,
                "purpose": "Home Renovation"
            },
            "current_offer": {
                "interest_rate": 11.50,
                "processing_fee_percent": 1.5
            },
            "sanction_letter": {
                "sanction_reference": "SL2025121400123",
                "approval_reference": "XXXXXXXXX",
                "sanction_date": datetime.now().strftime("%d / %m / %Y"),
                "validity_until": (datetime.now() + timedelta(days=60)).strftime("%d / %m / %Y"),
                "borrower_details": {
                    "name": "Mr Rakesh Singh",
                    "customer_id": "CUST001",
                    "pan": "ABCDE1234F",
                    "phone": "+91-9876543210",
                    "email": "rakesh.singh@email.com",
                    "address": "Flat 301, Building A, Green Valley Apartments, Andheri West, Mumbai - 400053"
                },
                "loan_details": {
                    "loan_type": "Home Loan",
                    "sanctioned_amount": 4500000,
                    "interest_rate": 8.50,
                    "tenure_months": 240,
                    "processing_fee": 9000,
                    "disbursement_amount": 4491000,
                    "purpose": "Purchase of Residential Property",
                    "emi": 34000,
                    "first_emi_date": (datetime.now() + timedelta(days=30)).strftime("%d %B %Y"),
                    "total_interest": 3660000,
                    "total_repayment": 8160000
                },
                "disbursement_details": {
                    "bank_name": "HDFC Bank",
                    "account_number": "XXXX XXXX 1234",
                    "disbursement_mode": "NEFT / RTGS",
                    "expected_disbursement": (datetime.now() + timedelta(days=7)).strftime("%d %B %Y")
                }
            }
        }

# Generate the PDF
print("Generating sample sanction letter PDF...")
tool_context = MockToolContext()

result = generate_sanction_letter_pdf("CUST001", tool_context)

if result["status"] == "success":
    print(f"\n✅ SUCCESS!")
    print(f"PDF generated: {result['pdf_path']}")
    print(f"File size: {result['file_size']}")
    print(f"\nOpen the file to view the sanction letter.")
elif result["status"] == "partial":
    print(f"\n⚠️ PARTIAL SUCCESS (HTML generated)")
    print(f"HTML file: {result.get('html_path', 'N/A')}")
    print(f"Suggestion: {result.get('suggestion', 'N/A')}")
else:
    print(f"\n❌ ERROR:")
    print(f"Message: {result['message']}")
