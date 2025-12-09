"""
Mock Credit Bureau API
Provides credit scores and credit history for customers
Credit scores are out of 900 (similar to CIBIL scores in India)
"""

import random
from datetime import datetime, timedelta

CREDIT_SCORES = {
    "CUST001": {
        "customer_id": "CUST001",
        "pan_number": "ABCDE1234F",
        "credit_score": 780,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 5,
            "active_accounts": 3,
            "closed_accounts": 2,
            "overdue_accounts": 0,
            "credit_utilization": 35,
            "oldest_account_age_months": 96,
            "recent_inquiries": 1,
            "payment_history": "Good",
            "defaults": 0
        }
    },
    "CUST002": {
        "customer_id": "CUST002",
        "pan_number": "FGHIJ5678K",
        "credit_score": 820,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 4,
            "active_accounts": 2,
            "closed_accounts": 2,
            "overdue_accounts": 0,
            "credit_utilization": 20,
            "oldest_account_age_months": 72,
            "recent_inquiries": 0,
            "payment_history": "Excellent",
            "defaults": 0
        }
    },
    "CUST003": {
        "customer_id": "CUST003",
        "pan_number": "KLMNO9012P",
        "credit_score": 750,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 8,
            "active_accounts": 4,
            "closed_accounts": 4,
            "overdue_accounts": 0,
            "credit_utilization": 45,
            "oldest_account_age_months": 156,
            "recent_inquiries": 2,
            "payment_history": "Good",
            "defaults": 0
        }
    },
    "CUST004": {
        "customer_id": "CUST004",
        "pan_number": "PQRST3456U",
        "credit_score": 810,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 3,
            "active_accounts": 2,
            "closed_accounts": 1,
            "overdue_accounts": 0,
            "credit_utilization": 25,
            "oldest_account_age_months": 60,
            "recent_inquiries": 1,
            "payment_history": "Excellent",
            "defaults": 0
        }
    },
    "CUST005": {
        "customer_id": "CUST005",
        "pan_number": "UVWXY7890Z",
        "credit_score": 720,
        "score_date": "2024-12-01",
        "score_range": "Good (700-749)",
        "credit_history": {
            "total_accounts": 6,
            "active_accounts": 3,
            "closed_accounts": 3,
            "overdue_accounts": 1,
            "credit_utilization": 55,
            "oldest_account_age_months": 180,
            "recent_inquiries": 3,
            "payment_history": "Fair",
            "defaults": 0
        }
    },
    "CUST006": {
        "customer_id": "CUST006",
        "pan_number": "ABCFG1234H",
        "credit_score": 800,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 4,
            "active_accounts": 2,
            "closed_accounts": 2,
            "overdue_accounts": 0,
            "credit_utilization": 30,
            "oldest_account_age_months": 48,
            "recent_inquiries": 0,
            "payment_history": "Excellent",
            "defaults": 0
        }
    },
    "CUST007": {
        "customer_id": "CUST007",
        "pan_number": "HIJKL5678M",
        "credit_score": 790,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 7,
            "active_accounts": 4,
            "closed_accounts": 3,
            "overdue_accounts": 0,
            "credit_utilization": 40,
            "oldest_account_age_months": 120,
            "recent_inquiries": 1,
            "payment_history": "Good",
            "defaults": 0
        }
    },
    "CUST008": {
        "customer_id": "CUST008",
        "pan_number": "NOPQR9012S",
        "credit_score": 770,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 5,
            "active_accounts": 3,
            "closed_accounts": 2,
            "overdue_accounts": 0,
            "credit_utilization": 35,
            "oldest_account_age_months": 84,
            "recent_inquiries": 2,
            "payment_history": "Good",
            "defaults": 0
        }
    },
    "CUST009": {
        "customer_id": "CUST009",
        "pan_number": "TUVWX3456Y",
        "credit_score": 760,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 9,
            "active_accounts": 4,
            "closed_accounts": 5,
            "overdue_accounts": 0,
            "credit_utilization": 42,
            "oldest_account_age_months": 216,
            "recent_inquiries": 1,
            "payment_history": "Good",
            "defaults": 0
        }
    },
    "CUST010": {
        "customer_id": "CUST010",
        "pan_number": "YZABC7890D",
        "credit_score": 680,
        "score_date": "2024-12-01",
        "score_range": "Fair (650-699)",
        "credit_history": {
            "total_accounts": 3,
            "active_accounts": 2,
            "closed_accounts": 1,
            "overdue_accounts": 1,
            "credit_utilization": 65,
            "oldest_account_age_months": 36,
            "recent_inquiries": 4,
            "payment_history": "Fair",
            "defaults": 0
        }
    },
    "CUST011": {
        "customer_id": "CUST011",
        "pan_number": "DEFGH1234I",
        "credit_score": 740,
        "score_date": "2024-12-01",
        "score_range": "Good (700-749)",
        "credit_history": {
            "total_accounts": 6,
            "active_accounts": 3,
            "closed_accounts": 3,
            "overdue_accounts": 0,
            "credit_utilization": 50,
            "oldest_account_age_months": 144,
            "recent_inquiries": 2,
            "payment_history": "Good",
            "defaults": 0
        }
    },
    "CUST012": {
        "customer_id": "CUST012",
        "pan_number": "JKLMN5678O",
        "credit_score": 830,
        "score_date": "2024-12-01",
        "score_range": "Excellent (750-900)",
        "credit_history": {
            "total_accounts": 5,
            "active_accounts": 3,
            "closed_accounts": 2,
            "overdue_accounts": 0,
            "credit_utilization": 15,
            "oldest_account_age_months": 108,
            "recent_inquiries": 0,
            "payment_history": "Excellent",
            "defaults": 0
        }
    }
}


