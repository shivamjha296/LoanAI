"""
Mock Offer Mart Server
Contains pre-approved loan offers for customers
"""

from datetime import datetime, timedelta

LOAN_OFFERS = {
    "CUST001": {
        "customer_id": "CUST001",
        "customer_name": "Rajesh Kumar",
        "pre_approved_amount": 500000,
        "max_tenure_months": 60,
        "interest_rate": 11.5,
        "processing_fee_percent": 1.5,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": False,
        "min_loan_amount": 50000
    },
    "CUST002": {
        "customer_id": "CUST002",
        "customer_name": "Priya Sharma",
        "pre_approved_amount": 750000,
        "max_tenure_months": 60,
        "interest_rate": 10.75,
        "processing_fee_percent": 1.0,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "Zero processing fee for first-time borrowers",
        "min_loan_amount": 50000
    },
    "CUST003": {
        "customer_id": "CUST003",
        "customer_name": "Amit Patel",
        "pre_approved_amount": 1000000,
        "max_tenure_months": 72,
        "interest_rate": 11.0,
        "processing_fee_percent": 1.5,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "Business owner special - Flexible EMI options",
        "min_loan_amount": 100000
    },
    "CUST004": {
        "customer_id": "CUST004",
        "customer_name": "Sunita Verma",
        "pre_approved_amount": 800000,
        "max_tenure_months": 60,
        "interest_rate": 10.5,
        "processing_fee_percent": 1.0,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "IT Professional Special - 0.25% rate discount",
        "min_loan_amount": 50000
    },
    "CUST005": {
        "customer_id": "CUST005",
        "customer_name": "Vikram Singh",
        "pre_approved_amount": 400000,
        "max_tenure_months": 48,
        "interest_rate": 12.5,
        "processing_fee_percent": 2.0,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": False,
        "min_loan_amount": 50000
    },
    "CUST006": {
        "customer_id": "CUST006",
        "customer_name": "Neha Gupta",
        "pre_approved_amount": 700000,
        "max_tenure_months": 60,
        "interest_rate": 10.75,
        "processing_fee_percent": 1.0,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "CA Special - Priority processing",
        "min_loan_amount": 50000
    },
    "CUST007": {
        "customer_id": "CUST007",
        "customer_name": "Ravi Menon",
        "pre_approved_amount": 1500000,
        "max_tenure_months": 72,
        "interest_rate": 10.25,
        "processing_fee_percent": 1.0,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "Doctor's Loan - No income proof required",
        "min_loan_amount": 100000
    },
    "CUST008": {
        "customer_id": "CUST008",
        "customer_name": "Anita Desai",
        "pre_approved_amount": 600000,
        "max_tenure_months": 60,
        "interest_rate": 11.25,
        "processing_fee_percent": 1.5,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": False,
        "min_loan_amount": 50000
    },
    "CUST009": {
        "customer_id": "CUST009",
        "customer_name": "Suresh Reddy",
        "pre_approved_amount": 900000,
        "max_tenure_months": 60,
        "interest_rate": 11.0,
        "processing_fee_percent": 1.0,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "Professor Special - Academic institution discount",
        "min_loan_amount": 50000
    },
    "CUST010": {
        "customer_id": "CUST010",
        "customer_name": "Deepa Nair",
        "pre_approved_amount": 300000,
        "max_tenure_months": 36,
        "interest_rate": 14.0,
        "processing_fee_percent": 2.5,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": False,
        "min_loan_amount": 25000
    },
    "CUST011": {
        "customer_id": "CUST011",
        "customer_name": "Manoj Tiwari",
        "pre_approved_amount": 1200000,
        "max_tenure_months": 72,
        "interest_rate": 11.5,
        "processing_fee_percent": 1.5,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "Legal Professional Special - Extended tenure option",
        "min_loan_amount": 100000
    },
    "CUST012": {
        "customer_id": "CUST012",
        "customer_name": "Kavita Joshi",
        "pre_approved_amount": 850000,
        "max_tenure_months": 60,
        "interest_rate": 10.5,
        "processing_fee_percent": 0.5,
        "offer_valid_until": "2025-03-31",
        "offer_type": "PRE_APPROVED",
        "special_offer": True,
        "special_offer_details": "Bank Employee Special - Lowest processing fee",
        "min_loan_amount": 50000
    }
}


