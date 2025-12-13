"""
Campaign & Ad Source Intelligence Data
Tracks how customers discovered Tata Capital and their intent
"""

from datetime import datetime, timedelta

# Campaign sources and their associated intents
CAMPAIGNS = {
    "GOOGLE_MEDICAL_EMERGENCY": {
        "campaign_id": "CAM_001",
        "source": "Google Ads",
        "keyword": "emergency medical loan",
        "intent": "URGENT_MEDICAL",
        "urgency_level": "HIGH",
        "typical_amount_range": (100000, 1500000),
        "conversion_rate": 0.42,
        "best_pitch": "medical_emergency",
        "offer_expiry_hours": 24
    },
    "GOOGLE_HOME_RENOVATION": {
        "campaign_id": "CAM_002",
        "source": "Google Ads",
        "keyword": "home renovation loan",
        "intent": "HOME_IMPROVEMENT",
        "urgency_level": "MEDIUM",
        "typical_amount_range": (200000, 2000000),
        "conversion_rate": 0.35,
        "best_pitch": "home_renovation_expert",
        "offer_expiry_hours": 72
    },
    "FACEBOOK_WEDDING": {
        "campaign_id": "CAM_003",
        "source": "Facebook Ads",
        "keyword": "wedding loan low emi",
        "intent": "WEDDING_PLANNING",
        "urgency_level": "MEDIUM",
        "typical_amount_range": (200000, 2500000),
        "conversion_rate": 0.38,
        "best_pitch": "dream_wedding",
        "offer_expiry_hours": 48
    },
    "ORGANIC_TRAVEL": {
        "campaign_id": "CAM_004",
        "source": "Organic Search",
        "keyword": "personal loan for travel",
        "intent": "LEISURE_TRAVEL",
        "urgency_level": "LOW",
        "typical_amount_range": (50000, 500000),
        "conversion_rate": 0.28,
        "best_pitch": "dream_vacation",
        "offer_expiry_hours": 96
    },
    "EMAIL_TOPUP": {
        "campaign_id": "CAM_005",
        "source": "Email Marketing",
        "keyword": "existing customer top-up offer",
        "intent": "ADDITIONAL_FUNDS",
        "urgency_level": "LOW",
        "typical_amount_range": (100000, 700000),
        "conversion_rate": 0.55,
        "best_pitch": "loyal_customer_upgrade",
        "offer_expiry_hours": 120
    },
    "REFERRAL": {
        "campaign_id": "CAM_006",
        "source": "Customer Referral",
        "keyword": "friend referral",
        "intent": "GENERAL_PURPOSE",
        "urgency_level": "MEDIUM",
        "typical_amount_range": (100000, 1500000),
        "conversion_rate": 0.48,
        "best_pitch": "trusted_recommendation",
        "offer_expiry_hours": 72
    },
    "DIRECT_WEBSITE": {
        "campaign_id": "CAM_007",
        "source": "Direct Website",
        "keyword": "personal loan best rates",
        "intent": "RATE_SHOPPING",
        "urgency_level": "LOW",
        "typical_amount_range": (150000, 3500000),
        "conversion_rate": 0.32,
        "best_pitch": "best_rates_guarantee",
        "offer_expiry_hours": 48
    },
    "SMS_PREAPPROVED": {
        "campaign_id": "CAM_008",
        "source": "SMS Campaign",
        "keyword": "pre-approved loan offer",
        "intent": "PREAPPROVED_INQUIRY",
        "urgency_level": "MEDIUM",
        "typical_amount_range": (200000, 2000000),
        "conversion_rate": 0.62,
        "best_pitch": "exclusive_preapproval",
        "offer_expiry_hours": 48
    }
}


# Customer journey tracking
CUSTOMER_CAMPAIGNS = {
    "CUST001": {
        "campaign_source": "EMAIL_TOPUP",
        "landing_date": datetime.now() - timedelta(days=2),
        "visits_count": 3,
        "pages_viewed": ["home", "personal-loan", "emi-calculator", "apply"],
        "time_on_site_minutes": 45,
        "previous_interactions": [
            {"date": "2023-06-20", "action": "Loan inquiry", "result": "Applied but withdrawn"},
            {"date": "2024-03-15", "action": "EMI calculator", "result": "No application"}
        ],
        "current_loans": [
            {"type": "Personal Loan", "amount": 300000, "emi": 8500, "outstanding": 150000, "status": "ACTIVE"}
        ],
        "relationship_tenure_years": 2,
        "payment_history": "EXCELLENT"
    },
    "CUST002": {
        "campaign_source": "GOOGLE_MEDICAL_EMERGENCY",
        "landing_date": datetime.now() - timedelta(hours=3),
        "visits_count": 1,
        "pages_viewed": ["medical-loan", "apply"],
        "time_on_site_minutes": 12,
        "previous_interactions": [],
        "current_loans": [],
        "relationship_tenure_years": 0,
        "payment_history": None
    },
    "CUST003": {
        "campaign_source": "FACEBOOK_WEDDING",
        "landing_date": datetime.now() - timedelta(days=5),
        "visits_count": 5,
        "pages_viewed": ["wedding-loan", "emi-calculator", "documents-required", "customer-reviews"],
        "time_on_site_minutes": 78,
        "previous_interactions": [],
        "current_loans": [],
        "relationship_tenure_years": 0,
        "payment_history": None
    },
    "CUST004": {
        "campaign_source": "DIRECT_WEBSITE",
        "landing_date": datetime.now() - timedelta(days=1),
        "visits_count": 2,
        "pages_viewed": ["home", "interest-rates", "compare"],
        "time_on_site_minutes": 28,
        "previous_interactions": [
            {"date": "2024-11-10", "action": "Rate inquiry", "result": "No application"}
        ],
        "current_loans": [],
        "relationship_tenure_years": 0,
        "payment_history": None
    },
    "CUST005": {
        "campaign_source": "GOOGLE_HOME_RENOVATION",
        "landing_date": datetime.now() - timedelta(hours=8),
        "visits_count": 2,
        "pages_viewed": ["home-renovation-loan", "documents", "apply"],
        "time_on_site_minutes": 35,
        "previous_interactions": [],
        "current_loans": [],
        "relationship_tenure_years": 0,
        "payment_history": None
    }
}


