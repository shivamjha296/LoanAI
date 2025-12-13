"""
Emotional Intelligence & Sentiment Analysis Module (AI-Powered)
Uses Mistral AI to detect customer sentiment and provide adaptive response strategies
"""

import litellm
from typing import Dict, List
from datetime import datetime


# Use Mistral AI directly via litellm
def _call_mistral(prompt: str) -> str:
    """Call Mistral AI via litellm"""
    try:
        response = litellm.completion(
            model="mistral/mistral-large-2411",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Mistral API call failed: {e}")


def detect_sentiment(text: str, conversation_context: str = "") -> Dict:
    """
    AI-powered sentiment detection using Mistral AI.
    Analyzes customer emotion from their message with context awareness.
    
    Args:
        text: Customer's message text
        conversation_context: Recent conversation history for context
    
    Returns:
        dict: Sentiment analysis result with AI insights
    """
    try:
        # Build context line
        context_line = ""
        if conversation_context:
            context_line = f"RECENT CONVERSATION CONTEXT:\n{conversation_context}\n\n"
        
        # Smart sentiment detection prompt
        prompt = f"""Analyze the customer's emotional state from their message in a loan application conversation.

CUSTOMER MESSAGE: "{text}"

{context_line}Detect the PRIMARY emotion and provide a confidence score (0.0-1.0):

EMOTION TYPES:
1. EXCITEMENT - Positive, enthusiastic, ready to proceed, eager
2. CONFUSION - Unclear, needs explanation, doesn't understand concepts
3. HESITATION - Unsure, considering options, needs reassurance
4. FRUSTRATION - Annoyed, impatient, experiencing difficulty
5. TRUST - Comfortable, confident, accepting information
6. URGENCY - Time-sensitive, needs quick resolution, deadline pressure
7. PRICE_CONCERN - Worried about cost, budget constraints, rates too high
8. NEUTRAL - Calm, factual, no strong emotion detected

Respond in this EXACT format (no extra text):
SENTIMENT: [one of the 8 emotions above]
CONFIDENCE: [0.0-1.0]
SCORE: [+0.8 for positive, -0.6 for negative, 0.0 for neutral]
REASONING: [one brief sentence explaining why]

Example:
SENTIMENT: CONFUSION
CONFIDENCE: 0.75
SCORE: -0.3
REASONING: Customer is asking clarifying questions and using phrases like "I don't understand"

Now analyze the customer message above:"""

        # Get Mistral AI response
        result_text = _call_mistral(prompt).strip()
        
        # Parse AI response
        sentiment_type = "NEUTRAL"
        confidence = 0.5
        score = 0.0
        reasoning = "No strong emotion detected"
        
        for line in result_text.split('\n'):
            line = line.strip()
            if line.startswith('SENTIMENT:'):
                sentiment_type = line.split(':', 1)[1].strip().upper()
            elif line.startswith('CONFIDENCE:'):
                try:
                    confidence = float(line.split(':', 1)[1].strip())
                except:
                    confidence = 0.7
            elif line.startswith('SCORE:'):
                try:
                    score = float(line.split(':', 1)[1].strip())
                except:
                    score = 0.0
            elif line.startswith('REASONING:'):
                reasoning = line.split(':', 1)[1].strip()
        
        # Map to emoji
        emoji_map = {
            "EXCITEMENT": "😊",
            "CONFUSION": "😕",
            "HESITATION": "🤔",
            "FRUSTRATION": "😤",
            "TRUST": "👍",
            "URGENCY": "⚡",
            "PRICE_CONCERN": "💰",
            "NEUTRAL": "😐"
        }
        
        return {
            "status": "detected",
            "primary_sentiment": sentiment_type,
            "sentiment_score": score,
            "confidence": confidence,
            "emoji": emoji_map.get(sentiment_type, "😐"),
            "reasoning": reasoning,
            "adaptive_strategy": get_adaptive_strategy(sentiment_type, text),
            "ai_powered": True
        }
        
    except Exception as e:
        # Fallback to neutral on error
        print(f"⚠️ Mistral AI sentiment detection failed: {e}")
        return {
            "status": "neutral",
            "primary_sentiment": "NEUTRAL",
            "sentiment_score": 0.0,
            "confidence": 0.5,
            "emoji": "😐",
            "reasoning": "AI unavailable - using neutral fallback",
            "adaptive_strategy": get_adaptive_strategy("NEUTRAL", text),
            "error": str(e)
        }


def get_adaptive_strategy(sentiment_type: str, customer_message: str = "") -> Dict:
    """
    AI-powered adaptive response strategy generation using Mistral AI.
    Creates context-aware response guidelines based on detected sentiment.
    
    Args:
        sentiment_type: The detected sentiment type
        customer_message: The actual customer message for context
    
    Returns:
        dict: Adaptive strategy with tone, pace, focus, and AI example
    """
    try:
        # Smart adaptive strategy prompt
        prompt = f"""You are an expert loan sales coach. The customer is feeling {sentiment_type}.

CUSTOMER MESSAGE: "{customer_message}"

Provide an adaptive response strategy for the loan agent:

EMOTION-SPECIFIC GUIDELINES:
- EXCITEMENT: Match energy, fast-track, celebrate momentum, minimize friction
- CONFUSION: Simplify language, use analogies, slow down, confirm understanding
- HESITATION: Reassure, provide social proof, address concerns, build confidence
- FRUSTRATION: Deep empathy, apologize if needed, offer escalation, simplify drastically
- TRUST: Professional confidence, reinforce credibility, transparent terms
- URGENCY: Acknowledge timeline, provide clear ETA, fast-track process
- PRICE_CONCERN: Show value comparison, break down costs, highlight savings
- NEUTRAL: Balanced professional, informative, build rapport

Respond in this EXACT format (no extra text):
TONE: [describe the emotional tone to use - max 4 words]
PACE: [FAST/MODERATE/SLOW]
FOCUS: [3 priorities separated by commas]
APPROACH: [Write ONE short example sentence (15-25 words) showing how to respond]

Example:
TONE: Patient & Educational
PACE: SLOW
FOCUS: Simplify terms, Use analogies, Confirm understanding
APPROACH: Let me explain EMI simply - it's like paying for Netflix monthly, but for your loan.

Now create the strategy for {sentiment_type}:"""

        # Get Mistral AI response via LiteLlm
        response = _sentiment_mod
        result_text = _call_mistral(prompt)
        # Parse AI response
        strategy = {
            "tone": "Professional & Friendly",
            "pace": "MODERATE",
            "focus": "Build rapport, Provide information, Move forward",
            "approach": "Happy to help! Let me guide you through the next steps.",
            "ai_generated": True
        }
        
        for line in result_text.split('\n'):
            line = line.strip()
            if line.startswith('TONE:'):
                strategy["tone"] = line.split(':', 1)[1].strip()
            elif line.startswith('PACE:'):
                strategy["pace"] = line.split(':', 1)[1].strip().upper()
                # Validate pace
                if strategy["pace"] not in ["FAST", "MODERATE", "SLOW"]:
                    strategy["pace"] = "MODERATE"
            elif line.startswith('FOCUS:'):
                focus_text = line.split(':', 1)[1].strip()
                strategy["focus"] = focus_text
            elif line.startswith('APPROACH:'):
                strategy["approach"] = line.split(':', 1)[1].strip()
        
        return strategy
        
    except Exception as e:
        # Fallback strategy
        print(f"⚠️ Mistral AI strategy generation failed: {e}")
        return {
            "tone": "Professional & Friendly",
            "pace": "MODERATE",
            "focus": "Build rapport, Provide information, Move forward",
            "approach": "I'm here to help! Let me know if you have any questions.",
            "error": str(e)
        }


def get_sentiment_context_for_agent(sentiment_result: Dict) -> str:
    """
    Generates formatted sentiment context for agent prompt with Mistral AI insights.
    
    Args:
        sentiment_result: Result from detect_sentiment()
    
    Returns:
        str: Formatted context for agent instruction
    """
    if sentiment_result["status"] == "neutral":
        return "No strong sentiment detected. Maintain professional, balanced tone."
    
    strategy = sentiment_result["adaptive_strategy"]
    
    context = f"""
🎭 MISTRAL AI EMOTIONAL INTELLIGENCE DETECTED:
Customer Sentiment: {sentiment_result['emoji']} {sentiment_result['primary_sentiment']}
Confidence: {sentiment_result['confidence']:.0%} | Score: {sentiment_result['sentiment_score']:.2f}
AI Reasoning: {sentiment_result.get('reasoning', 'N/A')}

🤖 MISTRAL AI-POWERED ADAPTIVE STRATEGY:
Tone: {strategy['tone']}
Response Pace: {strategy['pace']}
Focus On: {strategy['focus']}

💡 AI EXAMPLE APPROACH:
"{strategy['approach']}"

⚡ INSTRUCTION: Apply this Mistral AI-generated strategy in your next response!
"""
    
    return context


def track_sentiment_evolution(conversation_history: List[Dict]) -> Dict:
    """
    Tracks how sentiment evolves throughout a conversation.
    
    Args:
        conversation_history: List of messages with sentiment data
    
    Returns:
        dict: Sentiment trend analysis
    """
    if not conversation_history:
        return {
            "trend": "NEUTRAL",
            "improvement": 0.0,
            "risk_level": "LOW"
        }
    
    # Extract sentiment scores
    scores = []
    for msg in conversation_history:
        if isinstance(msg, dict) and "sentiment" in msg:
            sentiment = msg["sentiment"]
            if isinstance(sentiment, dict) and "sentiment_score" in sentiment:
                scores.append(sentiment["sentiment_score"])
    
    if len(scores) < 2:
        latest_score = scores[0] if scores else 0.0
        risk_level = "CRITICAL" if latest_score < -0.5 else ("HIGH" if latest_score < -0.3 else "LOW")
        return {
            "trend": "NEUTRAL",
            "improvement": 0.0,
            "risk_level": risk_level,
            "latest_score": latest_score
        }
    
    # Calculate trend
    first_half_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
    second_half_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
    
    improvement = second_half_avg - first_half_avg
    
    # Determine trend
    if improvement > 0.2:
        trend = "IMPROVING"
        risk_level = "LOW"
    elif improvement < -0.2:
        trend = "DECLINING"
        risk_level = "HIGH"
    else:
        trend = "STABLE"
        risk_level = "MEDIUM"
    
    # Latest sentiment determines immediate risk
    latest_score = scores[-1]
    if latest_score < -0.5:
        risk_level = "CRITICAL"
    elif latest_score < -0.3:
        risk_level = "HIGH"
    
    return {
        "trend": trend,
        "improvement": improvement,
        "risk_level": risk_level,
        "latest_score": latest_score,
        "average_score": sum(scores) / len(scores)
    }
