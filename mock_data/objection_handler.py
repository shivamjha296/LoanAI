"""
Intelligent Objection Handling System
Diagnoses customer objections and provides strategic responses
"""

# Objection taxonomy with classification
OBJECTION_TYPES = {
    "INTEREST_RATE_HIGH": {
        "category": "PRICING",
        "severity": "HIGH",
        "common_phrases": [
            "interest rate seems high",
            "rate is too much",
            "expensive interest",
            "other banks offer lower",
            "can you reduce the rate"
        ],
        "root_cause": "Price sensitivity / Comparison shopping",
        "counter_strategies": ["market_comparison", "total_value_proposition", "rate_negotiation_path"]
    },
    "EMI_TOO_HIGH": {
        "category": "AFFORDABILITY",
        "severity": "HIGH",
        "common_phrases": [
            "emi is too high",
            "can't afford this much",
            "monthly payment too large",
            "emi burden",
            "looking for lower emi"
        ],
        "root_cause": "Budget constraints / Cash flow concerns",
        "counter_strategies": ["tenure_extension", "amount_reduction", "income_projection"]
    },
    "NO_IMMEDIATE_NEED": {
        "category": "URGENCY",
        "severity": "MEDIUM",
        "common_phrases": [
            "don't need right now",
            "just exploring",
            "not urgent",
            "maybe later",
            "just checking options"
        ],
        "root_cause": "Lack of urgency / Information gathering",
        "counter_strategies": ["create_urgency", "opportunity_cost", "pre_approval_benefit"]
    },
    "REPAYMENT_FEAR": {
        "category": "RISK",
        "severity": "HIGH",
        "common_phrases": [
            "what if I can't repay",
            "worried about default",
            "job security concern",
            "what happens if I miss emi",
            "scared of taking loan"
        ],
        "root_cause": "Fear of financial stress / Job insecurity",
        "counter_strategies": ["flexible_options", "insurance_option", "success_stories"]
    },
    "HIDDEN_CHARGES_CONCERN": {
        "category": "TRUST",
        "severity": "MEDIUM",
        "common_phrases": [
            "any hidden charges",
            "what are all the fees",
            "total cost unclear",
            "surprise charges",
            "processing fee seems high"
        ],
        "root_cause": "Trust issues / Transparency concerns",
        "counter_strategies": ["complete_transparency", "charge_breakdown", "written_guarantee"]
    },
    "DOCUMENTATION_HASSLE": {
        "category": "CONVENIENCE",
        "severity": "LOW",
        "common_phrases": [
            "too many documents",
            "paperwork is too much",
            "don't have time",
            "complicated process",
            "too much hassle"
        ],
        "root_cause": "Time constraints / Process complexity perception",
        "counter_strategies": ["minimal_docs_pitch", "digital_process", "assisted_support"]
    },
    "CREDIT_SCORE_WORRY": {
        "category": "ELIGIBILITY",
        "severity": "MEDIUM",
        "common_phrases": [
            "my cibil is low",
            "credit score not good",
            "will I get approved",
            "had defaults before",
            "worried about rejection"
        ],
        "root_cause": "Credit history concerns / Fear of rejection",
        "counter_strategies": ["pre_check_assurance", "alternate_solutions", "improvement_plan"]
    },
    "BETTER_OFFER_ELSEWHERE": {
        "category": "COMPETITION",
        "severity": "HIGH",
        "common_phrases": [
            "other bank offered better",
            "competitor has lower rate",
            "got better deal elsewhere",
            "xyz bank is cheaper",
            "friend got better offer"
        ],
        "root_cause": "Competitive offer / Price comparison",
        "counter_strategies": ["total_cost_comparison", "service_differentiation", "match_or_beat"]
    },
    "FAMILY_CONSULTATION": {
        "category": "DECISION_DELAY",
        "severity": "LOW",
        "common_phrases": [
            "need to ask my wife",
            "will discuss with family",
            "let me check with spouse",
            "need parents approval",
            "have to consult partner"
        ],
        "root_cause": "Joint decision making / Need for consensus",
        "counter_strategies": ["include_family_session", "information_packet", "extended_validity"]
    },
    "PROCESSING_TIME_CONCERN": {
        "category": "SPEED",
        "severity": "MEDIUM",
        "common_phrases": [
            "how long will it take",
            "need money urgently",
            "can't wait too long",
            "when will I get funds",
            "is it fast"
        ],
        "root_cause": "Urgency / Time sensitivity",
        "counter_strategies": ["speed_guarantee", "timeline_clarity", "priority_processing"]
    }
}


