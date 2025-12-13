"""
Persuasion Strategy Engine
Selects and applies sales strategies based on customer profile and psychology
"""

# Customer segmentation based on behavior and profile
CUSTOMER_PROFILES = {
    "FIRST_TIME_CAUTIOUS": {
        "description": "First-time borrower, risk-averse, needs education",
        "strategy": "EDUCATIONAL",
        "tone": "warm_patient_educational",
        "trust_building_priority": "HIGH",
        "pace": "SLOW",
        "focus_areas": ["how_it_works", "safety", "transparency", "step_by_step"]
    },
    "REPEAT_LOYAL": {
        "description": "Existing customer with good payment history",
        "strategy": "UPGRADE_APPRECIATION",
        "tone": "appreciative_privileged",
        "trust_building_priority": "LOW",  # Already established
        "pace": "MEDIUM",
        "focus_areas": ["loyalty_benefits", "exclusive_rates", "fast_approval", "relationship_value"]
    },
    "HIGH_CREDIT_AFFLUENT": {
        "description": "High credit score, high income, premium segment",
        "strategy": "PREMIUM_OFFERING",
        "tone": "confident_professional",
        "trust_building_priority": "MEDIUM",
        "pace": "FAST",
        "focus_areas": ["best_rates", "higher_limits", "premium_service", "exclusive_features"]
    },
    "BUDGET_CONSCIOUS": {
        "description": "Moderate income, EMI-sensitive, value-focused",
        "strategy": "EMI_FOCUSED",
        "tone": "practical_empathetic",
        "trust_building_priority": "MEDIUM",
        "pace": "MEDIUM",
        "focus_areas": ["affordable_emi", "flexible_tenure", "no_hidden_costs", "value_for_money"]
    },
    "SKEPTICAL_RESEARCHER": {
        "description": "Rate shopping, multiple visits, comparison-focused",
        "strategy": "TRANSPARENT_FACTUAL",
        "tone": "transparent_data_driven",
        "trust_building_priority": "HIGH",
        "pace": "MEDIUM",
        "focus_areas": ["rate_comparison", "total_cost", "terms_clarity", "reviews_ratings"]
    },
    "URGENT_NEED": {
        "description": "Emergency requirement, time-sensitive",
        "strategy": "SPEED_ASSURANCE",
        "tone": "empathetic_efficient",
        "trust_building_priority": "MEDIUM",
        "pace": "FAST",
        "focus_areas": ["instant_approval", "24hr_disbursal", "minimal_documentation", "emergency_support"]
    }
}


# Persuasion techniques mapped to customer profiles
PERSUASION_TECHNIQUES = {
    "EDUCATIONAL": {
        "opening_style": "consultative",
        "key_phrases": [
            "Let me explain how this works...",
            "Here's what happens step by step...",
            "There's no pressure - let me walk you through the process...",
            "Many first-time borrowers find this helpful...",
            "Feel free to ask any questions you have..."
        ],
        "proof_elements": ["customer_testimonials", "regulatory_compliance", "security_features"],
        "objection_approach": "educate_then_reassure",
        "close_style": "soft_permission"
    },
    "UPGRADE_APPRECIATION": {
        "opening_style": "relationship_focused",
        "key_phrases": [
            "As a valued customer for [X] years, you're pre-approved for...",
            "We appreciate your excellent payment history...",
            "You qualify for our best rates - exclusively for loyal customers...",
            "Your relationship with us makes you eligible for...",
            "Thank you for your continued trust in Tata Capital..."
        ],
        "proof_elements": ["relationship_history", "loyalty_benefits", "exclusive_access"],
        "objection_approach": "reinforce_relationship_value",
        "close_style": "exclusive_opportunity"
    },
    "PREMIUM_OFFERING": {
        "opening_style": "premium_concierge",
        "key_phrases": [
            "You qualify for our premium offering with the best rates...",
            "Based on your excellent credit profile...",
            "As a high-value customer, you have access to...",
            "We can offer you up to ₹35 lakhs at just 10.99%...",
            "Dedicated relationship manager for faster processing..."
        ],
        "proof_elements": ["credit_score_benefits", "rate_advantage", "higher_limits"],
        "objection_approach": "premium_service_value",
        "close_style": "confident_recommendation"
    },
    "EMI_FOCUSED": {
        "opening_style": "affordability_first",
        "key_phrases": [
            "Just ₹8,500/month - less than your dining and entertainment budget...",
            "Flexible EMI options starting as low as...",
            "You can choose a comfortable EMI that fits your budget...",
            "Let's find a monthly payment that works for you...",
            "Zero prepayment charges - pay off early if your situation improves..."
        ],
        "proof_elements": ["emi_breakdown", "total_cost_transparency", "flexibility_options"],
        "objection_approach": "break_down_affordability",
        "close_style": "comfort_oriented"
    },
    "TRANSPARENT_FACTUAL": {
        "opening_style": "data_driven",
        "key_phrases": [
            "Here's the complete breakdown with zero hidden charges...",
            "Let me show you the exact numbers...",
            "Our interest rate is 10.99% compared to market average of 13-15%...",
            "Total cost of loan: ₹X (Principal) + ₹Y (Interest) = ₹Z...",
            "Independent rating: 4.5/5 stars from 50,000+ customers..."
        ],
        "proof_elements": ["rate_comparison_chart", "total_cost_breakdown", "customer_ratings"],
        "objection_approach": "provide_detailed_facts",
        "close_style": "informed_decision"
    },
    "SPEED_ASSURANCE": {
        "opening_style": "empathetic_urgent",
        "key_phrases": [
            "I understand this is urgent - we can approve within 2 hours...",
            "Funds in your account within 24 hours...",
            "Minimal documentation for medical emergencies...",
            "Let me fast-track your application...",
            "We're here to help in your time of need..."
        ],
        "proof_elements": ["speed_metrics", "emergency_success_stories", "support_availability"],
        "objection_approach": "emphasize_speed_support",
        "close_style": "immediate_action"
    }
}