def get_credit_score(customer_id: str) -> dict:
    """
    Fetch credit score from mock credit bureau API
    Returns credit score out of 900 with credit history details
    """
    credit_data = CREDIT_SCORES.get(customer_id)
    if not credit_data:
        return {
            "status": "error",
            "message": "Customer not found in credit bureau records"
        }
    
    return {
        "status": "success",
        "customer_id": customer_id,
        "credit_score": credit_data["credit_score"],
        "score_date": credit_data["score_date"],
        "score_range": credit_data["score_range"],
        "credit_history": credit_data["credit_history"]
    }


def get_credit_score_by_pan(pan_number: str) -> dict:
    """
    Fetch credit score using PAN number
    """
    for customer_id, credit_data in CREDIT_SCORES.items():
        if credit_data["pan_number"] == pan_number:
            return {
                "status": "success",
                "customer_id": customer_id,
                "credit_score": credit_data["credit_score"],
                "score_date": credit_data["score_date"],
                "score_range": credit_data["score_range"],
                "credit_history": credit_data["credit_history"]
            }
    
    return {
        "status": "error",
        "message": "PAN number not found in credit bureau records"
    }


def check_eligibility_by_score(credit_score: int) -> dict:
    """
    Check loan eligibility based on credit score
    Minimum score required: 700
    """
    if credit_score >= 750:
        return {
            "eligible": True,
            "risk_category": "Low Risk",
            "interest_rate_range": "10.5% - 12%",
            "message": "Excellent credit score. Eligible for best interest rates."
        }
    elif credit_score >= 700:
        return {
            "eligible": True,
            "risk_category": "Medium Risk",
            "interest_rate_range": "12% - 15%",
            "message": "Good credit score. Eligible for standard interest rates."
        }
    elif credit_score >= 650:
        return {
            "eligible": True,
            "risk_category": "High Risk",
            "interest_rate_range": "15% - 18%",
            "message": "Fair credit score. Eligible with higher interest rates."
        }
    else:
        return {
            "eligible": False,
            "risk_category": "Very High Risk",
            "interest_rate_range": "N/A",
            "message": "Credit score below minimum threshold. Not eligible for personal loan."
        }