# Counter-strategies with specific responses
COUNTER_STRATEGIES = {
    "market_comparison": {
        "name": "Market Rate Comparison",
        "approach": "Show that your rates are competitive",
        "response_template": """
I understand your concern about the interest rate. Let me share some context:

**Market Comparison:**
- Bank Personal Loans: 13-15% p.a.
- Credit Card EMI: 18-24% p.a.
- Private Financiers: 16-20% p.a.
- Tata Capital: 10.99-11.99% p.a. ✓

**What makes our rate better:**
1. We're actually 2-3% LOWER than most banks
2. No hidden charges - this is your final rate
3. For customers with 750+ credit score, we offer 10.99%
4. Pre-payment allowed with minimal charges

**Total Savings Example:**
- ₹5L loan at our 11.99% = Total interest ₹1,85,000
- Same loan at bank's 14% = Total interest ₹2,45,000
- You SAVE ₹60,000 with us!

Would you like me to show you the exact comparison for your loan amount?
""",
        "success_rate": 0.68
    },
    
    "tenure_extension": {
        "name": "Extend Tenure to Reduce EMI",
        "approach": "Offer longer tenure to make EMI affordable",
        "response_template": """
I completely understand - let's find an EMI that fits comfortably in your budget.

**Here's a simple solution:**

Your Current Option:
- ₹5,00,000 at 48 months = ₹12,500/month

**Adjusted Options:**
- ₹5,00,000 at 60 months = ₹10,800/month (₹1,700 less!)
- ₹5,00,000 at 72 months = ₹9,400/month (₹3,100 less!)

**The best part:**
- You can prepay anytime to reduce tenure later
- After 12 months: 25% prepayment with ZERO charges
- If your income increases, pay off faster

Which monthly amount feels comfortable for your budget?
""",
        "success_rate": 0.75
    },
    
    "create_urgency": {
        "name": "Create Urgency",
        "approach": "Highlight time-sensitive benefits",
        "response_template": """
I appreciate you being thoughtful about this decision! Let me share why many customers who "wait" later regret it:

**Time-Sensitive Benefits:**
1. **Pre-approved offer expires in 48 hours** - Rate locked at 11.99%
2. **Interest rates are rising** - RBI might increase rates next quarter
3. **Your credit limit might reduce** - Pre-approved amount is highest now

**Opportunity Cost:**
- Planning that home renovation? Delaying 3 months = Property prices up 5%
- Medical procedure? Early treatment = Better outcomes
- Wedding expenses? Last-minute arrangements = 30% more expensive

**What our customers say:**
"I wish I had taken the loan when first offered - same bank later charged me 13.5% instead of 11.99%" - Rajesh K.

**Smart approach:**
- Accept the offer now (locks your rate)
- Disburse when you need (valid for 30 days)
- Use it on your terms

Would you like to lock this rate before it expires?
""",
        "success_rate": 0.52
    },
    
    "flexible_options": {
        "name": "Flexible Repayment Options",
        "approach": "Highlight safety nets and flexibility",
        "response_template": """
I'm glad you're thinking about this - it shows you're a responsible borrower! Let me share the safety features we have:

**If You Face Difficulties:**

1. **Moratorium Period (Medical/Job Loss):**
   - Apply for 3-6 month EMI pause
   - Tenure extends, but no penalty
   - Available in genuine emergencies

2. **Tenure Modification:**
   - Extend tenure to reduce EMI burden
   - Can be done after 12 EMIs

3. **Part Payment Option:**
   - Pay lump sum to reduce burden anytime
   - First 25% part-payment = Zero charges

4. **Insurance Cover (Optional):**
   - Job Loss Protection: Covers EMI for 6 months
   - Critical Illness: Waives outstanding amount
   - Death Coverage: Family not liable
   - Premium: Just ₹500/month for ₹5L loan

**Success Story:**
"I lost my job in month 8. Tata Capital gave me 3-month moratorium. Found new job, resumed payments. No harassment, no penalties." - Amit P.

**Our Philosophy:**
We want you to succeed, not default. Your success = Our success.

Would you like to add the insurance cover for extra peace of mind?
""",
        "success_rate": 0.71
    },
    
    "complete_transparency": {
        "name": "Complete Transparency Breakdown",
        "approach": "Provide exhaustive cost breakdown",
        "response_template": """
Excellent question! I appreciate you asking this. Let me give you the COMPLETE breakdown - nothing hidden:

**TOTAL COST BREAKDOWN FOR ₹5,00,000 LOAN:**

**One-Time Charges:**
1. Processing Fee: ₹17,500 (3.5% of loan)
2. GST on Processing: ₹3,150 (18% of processing fee)
3. Stamp Duty: ~₹500 (varies by state)
**Total One-Time: ₹21,150**

**Monthly Charges:**
1. EMI: ₹10,800 (Principal + Interest)
**Total Monthly: ₹10,800 ONLY**

**Zero Charge for:**
- Application ✓
- Documentation ✓
- Disbursement ✓
- Account maintenance ✓
- First 25% prepayment (after 12 months) ✓

**Optional Charges (Only if you use):**
- Late payment: ₹500 (avoidable)
- Bounce charge: ₹500 (avoidable)
- NOC after closure: ₹500 (one-time)

**WRITTEN GUARANTEE:**
I will send you a signed cost sheet. If ANY charge appears that's not mentioned here, we'll WAIVE it completely.

**Total You Repay:**
- ₹5,00,000 (Principal) + ₹1,48,000 (Interest) + ₹21,150 (Fees) = ₹6,69,150

That's it. No surprises. No hidden clauses.

Can I email you this detailed breakdown right now?
""",
        "success_rate": 0.82
    },
    
    "minimal_docs_pitch": {
        "name": "Minimal Documentation Process",
        "approach": "Simplify process perception",
        "response_template": """
I hear you - nobody likes paperwork! Here's the good news:

**For Pre-Approved Customers (That's You!):**

**All You Need:**
1. PAN Card (photo)
2. Aadhaar Card (e-KYC online)
3. Last 3 months' salary slips OR bank statement
4. Selfie for verification

**That's it! Just 4 things.**

**How We Make it Easy:**
- Upload photos from phone (WhatsApp/Email)
- Our team helps you if stuck
- Digital signature (no physical paperwork)
- Entire process on video call if needed

**Timeline:**
- Document upload: 15 minutes
- Verification: 2 hours
- Approval: Same day
- Funds in account: 24 hours

**We'll Help You:**
- Dedicated assistant (Mr. Soham Patel)
- Video call support
- WhatsApp reminders
- Document checklist sent to you

**Customer Experience:**
"I was dreading the paperwork. Turned out I just clicked 4 photos on my phone and was done in 10 minutes!" - Priya S.

Want me to send you the document checklist on WhatsApp right now?
""",
        "success_rate": 0.77
    },
    
    "total_cost_comparison": {
        "name": "Total Cost vs Service Comparison",
        "approach": "Compete on total value, not just price",
        "response_template": """
I'm glad you're comparing - that's smart! But let me show you what often gets missed in "cheaper" offers:

**TOTAL COST COMPARISON:**

**Competitor Offer (e.g., XYZ Bank):**
- Interest Rate: 11.5% (vs our 11.99%)
- Processing Fee: 2% (vs our 3.5%)
- Hidden Charges: ₹5,000-10,000
- Prepayment Charges: 5% always (vs our 0% for 25%)
- Approval Time: 5-7 days (vs our 24 hours)
- Customer Service: Call center (vs dedicated RM)

**REAL TOTAL COST (₹5L loan, 5 years):**

XYZ Bank:
- Interest: ₹1,82,000
- Processing: ₹10,000 + ₹2,000 hidden charges
- Prepayment fee (if you close early): ₹15,000
- **TOTAL: ₹2,09,000**

Tata Capital:
- Interest: ₹1,85,000
- Processing: ₹17,500 + ₹3,150 GST
- Prepayment fee: ₹0 (25% free)
- **TOTAL: ₹2,05,650**

**You SAVE ₹3,350 + Get Better Service!**

**What You Get Extra with Us:**
1. 24-hour approval (vs 5-7 days)
2. Dedicated relationship manager
3. Top-up facility at same rate
4. Part-prepayment flexibility
5. Moratorium in emergencies

**The Question:**
Do you want the "cheapest-looking" offer, or the best overall value?

Let me send you this comparison sheet. Many customers switch FROM those banks TO us!
""",
        "success_rate": 0.73
    },
    
    "speed_guarantee": {
        "name": "Speed & Timeline Guarantee",
        "approach": "Provide clear, fast timeline",
        "response_template": """
Great question! Let me give you the EXACT timeline:

**TATA CAPITAL SPEED GUARANTEE:**

**TODAY (Application):**
- Fill basic details: 10 minutes
- Upload 4 documents: 15 minutes
- **Application submitted: 25 minutes total**

**WITHIN 2 HOURS:**
- Credit check completed
- Eligibility confirmed
- **Approval/Pre-approval: 2 hours**

**SAME DAY:**
- Sanction letter generated
- Rate locked
- **Offer confirmed: 8 hours max**

**NEXT DAY:**
- Final verification call
- Agreement signing (digital)
- **Funds disbursed: 24 hours**

**For Medical Emergencies:**
- Express processing: 4-6 hours total
- Weekend support available
- Direct hospital payment option

**MONEY-BACK GUARANTEE:**
If we don't disburse within 24 hours (for complete applications), we'll waive your processing fee!

**Live Tracking:**
- SMS updates at each stage
- Track on mobile app
- Call/WhatsApp your RM anytime

**Ready to start your 24-hour countdown?**
""",
        "success_rate": 0.79
    }
}