def get_campaign_data(customer_id: str) -> dict:
    """Get campaign and journey data for a customer"""
    journey = CUSTOMER_CAMPAIGNS.get(customer_id, {
        "campaign_source": "DIRECT_WEBSITE",
        "landing_date": datetime.now(),
        "visits_count": 1,
        "pages_viewed": ["home"],
        "time_on_site_minutes": 5,
        "previous_interactions": [],
        "current_loans": [],
        "relationship_tenure_years": 0,
        "payment_history": None
    })
    
    campaign_key = journey["campaign_source"]
    campaign = CAMPAIGNS.get(campaign_key, CAMPAIGNS["DIRECT_WEBSITE"])
    
    # Calculate customer type
    if journey["relationship_tenure_years"] > 0:
        customer_type = "REPEAT_CUSTOMER"
    elif journey["previous_interactions"]:
        customer_type = "RETURNING_VISITOR"
    else:
        customer_type = "FIRST_TIME"
    
    return {
        "customer_id": customer_id,
        "customer_type": customer_type,
        "campaign": campaign,
        "journey": journey,
        "intent": campaign["intent"],
        "urgency_level": campaign["urgency_level"],
        "best_pitch_strategy": campaign["best_pitch"],
        "offer_expires_in_hours": campaign["offer_expiry_hours"]
    }


def get_personalized_opening(customer_id: str, customer_name: str, campaign_data: dict) -> str:
    """Generate a personalized opening message based on campaign and customer history"""
    
    campaign = campaign_data["campaign"]
    journey = campaign_data["journey"]
    intent = campaign["intent"]
    customer_type = campaign_data["customer_type"]
    
    # Base greeting
    greeting = f"Hi {customer_name}! I'm Priya Sharma from Tata Capital. "
    
    # Returning customer personalization
    if customer_type == "REPEAT_CUSTOMER":
        tenure = journey["relationship_tenure_years"]
        payment_history = journey["payment_history"]
        
        if payment_history == "EXCELLENT":
            greeting += f"It's wonderful to see you again! You've been a valued customer for {tenure} years with an excellent repayment track record. "
        else:
            greeting += f"Welcome back! We appreciate your {tenure}-year relationship with us. "
        
        # Intent-based context
        if intent == "ADDITIONAL_FUNDS":
            greeting += "I noticed you're interested in our exclusive top-up loan offer. Based on your excellent payment history, you're pre-approved for additional funds at your existing rate! "
        else:
            greeting += "As a valued customer, you have access to our best rates and priority processing. "
    
    elif customer_type == "RETURNING_VISITOR":
        previous_action = journey["previous_interactions"][-1]["action"] if journey["previous_interactions"] else "inquiry"
        greeting += f"Welcome back! I see you previously explored our {previous_action}. "
    
    else:  # FIRST_TIME
        greeting += "Welcome! "
    
    # Intent-specific messaging
    if intent == "URGENT_MEDICAL":
        greeting += "I understand you need funds for a medical emergency. We offer instant approval for medical loans with flexible repayment options. "
    
    elif intent == "HOME_IMPROVEMENT":
        greeting += "Looking to renovate your home? Great choice! We offer specialized home renovation loans with flexible disbursement options. "
    
    elif intent == "WEDDING_PLANNING":
        greeting += "Planning your dream wedding? Congratulations! Our wedding loans come with flexible EMIs and cover all your wedding expenses. "
    
    elif intent == "LEISURE_TRAVEL":
        greeting += "Planning your dream vacation? Wonderful! Our travel loans offer quick approval and flexible repayment. "
    
    elif intent == "RATE_SHOPPING":
        greeting += "I see you're comparing rates. Let me share our best offer with you - starting at just 10.99% p.a. with zero hidden charges! "
    
    elif intent == "PREAPPROVED_INQUIRY":
        greeting += "Yes, your pre-approved loan offer is ready! You can get funds in your account within 24 hours. "
    
    else:  # GENERAL_PURPOSE
        greeting += "How can I help you with your financial needs today? "
    
    # Add urgency if applicable
    if campaign["urgency_level"] == "HIGH":
        greeting += f"\n\n⚡ Quick note: Your special offer expires in {campaign['offer_expiry_hours']} hours!"
    elif campaign["offer_expiry_hours"] <= 48:
        greeting += f"\n\n⏰ This exclusive offer is valid for the next {campaign['offer_expiry_hours']} hours."
    
    greeting += "\n\nWhat specific amount are you looking for?"
    
    return greeting
