# Mock Data Module for BFSI Loan Chatbot
# Contains synthetic customer data, CRM data, credit bureau API, and offer mart data

from .customer_data import CUSTOMERS, get_customer_by_phone, get_customer_by_id
from .crm_data import CRM_DATA, get_kyc_data
from .credit_bureau import CREDIT_SCORES, get_credit_score
from .offer_mart import LOAN_OFFERS, get_pre_approved_offer

__all__ = [
    "CUSTOMERS",
    "get_customer_by_phone",
    "get_customer_by_id",
    "CRM_DATA",
    "get_kyc_data",
    "CREDIT_SCORES",
    "get_credit_score",
    "LOAN_OFFERS",
    "get_pre_approved_offer",
]