def determine_customer_profile(customer_data: dict, campaign_data: dict, credit_score: int) -> str:
    """
    Analyze customer data and determine the best profile match
    
    Args:
        customer_data: Customer information from database
        campaign_data: Campaign and journey data
        credit_score: Customer's credit score
    
    Returns:
        Profile key from CUSTOMER_PROFILES
    """
    customer_type = campaign_data.get("customer_type", "FIRST_TIME")
    journey = campaign_data.get("journey", {})
    intent = campaign_data.get("intent", "GENERAL_PURPOSE")
    urgency = campaign_data.get("urgency_level", "LOW")
    monthly_salary = customer_data.get("monthly_salary", 50000)
    
    # Urgent need profile
    if urgency == "HIGH" or intent in ["URGENT_MEDICAL"]:
        return "URGENT_NEED"
    
    # Repeat customer with good history
    if customer_type == "REPEAT_CUSTOMER":
        payment_history = journey.get("payment_history")
        if payment_history in ["EXCELLENT", "GOOD"]:
            return "REPEAT_LOYAL"
    
    # High credit, high income → Premium
    if credit_score >= 800 and monthly_salary >= 100000:
        return "HIGH_CREDIT_AFFLUENT"
    
    # Budget conscious
    if monthly_salary < 50000:
        return "BUDGET_CONSCIOUS"
    
    # Rate shopping behavior
    if journey.get("visits_count", 1) > 3 or "compare" in journey.get("pages_viewed", []):
        return "SKEPTICAL_RESEARCHER"
    
    # First time borrower (default for new customers)
    if customer_type == "FIRST_TIME":
        return "FIRST_TIME_CAUTIOUS"
    
    # Fallback
    return "FIRST_TIME_CAUTIOUS"


def get_strategy_instructions(profile_key: str) -> dict:
    """Get the full strategy instructions for a customer profile"""
    profile = CUSTOMER_PROFILES.get(profile_key, CUSTOMER_PROFILES["FIRST_TIME_CAUTIOUS"])
    strategy = profile["strategy"]
    technique = PERSUASION_TECHNIQUES.get(strategy, PERSUASION_TECHNIQUES["EDUCATIONAL"])
    
    return {
        "profile": profile,
        "technique": technique,
        "profile_key": profile_key,
        "strategy_name": strategy
    }


def get_strategy_prompt(customer_data: dict, campaign_data: dict, credit_score: int) -> str:
    """
    Generate a comprehensive strategy prompt for the Master Agent
    
    Returns:
        Formatted prompt with strategy instructions
    """
    profile_key = determine_customer_profile(customer_data, campaign_data, credit_score)
    strategy = get_strategy_instructions(profile_key)
    
    profile = strategy["profile"]
    technique = strategy["technique"]
    
    prompt = f"""
**PERSUASION STRATEGY: {strategy['strategy_name']}**

**Customer Profile:** {profile['description']}

**Communication Guidelines:**
- **Tone:** {profile['tone'].replace('_', ' ').title()}
- **Pace:** {profile['pace']} - {"Move quickly to action" if profile['pace'] == 'FAST' else "Take time to build understanding" if profile['pace'] == 'SLOW' else "Balanced approach"}
- **Trust Building Priority:** {profile['trust_building_priority']}

**Opening Style:** {technique['opening_style'].replace('_', ' ').title()}

**Key Phrases to Use:**
{chr(10).join(f"- {phrase}" for phrase in technique['key_phrases'])}

**Focus Areas (in priority order):**
{chr(10).join(f"- {area.replace('_', ' ').title()}" for area in profile['focus_areas'])}

**Proof Elements to Emphasize:**
{chr(10).join(f"- {element.replace('_', ' ').title()}" for element in technique['proof_elements'])}

**Objection Handling Approach:** {technique['objection_approach'].replace('_', ' ').title()}

**Closing Style:** {technique['close_style'].replace('_', ' ').title()}

**Remember:** This customer responds best to {profile['tone'].replace('_', ' ')} communication. 
Adjust your language and approach accordingly throughout the conversation.
"""
    
    return prompt.strip()