def detect_objection(customer_message: str) -> list:
    """
    Detect objections in customer message using keyword matching
    
    Args:
        customer_message: The customer's message text
    
    Returns:
        List of detected objection types with confidence scores
    """
    customer_message_lower = customer_message.lower()
    detected = []
    
    for objection_type, details in OBJECTION_TYPES.items():
        confidence = 0
        matched_phrases = []
        
        for phrase in details["common_phrases"]:
            if phrase in customer_message_lower:
                confidence += 1
                matched_phrases.append(phrase)
        
        if confidence > 0:
            detected.append({
                "type": objection_type,
                "category": details["category"],
                "severity": details["severity"],
                "confidence": min(confidence / len(details["common_phrases"]), 1.0),
                "matched_phrases": matched_phrases,
                "counter_strategies": details["counter_strategies"]
            })
    
    # Sort by confidence
    detected.sort(key=lambda x: x["confidence"], reverse=True)
    
    return detected


def get_objection_response(objection_type: str, customer_data: dict) -> dict:
    """
    Get the best counter-strategy for an objection
    
    Args:
        objection_type: The type of objection detected
        customer_data: Customer profile for personalization
    
    Returns:
        Counter-strategy details with response template
    """
    objection = OBJECTION_TYPES.get(objection_type)
    if not objection:
        return None
    
    # Get primary counter-strategy
    primary_strategy = objection["counter_strategies"][0]
    strategy = COUNTER_STRATEGIES.get(primary_strategy)
    
    if not strategy:
        return None
    
    return {
        "objection_type": objection_type,
        "objection_category": objection["category"],
        "severity": objection["severity"],
        "strategy_name": strategy["name"],
        "approach": strategy["approach"],
        "response_template": strategy["response_template"],
        "success_rate": strategy["success_rate"],
        "alternate_strategies": objection["counter_strategies"][1:]
    }