def get_pre_approved_offer(customer_id: str) -> dict:
    """
    Fetch pre-approved loan offer for a customer from Offer Mart
    """
    offer = LOAN_OFFERS.get(customer_id)
    if not offer:
        return {
            "status": "error",
            "message": "No pre-approved offer found for this customer"
        }
    
    return {
        "status": "success",
        "offer": offer
    }


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> dict:
    """
    Calculate EMI for a loan
    EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)
    where P = Principal, r = monthly interest rate, n = number of months
    """
    monthly_rate = annual_rate / (12 * 100)
    
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    
    total_payment = emi * tenure_months
    total_interest = total_payment - principal
    
    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "principal": principal,
        "interest_rate": annual_rate,
        "tenure_months": tenure_months
    }


def check_loan_eligibility(customer_id: str, requested_amount: float, monthly_salary: float) -> dict:
    """
    Check if customer is eligible for the requested loan amount
    Rules:
    - If amount <= pre_approved_limit: Instant approval
    - If amount <= 2x pre_approved_limit: Need salary slip, EMI should be <= 50% of salary
    - If amount > 2x pre_approved_limit: Reject
    """
    offer = LOAN_OFFERS.get(customer_id)
    if not offer:
        return {
            "status": "error",
            "eligible": False,
            "message": "No pre-approved offer found for this customer"
        }
    
    pre_approved_limit = offer["pre_approved_amount"]
    
    # Calculate EMI for maximum tenure
    max_tenure = offer["max_tenure_months"]
    interest_rate = offer["interest_rate"]
    emi_details = calculate_emi(requested_amount, interest_rate, max_tenure)
    emi = emi_details["emi"]
    
    # Rule 1: Within pre-approved limit - instant approval
    if requested_amount <= pre_approved_limit:
        return {
            "status": "success",
            "eligible": True,
            "approval_type": "INSTANT",
            "message": f"Congratulations! Your loan of ₹{requested_amount:,.0f} is within your pre-approved limit. Instant approval available.",
            "emi_details": emi_details,
            "documents_required": ["None - Pre-approved"]
        }
    
    # Rule 2: Up to 2x pre-approved limit - need salary slip
    elif requested_amount <= 2 * pre_approved_limit:
        # Check if EMI is <= 50% of salary
        emi_to_salary_ratio = (emi / monthly_salary) * 100
        
        if emi_to_salary_ratio <= 50:
            return {
                "status": "success",
                "eligible": True,
                "approval_type": "CONDITIONAL",
                "message": f"Your loan of ₹{requested_amount:,.0f} exceeds pre-approved limit but is within extended limit. Salary slip verification required.",
                "emi_details": emi_details,
                "emi_to_salary_ratio": round(emi_to_salary_ratio, 2),
                "documents_required": ["Salary Slip (last 3 months)", "Bank Statement (last 6 months)"]
            }
        else:
            return {
                "status": "success",
                "eligible": False,
                "approval_type": "REJECTED",
                "message": f"EMI of ₹{emi:,.0f} exceeds 50% of your monthly salary (₹{monthly_salary:,.0f}). Please request a lower amount.",
                "emi_details": emi_details,
                "emi_to_salary_ratio": round(emi_to_salary_ratio, 2),
                "max_eligible_amount": calculate_max_eligible_amount(monthly_salary, interest_rate, max_tenure)
            }
    
    # Rule 3: More than 2x pre-approved limit - reject
    else:
        max_allowed = 2 * pre_approved_limit
        return {
            "status": "success",
            "eligible": False,
            "approval_type": "REJECTED",
            "message": f"Requested amount ₹{requested_amount:,.0f} exceeds maximum allowed limit of ₹{max_allowed:,.0f} (2x pre-approved limit).",
            "max_allowed_amount": max_allowed,
            "pre_approved_limit": pre_approved_limit
        }


def calculate_max_eligible_amount(monthly_salary: float, interest_rate: float, tenure_months: int) -> float:
    """
    Calculate maximum eligible loan amount based on 50% EMI to salary ratio
    """
    max_emi = monthly_salary * 0.5
    monthly_rate = interest_rate / (12 * 100)
    
    if monthly_rate == 0:
        max_amount = max_emi * tenure_months
    else:
        max_amount = max_emi * (((1 + monthly_rate) ** tenure_months) - 1) / (monthly_rate * ((1 + monthly_rate) ** tenure_months))
    
    return round(max_amount, 2)


def get_available_tenures(customer_id: str) -> dict:
    """
    Get available loan tenures for a customer
    """
    offer = LOAN_OFFERS.get(customer_id)
    if not offer:
        return {
            "status": "error",
            "message": "No pre-approved offer found for this customer"
        }
    
    max_tenure = offer["max_tenure_months"]
    tenures = [12, 24, 36, 48, 60]
    if max_tenure > 60:
        tenures.append(72)
    
    available_tenures = [t for t in tenures if t <= max_tenure]
    
    return {
        "status": "success",
        "available_tenures": available_tenures,
        "max_tenure_months": max_tenure
    }
