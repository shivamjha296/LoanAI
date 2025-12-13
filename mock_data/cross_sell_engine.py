"""
Contextual Cross-Sell Engine
Offers relevant additional products after successful loan approval
"""

from typing import Dict, List
import random


# Product catalog for cross-selling
CROSS_SELL_PRODUCTS = {
    "LOAN_PROTECTION_INSURANCE": {
        "name": "Loan Protection Insurance",
        "description": "Comprehensive coverage for your loan in case of job loss, disability, or critical illness",
        "price": "₹150/month",
        "benefits": [
            "EMI coverage for up to 12 months in case of job loss",
            "Full loan waiver in case of critical illness or disability",
            "Accidental death coverage of loan amount",
            "Zero waiting period"
        ],
        "relevance_score": {
            "medical_emergency": 0.9,
            "high_loan_amount": 0.8,
            "first_time_borrower": 0.7,
            "default": 0.6
        },
        "icon": "🛡️"
    },
    "CREDIT_CARD": {
        "name": "Tata Capital Premium Credit Card",
        "description": "Lifetime free credit card with cashback and rewards",
        "price": "₹0 annual fee (Lifetime)",
        "benefits": [
            "5% cashback on all purchases",
            "2 reward points per ₹100 spent",
            "Complimentary airport lounge access (4 times/year)",
            "Special offers on dining and shopping"
        ],
        "relevance_score": {
            "high_credit_score": 0.9,
            "repeat_customer": 0.7,
            "affluent": 0.8,
            "default": 0.5
        },
        "icon": "💳"
    },
    "FIXED_DEPOSIT": {
        "name": "Tax-Saving Fixed Deposit",
        "description": "Earn attractive interest while saving tax under Section 80C",
        "price": "Min. ₹10,000 investment",
        "benefits": [
            "7.5% p.a. interest rate (higher than banks)",
            "Tax deduction up to ₹1.5 lakh under 80C",
            "Flexible tenure: 1-5 years",
            "Auto-renewal option available"
        ],
        "relevance_score": {
            "high_income": 0.8,
            "tax_season": 0.9,
            "affluent": 0.7,
            "default": 0.4
        },
        "icon": "💰"
    },
    "HOME_LOAN": {
        "name": "Home Loan with Pre-Approved Limit",
        "description": "Special rates for existing customers planning to buy property",
        "price": "Starting 8.5% p.a.",
        "benefits": [
            "Pre-approved limit up to ₹50 lakhs",
            "0.5% rate discount for existing customers",
            "Tax benefits up to ₹3.5 lakhs/year",
            "Flexible repayment options"
        ],
        "relevance_score": {
            "home_renovation_customer": 0.9,
            "high_income": 0.8,
            "repeat_customer": 0.7,
            "default": 0.3
        },
        "icon": "🏠"
    },
    "INVESTMENT_PLAN": {
        "name": "Systematic Investment Plan (SIP)",
        "description": "Start investing in mutual funds with as low as ₹500/month",
        "price": "Starting ₹500/month",
        "benefits": [
            "Potential returns of 12-15% p.a.",
            "Zero commission on direct plans",
            "Free portfolio management",
            "Tax-saving options available"
        ],
        "relevance_score": {
            "young_professional": 0.8,
            "high_income": 0.7,
            "affluent": 0.6,
            "default": 0.5
        },
        "icon": "📈"
    }
}


def recommend_cross_sell_products(customer_data: Dict, loan_data: Dict) -> List[Dict]:
    """
    Recommend relevant cross-sell products based on customer profile and loan.
    
    Args:
        customer_data: Customer profile information
        loan_data: Approved loan details
    
    Returns:
        list: Recommended products sorted by relevance
    """
    recommendations = []
    
    # Determine customer context
    loan_amount = loan_data.get("loan_amount", 0)
    loan_purpose = loan_data.get("purpose", "").lower()
    credit_score = customer_data.get("credit_score", 750)
    monthly_salary = customer_data.get("monthly_salary", 50000)
    
    # Calculate relevance for each product
    for product_id, product_info in CROSS_SELL_PRODUCTS.items():
        relevance_scores = product_info["relevance_score"]
        
        # Determine context-specific relevance
        if loan_purpose in ["medical emergency", "health"] and product_id == "LOAN_PROTECTION_INSURANCE":
            relevance = relevance_scores.get("medical_emergency", 0.6)
        elif loan_amount >= 500000 and product_id == "LOAN_PROTECTION_INSURANCE":
            relevance = relevance_scores.get("high_loan_amount", 0.6)
        elif credit_score >= 800 and product_id == "CREDIT_CARD":
            relevance = relevance_scores.get("high_credit_score", 0.5)
        elif monthly_salary >= 100000:
            relevance = relevance_scores.get("affluent", 0.5)
        elif "home" in loan_purpose or "renovation" in loan_purpose:
            relevance = relevance_scores.get("home_renovation_customer", 0.3)
        else:
            relevance = relevance_scores.get("default", 0.3)
        
        # Add small randomization to vary recommendations
        relevance += random.uniform(-0.05, 0.05)
        
        recommendations.append({
            "product_id": product_id,
            "name": product_info["name"],
            "description": product_info["description"],
            "price": product_info["price"],
            "benefits": product_info["benefits"],
            "icon": product_info["icon"],
            "relevance_score": round(relevance, 2)
        })
    
    # Sort by relevance and return top 2
    recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)
    return recommendations[:2]


def format_cross_sell_message(customer_name: str, loan_amount: float, products: List[Dict]) -> str:
    """
    Format a friendly cross-sell message.
    
    Args:
        customer_name: Customer's name
        loan_amount: Approved loan amount
        products: List of recommended products
    
    Returns:
        str: Formatted message for agent to deliver
    """
    if not products:
        return ""
    
    # Primary product
    primary_product = products[0]
    
    message = f"""
Congratulations on your ₹{loan_amount:,.0f} loan approval, {customer_name}! 🎉

Quick tip: Based on your profile, you might be interested in our {primary_product['icon']} **{primary_product['name']}**:

✨ {primary_product['description']}
💰 Investment: {primary_product['price']}

Key Benefits:
"""
    
    for benefit in primary_product['benefits'][:3]:  # Show top 3 benefits
        message += f"  ✓ {benefit}\n"
    
    # Secondary product (brief mention)
    if len(products) > 1:
        secondary_product = products[1]
        message += f"\n💡 You may also like: {secondary_product['icon']} {secondary_product['name']} ({secondary_product['price']})"
    
    message += """

Would you like to hear more about this, or should I send you the details via email/SMS? 
(Or we can skip this and proceed directly to your sanction letter - totally up to you!)
"""
    
    return message


def log_cross_sell_interaction(product_id: str, customer_id: str, action: str):
    """
    Log cross-sell interaction for analytics.
    
    Args:
        product_id: ID of the product offered
        customer_id: Customer ID
        action: Action taken (offered, interested, declined, accepted)
    """
    # This would integrate with analytics tracker
    # For now, we'll just track in session state
    pass


def get_cross_sell_summary(products: List[Dict]) -> str:
    """
    Get a brief summary of recommended products for agent context.
    
    Args:
        products: List of recommended products
    
    Returns:
        str: Summary text
    """
    if not products:
        return "No cross-sell products recommended for this customer."
    
    summary = "🎁 CROSS-SELL RECOMMENDATIONS:\n"
    for idx, product in enumerate(products, 1):
        summary += f"  {idx}. {product['icon']} {product['name']} ({product['price']}) - Relevance: {product['relevance_score']:.0%}\n"
    
    return summary