def get_objection_handling_prompt(detected_objections: list) -> str:
    """
    Generate a prompt for handling detected objections
    
    Args:
        detected_objections: List of detected objections
    
    Returns:
        Formatted prompt with objection handling instructions
    """
    if not detected_objections:
        return ""
    
    primary_objection = detected_objections[0]
    objection_type = primary_objection["type"]
    
    response_data = get_objection_response(objection_type, {})
    
    if not response_data:
        return ""
    
    prompt = f"""
**⚠️ OBJECTION DETECTED: {objection_type.replace('_', ' ').title()}**

**Objection Category:** {response_data['objection_category']}
**Severity:** {response_data['severity']}
**Confidence:** {primary_objection['confidence']:.0%}

**Counter-Strategy:** {response_data['strategy_name']}
**Approach:** {response_data['approach']}
**Historical Success Rate:** {response_data['success_rate']:.0%}

**Recommended Response:**
{response_data['response_template']}

**Alternate Strategies (if primary doesn't work):**
{chr(10).join(f"- {s.replace('_', ' ').title()}" for s in response_data['alternate_strategies'])}

**Handling Tips:**
1. Acknowledge the concern empathetically
2. Use the response template as a guide (personalize it)
3. Provide data/proof to support your counter-argument
4. End with a clarifying question to move forward
"""
    
    return prompt.strip()
