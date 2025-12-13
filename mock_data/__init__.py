# Mock Data Module for BFSI Loan Chatbot
# Contains synthetic customer data, CRM data, credit bureau API, and offer mart data
# NEW: Campaign intelligence, persuasion strategies, objection handling, sentiment analysis, analytics, cross-sell

from .customer_data import CUSTOMERS, get_customer_by_phone, get_customer_by_id
from .crm_data import CRM_DATA, get_kyc_data
from .credit_bureau import CREDIT_SCORES, get_credit_score
from .offer_mart import LOAN_OFFERS, get_pre_approved_offer
from .campaign_data import CAMPAIGNS, get_campaign_data, get_personalized_opening
from .persuasion_strategy import determine_customer_profile, get_strategy_prompt
from .objection_handler import detect_objection, get_objection_handling_prompt
from .sentiment_analyzer import detect_sentiment, get_sentiment_context_for_agent, track_sentiment_evolution
from .analytics_tracker import log_conversation, get_performance_dashboard, display_performance_dashboard
from .cross_sell_engine import recommend_cross_sell_products, format_cross_sell_message, get_cross_sell_summary

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
    "CAMPAIGNS",
    "get_campaign_data",
    "get_personalized_opening",
    "determine_customer_profile",
    "get_strategy_prompt",
    "detect_objection",
    "get_objection_handling_prompt",
    "detect_sentiment",
    "get_sentiment_context_for_agent",
    "track_sentiment_evolution",
    "log_conversation",
    "get_performance_dashboard",
    "display_performance_dashboard",
    "recommend_cross_sell_products",
    "format_cross_sell_message",
    "get_cross_sell_summary",
]
