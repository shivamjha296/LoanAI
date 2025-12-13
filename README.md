# 🏦 BFSI Personal Loan Chatbot - Tata Capital Digital Sales Assistant

A highly intelligent multi-agent AI system for automating personal loan sales with **Pre-Conversation Intelligence**, **Persuasion Strategy Engine**, and **Real-time Objection Handling**. This solution simulates a human-like sales process using an Agentic AI approach with a Master Agent orchestrating multiple Worker Agents.

## 🌟 **NEW: Advanced Intelligence Features**

### ⚡ **Parallel Agentic Processing**
**Smart background data loading** reduces total approval time from 3-4 minutes to under 1 minute:

**Timeline Comparison:**

**Before (Sequential):**
```
T=0s:  Customer starts chat
T=10s: Sales Agent shows offers
T=20s: Customer agrees → Start verification
T=30s: Fetch KYC data...
T=40s: Verification complete → Start underwriting
T=50s: Fetch credit score...
T=60s: Credit check complete → Approval
Total: ~60 seconds of data fetching
```

**After (Parallel):**
```
T=0s:  Customer starts chat + Background: Pre-fetch KYC & Credit Score ⚡
T=5s:  Sales Agent shows offers (data already loading)
T=10s: Customer agrees → Verification: INSTANT (pre-fetched) ✓
T=15s: Underwriting: INSTANT (pre-fetched) ✓
T=20s: Approval decision ready!
Total: ~20 seconds (3× faster!)
```

**How It Works:**
1. **Pre-loading Phase**: When customer is selected, system immediately fetches KYC data and credit score in background
2. **Smart Caching**: Data stored in session state with `_prefetched_kyc` and `_prefetched_credit` flags
3. **Instant Retrieval**: When Verification/Underwriting agents need data, they use cached version (0ms vs 10-15s)
4. **Graceful Fallback**: If pre-fetch fails, agents fetch normally (no functionality loss)

**Benefits:**
- ✅ 3× faster loan approvals
- ✅ Better customer experience (no waiting)
- ✅ Higher conversion rates (reduced drop-off)
- ✅ Scalable architecture (ready for real async APIs)

---

### 🧠 **Smart AI-Driven Persuasion**
**Replaced hard-coded strategies** with intelligent LLM-based adaptation:

**Old Approach:**
- Pre-defined customer profiles (FIRST_TIME_CAUTIOUS, REPEAT_LOYAL, etc.)
- Rigid scripts and templates
- Limited flexibility

**New Approach:**
- **Dynamic Context Analysis**: AI receives rich customer context (credit score, income, campaign source, urgency, history)
- **Real-time Adaptation**: LLM intelligently adjusts tone, language, and approach based on conversation flow
- **Smart Rules**: AI follows guidelines like:
  - High urgency → "2-hour approval, 24-hour funds"
  - Repeat customer → "Valued for X years, exclusive offer"
  - Budget-conscious → "Just ₹8,500/month EMI"
  - First-time → Educational, patient tone

**Example Smart Context:**
```
CUSTOMER CONTEXT FOR INTELLIGENT ADAPTATION:
- Credit Score: 820 (Excellent)
- Income: ₹1,25,000/month (High)
- Campaign: Email Marketing - existing customer top-up offer
- Intent: ADDITIONAL_FUNDS
- Urgency: LOW
- Customer Type: REPEAT_CUSTOMER
- Payment History: EXCELLENT

ADAPT YOUR APPROACH INTELLIGENTLY:
→ Show appreciation ("valued customer for 2 years")
→ Highlight premium rates ("your 820 score = 10.99% best rate")
→ Create gentle urgency ("exclusive offer expires in 120 hours")
```

**Benefits:**
- ✅ More natural, human-like conversations
- ✅ Better personalization without rigid templates
- ✅ Easier to maintain (no complex profile logic)
- ✅ Adapts to edge cases automatically

---

### 💚 **Emotional Intelligence & Sentiment Adaptation**
**AI-powered sentiment analysis** using **Mistral AI** detects customer emotions in real-time:

**Powered by Mistral AI:**
- **Sentiment Detection**: Analyzes customer message + conversation context
- **Adaptive Strategy**: Generates tone, pace, focus, and example response
- **Context-Aware**: Uses last 3 messages for better emotional understanding
- **No Hard-Coding**: 100% AI-driven, adapts to nuanced expressions

**8 Emotions Detected:**
- 😊 **EXCITEMENT** → Fast-track, match energy
- 😕 **CONFUSION** → Simplify, slow down
- 🤔 **HESITATION** → Reassure, provide proof
- 😤 **FRUSTRATION** → Deep empathy, escalation
- 👍 **TRUST** → Reinforce credibility
- ⚡ **URGENCY** → Emphasize speed
- 💰 **PRICE_CONCERN** → Show value
- 😐 **NEUTRAL** → Professional friendly

**Example:**
```
User: "This is getting complicated..."
🤖 Mistral Sentiment: 😕 CONFUSION (Confidence: 75%)
AI Reasoning: Customer expressing difficulty understanding

Adaptive Strategy:
- Tone: Patient & Educational
- Pace: SLOW
- Focus: Simplify terms, Use analogies
- AI Example: "Let me explain EMI simply - like Netflix monthly"
```

---

### 📈 **Self-Improving Feedback Loop**
**Automatic performance tracking** with week-over-week analytics:

**Metrics Tracked:**
- Conversion rates per strategy
- Drop-off points analysis
- Objection resolution rates
- Time to decision
- Sentiment trends

**Dashboard Command:**
```bash
# Type 'dashboard' in chat to view:
📈 PERFORMANCE DASHBOARD
Week     Conversations  Approvals  Conv. Rate  Objections
2025-W49      15           8        53.3%         12
2025-W50      20          13        65.0%          8

Conversion Rate Change: +11.7% ↑
Efficiency Status: IMPROVING ✓
```

**Data Stored:** `analytics_data.json` (auto-created)

---

### 🎁 **Contextual Cross-Sell Engine**
**Smart product recommendations** after loan approval:

**5 Products:**
1. 🛡️ Loan Protection Insurance (₹150/month)
2. 💳 Premium Credit Card (₹0 fee)
3. 💰 Tax-Saving FD (7.5% p.a.)
4. 🏠 Home Loan (8.5% starting)
5. 📈 SIP (₹500/month minimum)

**Smart Recommendation:**
- Analyzes credit score, income, loan purpose
- Selects top 2 most relevant products
- Non-pushy: Offered AFTER approval
- Options: Learn more / Email / Skip

**Example:**
```
Congratulations on your ₹3L loan! 🎉
Based on your profile:

🛡️ Loan Protection Insurance (₹150/month)
- EMI coverage for job loss
- Critical illness waiver

💡 Also: 💳 Premium Credit Card (₹0 fee)

Interested or should I skip?
```

---

### 1. 🎯 Pre-Conversation Intelligence Layer
**Before the chat even starts**, the system analyzes:
- **Ad Source/Campaign**: Identifies how customer found us (Google Ads, Email, Referral, etc.)
- **Campaign Keyword**: "emergency medical loan" vs "home renovation loan" vs "wedding loan"
- **Customer Profile**: Loads from CRM - existing loans, payment history, previous interactions
- **Pre-computed Offers**: 3 ranked loan offers ready before first message
- **Contextualized Opening**: Personalized greeting based on customer history and intent

**Example Intelligence Output:**
```
🧠 AGENT INTELLIGENCE DASHBOARD
================================================================================

🎯 PRE-CONVERSATION INTELLIGENCE:
  Campaign Source: Email Marketing
  Campaign Keyword: existing customer top-up offer
  Customer Intent: ADDITIONAL_FUNDS
  Urgency Level: LOW
  Customer Type: 🌟 REPEAT_CUSTOMER
  Relationship Tenure: 2 years
  Payment History: EXCELLENT
  Current Loans: 1
  Offer Expires In: 120 hours

💡 AI-GENERATED OPENING:
  "Hi Rajesh! I'm Priya Sharma from Tata Capital. It's wonderful to see you 
   again! You've been a valued customer for 2 years with an excellent 
   repayment track record. I noticed you're interested in our exclusive 
   top-up loan offer..."
```

### 2. 🧠 Persuasion Strategy Engine
The system **intelligently adapts its sales approach** using AI-driven context analysis:

**Smart AI-Driven Approach:**
Instead of pre-defined profiles, the AI receives rich context and adapts in real-time:

| Context Factor | AI Adaptation Example |
|----------------|---------------------|
| **Urgent Medical Need** | "We understand the urgency. 2-hour approval, funds in 24 hours." |
| **Repeat Customer, Excellent History** | "As a valued customer for 2 years with perfect payments..." |
| **800+ Credit Score, High Income** | "Your excellent profile qualifies you for our premium 10.99% rate." |
| **Budget-Conscious (<₹50K)** | "Just ₹8,500/month - affordable EMI that fits your budget." |
| **Rate Shopper** | "Complete transparency: Save ₹60K vs banks." |
| **First-Time Borrower** | "Let me walk you through this step by step..." |

**How Smart Persuasion Works:**
1. System provides context: credit score category, income level, campaign source, intent, urgency, history
2. AI receives adaptation guidelines (not rigid scripts)
3. LLM intelligently adjusts tone, language, and approach based on conversation
4. Real-time flexibility handles edge cases automatically

**Example Context Provided to AI:**
```
CUSTOMER CONTEXT FOR INTELLIGENT ADAPTATION:
- Credit Score: 785 (Good) | Income: ₹60K/month (Medium)
- Campaign: Google Ads - home renovation
- Intent: HOME_IMPROVEMENT | Urgency: MEDIUM
- Customer Type: FIRST_TIME | Payment History: N/A

ADAPT INTELLIGENTLY:
→ First-time borrower → Educational, patient tone
→ Home renovation → Emphasize project timeline
→ Good credit → Competitive rates (11.5-12%)
→ Medium income → Focus on EMI affordability
```

**Benefits:**
- ✅ Natural conversations (no rigid scripts)
- ✅ Handles edge cases automatically  
- ✅ Easier to maintain and update
- ✅ More personalized responses

### 3. ⚠️ Intelligent Objection Handling System
**Real-time objection detection** with strategic counter-arguments:

**Common Objections Detected:**
- **"Interest rate seems high"** → Market comparison, total savings calculation
- **"EMI is too much"** → Tenure extension, flexible options, affordability breakdown
- **"I don't need right now"** → Urgency creation, opportunity cost, pre-approval benefits
- **"What if I can't repay?"** → Flexible repayment, insurance, payment holiday options
- **"Any hidden charges?"** → Complete transparency, written guarantee, charge breakdown
- **"Too much documentation"** → Minimal docs pitch (just 4 items), digital process
- **"My credit score is low"** → Pre-check assurance, alternate solutions
- **"Other banks offer better"** → Total cost comparison, service differentiation

**Example Objection Response:**
```
⚠️ Objection Detected: Interest Rate High (Confidence: 85%)

Counter-Strategy: Market Rate Comparison
Historical Success Rate: 68%

Response Template:
"I understand your concern. Let me share context:

Market Comparison:
- Bank Personal Loans: 13-15% p.a.
- Credit Card EMI: 18-24% p.a.
- Tata Capital: 10.99-11.99% p.a. ✓

Total Savings:
₹5L loan at our 11.99% = ₹1,85,000 interest
Same at bank's 14% = ₹2,45,000 interest
You SAVE ₹60,000 with us!"
```

## 📋 Problem Statement

The NBFC (Tata Capital) wants to improve its sales success rate for personal loans by using an AI-driven conversational approach. The solution simulates a human-like sales process where the Master Agent handles customer conversations, engages customers in a personalized manner, and collaborates with multiple Worker AI agents to complete the loan process.

## 🎯 Solution Overview

### Enhanced Architecture with Intelligence Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   🎯 PRE-CONVERSATION INTELLIGENCE                        │
│  Campaign Analysis | Customer Profiling | Offer Ranking | Intent Detection│
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    🧠 PERSUASION STRATEGY ENGINE                          │
│   Customer Segmentation | Tone Selection | Key Phrases | Proof Elements  │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         MASTER AGENT                                      │
│                  (Loan Master Agent - Orchestrator)                       │
│    • Manages conversation flow with intelligence                          │
│    • Applies persuasion strategies dynamically                            │
│    • Coordinates worker agents                                            │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  SALES AGENT  │   │ VERIFICATION  │   │ UNDERWRITING  │
│               │   │    AGENT      │   │    AGENT      │
│ • Loan offers │   │ • KYC check   │   │ • Credit score│
│ • EMI calc    │   │ • Phone/Addr  │   │ • Eligibility │
│ • Negotiate   │   │ • Documents   │   │ • Approve/    │
│ • Initiate    │   │               │   │   Reject      │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    ┌───────────────┐
                    │   SANCTION    │
                    │ LETTER AGENT  │
                    │               │
                    │ • Generate PDF│
                    │ • Send letter │
                    │ • Acceptance  │
                    └───────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  ⚠️ REAL-TIME OBJECTION HANDLER                          │
│   Detects objections | Provides counter-strategies | Tracks success rates│
└─────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### Master Agent (Orchestrator) - **Now with Intelligence**
- **Pre-loads customer context** before conversation starts
- **Applies persuasion strategies** based on customer profile
- **Detects and handles objections** in real-time
- Ensures smooth handoffs between agents
- **Human-like persona**: Ms. Priya Sharma - Relationship Manager

### Worker Agents

#### 1. Sales Agent - Mr. Rajesh Kumar (Loan Specialist)
- **Persona**: Friendly and experienced loan specialist
- Presents pre-approved loan offers
- Calculates EMI for different amounts and tenures
- Negotiates loan terms with customer
- Initiates loan application
- Introduces himself: "Hello! I'm Rajesh Kumar, your loan specialist..."

#### 2. Verification Agent - Mr. Soham Patel (KYC Verification Officer)
- **Persona**: Professional and efficient KYC officer
- Fetches KYC details from CRM
- Verifies phone and address
- Checks PAN and Aadhar verification
- Completes KYC verification
- Introduces himself: "Hello! I'm Soham Patel from the KYC verification team..."

#### 3. Underwriting Agent - Ms. Ananya Desai (Credit Evaluation Specialist)
- **Persona**: Thorough and fair credit specialist
- Fetches credit score from credit bureau (out of 900)
- Evaluates loan eligibility based on rules:
  - Credit score ≥ 700 required
  - Amount ≤ pre-approved limit → Instant approval
  - Amount ≤ 2× pre-approved limit → Salary slip required, EMI ≤ 50% salary
  - Amount > 2× pre-approved limit → Reject
- Handles salary slip verification
- Approves or rejects loan with empathy
- Introduces herself: "Hello! I'm Ananya Desai, your credit evaluation specialist..."

#### 4. Sanction Letter Agent - Mr. Vikram Mehta (Documentation Officer)
- **Persona**: Meticulous and friendly documentation officer
- Generates comprehensive sanction letter data
- **Creates professional PDF documents** with Tata Capital branding
- **Saves PDF to device** in `sanction_letters` folder
- Sends via email and SMS
- Processes customer acceptance
- Provides complete loan journey summary
- Introduces himself: "Congratulations! I'm Vikram Mehta from the documentation team..."

## ✨ Key Features

### 🎭 Human-like Agent Personas
Each agent has a distinct personality and introduces themselves by name, creating a seamless, conversational experience:
- **Ms. Priya Sharma** (Master Agent) - Warm relationship manager who coordinates the team
- **Mr. Rajesh Kumar** (Sales) - Enthusiastic loan specialist
- **Mr. Soham Patel** (Verification) - Professional KYC officer
- **Ms. Ananya Desai** (Underwriting) - Empathetic credit specialist
- **Mr. Vikram Mehta** (Sanction Letter) - Detail-oriented documentation officer

### 📄 PDF Sanction Letter Generation
- Professional HTML-based template with Tata Capital branding
- Automatically generates PDF documents using WeasyPrint
- Saves customer copy to local device in `sanction_letters` folder
- Includes all loan details, terms & conditions, EMI schedule
- Reference numbers for tracking

## 📊 Mock Data

### Synthetic Customer Database (12 customers)
- Personal details (name, age, city)
- Financial info (salary, bank account)
- Current loans
- Credit scores (680-830)
- Pre-approved limits (₹3L - ₹15L)

### Mock APIs
- **CRM Server**: Customer KYC data
- **Credit Bureau**: Credit scores and history
- **Offer Mart**: Pre-approved loan offers

## 🛠️ Project Structure

```
project/
├── main.py                           # Entry point
├── utils.py                          # Utility functions
├── requirements.txt                  # Python dependencies
├── sanction_letters/                 # Generated PDF sanction letters (auto-created)
├── README.md                         # Documentation
├── mock_data/                   # Synthetic data
│   ├── __init__.py
│   ├── customer_data.py         # Customer database
│   ├── crm_data.py              # KYC/CRM data
│   ├── credit_bureau.py         # Credit scores
│   └── offer_mart.py            # Loan offers
└── loan_master_agent/                # Agent modules
    ├── __init__.py
    ├── agent.py                      # Master agent (Ms. Priya Sharma)
    └── sub_agents/
        ├── __init__.py
        ├── sales_agent/
        │   ├── __init__.py
        │   └── agent.py              # Mr. Rajesh Kumar
        ├── verification_agent/
        │   ├── __init__.py
        │   └── agent.py              # Mr. Soham Patel
        ├── underwriting_agent/
        │   ├── __init__.py
        │   └── agent.py              # Ms. Ananya Desai
        └── sanction_letter_agent/
            ├── __init__.py
            ├── agent.py              # Mr. Vikram Mehta
            └── sanction_letter_template.html  # PDF template
```

## 📦 Installation

1. **Prerequisites**
   ```bash
   python >= 3.10
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install individually:
   ```bash
   pip install google-adk python-dotenv litellm weasyprint
   ```

3. **Set up environment**
   Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

   **Getting your Mistral API Key:**
   - Visit [Mistral AI Console](https://console.mistral.ai/)
   - Sign up or log in to your account
   - Navigate to "API Keys" section
   - Create a new API key
   - Copy and paste it into your `.env` file
   
  **Note:** This project uses Mistral AI's `mistral-large-2411` model via LiteLLM for all agents (latest release per Mistral docs).

## 🚀 Usage

1. **Run the chatbot**
   ```bash
   cd project
   python main.py
   ```

2. **Select a test customer** from the displayed list

3. **Start chatting!** Example conversations:
   - "Hi, I received an email about a loan offer"
   - "What's my pre-approved amount?"
   - "Calculate EMI for 5 lakh over 36 months"
   - "I want to apply for a personal loan for home renovation"

4. **Commands**
   - `help` - Show help information
   - `status` - View application status
   - `exit` - End conversation

## 💬 Sample Conversation Flow

```
Customer: Hi, I received an email about a pre-approved loan

Agent: Welcome to Tata Capital, Rajesh! 🎉 I see you have a pre-approved 
personal loan offer of up to ₹5,00,000 at attractive interest rates. 
What would you like to use the loan for?

Customer: I need money for home renovation, around 4 lakhs

Agent: [Delegates to Sales Agent]
Great choice! Let me show you the EMI options for ₹4,00,000:
- 24 months: ₹18,731/month
- 36 months: ₹13,098/month  
- 48 months: ₹10,294/month

Which tenure works best for your budget?

Customer: 36 months looks good. Let's proceed.

Agent: [Initiates Application → Verification Agent]
Perfect! I've initiated your application. Now let me quickly verify your KYC...
✓ Phone verified
✓ Address verified
✓ PAN verified
✓ Aadhar verified
KYC verification complete!

Agent: [Underwriting Agent]
Let me check your credit eligibility...
Credit Score: 780 (Excellent!)
✓ Amount within pre-approved limit
🎉 Congratulations! Your loan of ₹4,00,000 is APPROVED!

Agent: [Sanction Letter Agent]
I've generated your sanction letter. Here are the details:
- Loan Amount: ₹4,00,000
- Interest Rate: 11.5% p.a.
- EMI: ₹13,098
- Tenure: 36 months
- First EMI Date: January 24, 2025

The sanction letter has been sent to your email and phone.
```

## 📋 Underwriting Rules

| Scenario | Condition | Action |
|----------|-----------|--------|
| Credit Score < 700 | Low score | **REJECT** |
| Amount ≤ Pre-approved | Within limit | **INSTANT APPROVAL** |
| Amount ≤ 2× Pre-approved | Extended limit | Need salary slip, EMI ≤ 50% salary |
| Amount > 2× Pre-approved | Exceeds limit | **REJECT** |

---

## 🧪 Testing & Deployment

The BFSI Loan Agent system provides multiple testing methods using Google ADK's built-in capabilities. Choose the method that best fits your workflow.

### Method 1: Interactive CLI (Current Implementation)

The default way to test the system is using the interactive command-line interface:

```bash
python main.py
```

**Features:**
- Select from 12 pre-loaded customers
- See pre-approved offers immediately
- Interactive chat with colored terminal output
- View session state and conversation history
- Commands: `exit`, `quit`, `help`, `status`

**Best For:** Development, debugging, quick testing scenarios

---

### Method 2: Web UI (New)

Run the modern web interface with Tata Capital branding.

1. **Start the Backend Server**
   ```bash
   # In the project root
   python server.py
   ```
   The server will start at `http://localhost:8000`.

2. **Start the Frontend**
   ```bash
   # Open a new terminal
   cd frontend
   npm run dev
   ```
   The application will be available at `http://localhost:3000`.

3. **Access the Application**
   - Open `http://localhost:3000` in your browser.
   - Select a customer profile to start.
   - Chat with the assistant and track your loan application in real-time.

---

### Method 3: ADK Web UI (Browser-Based Testing)

Launch an interactive web interface for testing your agents with a visual chat UI, event inspector, and trace viewer.

#### Setup:
```bash
# Navigate to project directory (parent of loan_master_agent)
cd d:\adk\agent-development-kit-crash-course\project

# Launch web UI
adk web
```

#### Access:
Open `http://localhost:8000` in your browser.

#### Features:
- **Agent Selector**: Choose `loan_master_agent` from the dropdown
- **Chat Interface**: Test conversations with the loan agent
- **Events Tab**: Inspect function calls, responses, and tool executions
- **Trace Logs**: View latency and performance metrics for each operation
- **Voice Support**: Enable microphone for voice-based testing (requires Gemini Live API models like `gemini-2.0-flash-live-001`)

**Troubleshooting:**
- Ensure you run `adk web` from the **parent directory** of `loan_master_agent`, NOT inside the agent folder
- If you don't see `loan_master_agent` in the dropdown, check your current directory
- For Windows users encountering `NotImplementedError`, use: `adk web --no-reload`

**Best For:** UI testing, event debugging, presentation demos, stakeholder reviews

---

### Method 3: ADK API Server (REST API Testing)

Launch a FastAPI server to test agents programmatically via REST endpoints.

#### Setup:
```bash
# Navigate to project directory
cd d:\adk\agent-development-kit-crash-course\project

# Start API server
adk api_server
```

#### Access:
Server runs on `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs` (Swagger UI)

#### Example Usage:

**1. Create a Session:**
```bash
curl -X POST http://localhost:8000/apps/loan_master_agent/users/CUST001/sessions/session_001 \
  -H "Content-Type: application/json" \
  -d '{"pre_approved_limit": 500000, "credit_score": 780}'
```

**2. Send a Message (Single Response):**
```bash
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "loan_master_agent",
    "userId": "CUST001",
    "sessionId": "session_001",
    "newMessage": {
      "role": "user",
      "parts": [{"text": "I need a loan of 8 lakh rupees"}]
    }
  }'
```

**3. Send a Message (Streaming Response):**
```bash
curl -X POST http://localhost:8000/run_sse \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "loan_master_agent",
    "userId": "CUST001",
    "sessionId": "session_001",
    "newMessage": {
      "role": "user",
      "parts": [{"text": "What are my options?"}]
    },
    "streaming": true
  }'
```

**4. Get Session Details:**
```bash
curl -X GET http://localhost:8000/apps/loan_master_agent/users/CUST001/sessions/session_001
```

**5. List All Agents:**
```bash
curl -X GET http://localhost:8000/list-apps
```

**Best For:** Integration testing, automation, CI/CD pipelines, external system integration

---

### Method 4: Programmatic Testing (Python Runner)

Create custom test scripts using ADK's `Runner` class for automated testing.

**Example Test Script** (`test_agent.py`):
```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from loan_master_agent.agent import loan_master_agent

async def test_loan_approval():
    # Initialize session service
    session_service = InMemorySessionService()
    
    # Create runner
    runner = Runner(
        agent=loan_master_agent,
        app_name="loan_test",
        session_service=session_service
    )
    
    # Create session with initial state
    user_id = "CUST001"
    session_id = "test_session_001"
    initial_state = {
        "customer_id": "CUST001",
        "customer_name": "Rajesh Kumar",
        "pre_approved_limit": 500000,
        "credit_score": 780
    }
    
    session_service.create_session(
        user_id=user_id,
        session_id=session_id,
        initial_state=initial_state,
        app_name="loan_test"
    )
    
    # Test conversation
    messages = [
        "I need a personal loan",
        "I want 8 lakh rupees for 3 years",
        "Yes, proceed with verification"
    ]
    
    for message in messages:
        print(f"\n🗣️ User: {message}")
        events = await runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        )
        
        # Process events
        for event in events:
            if hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text'):
                        print(f"🤖 Agent: {part.text}")

# Run test
asyncio.run(test_loan_approval())
```

**Run:**
```bash
python test_agent.py
```

**Best For:** Automated testing, unit tests, regression testing, CI/CD integration

---

### Deployment Options

#### Option 1: Google Cloud Agent Engine (Recommended)
Easiest deployment to a managed service on Google Cloud Vertex AI.

```bash
# Deploy to Agent Engine
gcloud auth login
adk deploy agent-engine --project-id YOUR_PROJECT_ID
```

**Documentation:** [ADK Agent Engine Guide](https://google.github.io/adk-docs/deploy/agent-engine/)

---

#### Option 2: Google Cloud Run (Serverless)
Deploy as a containerized serverless application.

```bash
# Build and deploy to Cloud Run
gcloud run deploy loan-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

**Documentation:** [ADK Cloud Run Guide](https://google.github.io/adk-docs/deploy/cloud-run/)

---

#### Option 3: Google Kubernetes Engine (GKE)
Deploy to Kubernetes for full control and scalability.

**Documentation:** [ADK GKE Guide](https://google.github.io/adk-docs/deploy/gke/)

---

### Additional ADK Features

#### Sessions & State Management
The system uses `InMemorySessionService` for stateful conversations:
- Tracks customer journey across conversation turns
- Maintains loan application state
- Stores interaction history

**View Session State:**
```python
session = session_service.get_session(user_id, session_id, app_name)
print(session.state)  # Current state
print(session.events)  # Conversation history
```

#### Callbacks & Observability
ADK supports integration with observability tools:
- **Cloud Trace**: Distributed tracing
- **AgentOps**: Agent performance monitoring
- **MLflow**: Experiment tracking
- **Phoenix**: AI observability
- **Weights & Biases Weave**: Model monitoring

**Enable Logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)
```

#### Evaluation & Testing
ADK provides built-in evaluation capabilities:
- Criteria-based evaluation
- User simulation for testing
- Automated test generation

**Documentation:** [ADK Evaluation Guide](https://google.github.io/adk-docs/evaluate/)

---

### 📚 Official ADK Resources

- **Documentation**: [https://google.github.io/adk-docs/](https://google.github.io/adk-docs/)
- **Python SDK**: [https://github.com/google/adk-python](https://github.com/google/adk-python)
- **Quickstart Guide**: [https://google.github.io/adk-docs/get-started/quickstart/](https://google.github.io/adk-docs/get-started/quickstart/)
- **API Reference**: [https://google.github.io/adk-docs/api-reference/](https://google.github.io/adk-docs/api-reference/)
- **Community**: [https://google.github.io/adk-docs/community/](https://google.github.io/adk-docs/community/)

---

## 🧪 Test Scenarios

### Scenario 1: Happy Path (Instant Approval)
- Customer: CUST002 (Priya Sharma)
- Credit Score: 820
- Pre-approved: ₹7,50,000
- Request: ₹5,00,000
- Expected: **Instant Approval** ✓

### Scenario 2: Conditional Approval (Salary Verification)
- Customer: CUST001 (Rajesh Kumar)
- Credit Score: 780
- Pre-approved: ₹5,00,000
- Request: ₹8,00,000
- Expected: **Salary slip required** → Approval if EMI ≤ 50% salary

### Scenario 3: Rejection (Low Credit Score)
- Customer: CUST010 (Deepa Nair)
- Credit Score: 680
- Pre-approved: ₹3,00,000
- Request: Any amount
- Expected: **Rejection** (Score < 700)

### Scenario 4: Rejection (Amount Too High)
- Customer: CUST005 (Vikram Singh)
- Credit Score: 720
- Pre-approved: ₹4,00,000
- Request: ₹10,00,000 (> 2× limit)
- Expected: **Rejection** (Exceeds max limit)

## 🔧 Customization

### Adding New Customers
Edit `mock_data/customer_data.py` to add new customer profiles.

### Modifying Underwriting Rules
Edit `loan_master_agent/sub_agents/underwriting_agent/agent.py` to change eligibility criteria.

### Changing Interest Rates
Edit `mock_data/offer_mart.py` to update loan offers and rates.

---

## 🧠 Advanced Intelligence Features - Detailed Guide

### 🎯 Pre-Conversation Intelligence Layer

This powerful feature analyzes the customer **before the conversation even starts**, providing the agent with critical context.

#### How It Works

**1. Campaign Analysis:**
- Identifies how the customer found you (Google Ads, Email Marketing, Referrals, Facebook, etc.)
- Extracts campaign keywords (e.g., "emergency medical loan", "home renovation", "wedding expenses")
- Determines customer intent automatically

**2. Customer Profiling:**
- Loads complete relationship history from CRM
- Checks payment history for existing customers
- Identifies customer type (new, repeat, VIP, etc.)
- Calculates relationship tenure

**3. Offer Pre-computation:**
- Generates 3 ranked loan offers before first message
- Considers pre-approved limits, credit score, income
- Prioritizes offers based on campaign intent

**4. Personalized Opening:**
- Creates contextual greeting based on customer history
- References specific campaign or previous interactions
- Sets appropriate tone (urgent, celebratory, consultative)

#### Intelligence Dashboard Example

```
🧠 AGENT INTELLIGENCE DASHBOARD
================================================================================

🎯 PRE-CONVERSATION INTELLIGENCE:
  Campaign Source: Email Marketing
  Campaign Keyword: existing customer top-up offer
  Customer Intent: ADDITIONAL_FUNDS
  Urgency Level: LOW
  Customer Type: 🌟 REPEAT_CUSTOMER
  Relationship Tenure: 2 years
  Payment History: EXCELLENT
  Current Loans: 1
  Offer Expires In: 120 hours

💡 AI-GENERATED OPENING:
  "Hi Rajesh! I'm Priya Sharma from Tata Capital. It's wonderful to see you 
   again! You've been a valued customer for 2 years with an excellent 
   repayment track record. I noticed you're interested in our exclusive 
   top-up loan offer..."
```

#### Campaign Types Configured

| Campaign | Source | Intent | Urgency | Best Strategy |
|----------|--------|--------|---------|---------------|
| Medical Emergency | Google Ads | URGENT_EXPENSE | HIGH | Speed Assurance |
| Home Renovation | Google Ads | HOME_IMPROVEMENT | MEDIUM | Practical EMI Focus |
| Wedding Expenses | Facebook | LIFE_EVENT | MEDIUM | Emotional Connection |
| Top-up Offer | Email | ADDITIONAL_FUNDS | LOW | Loyalty Appreciation |
| Friend Referral | Referral | TRUST_BASED | MEDIUM | Social Proof |
| Rate Shopping | Website | PRICE_COMPARISON | LOW | Transparent Factual |

#### How to Use

**Automatic Mode (Recommended):**
```bash
python main.py
# Intelligence dashboard appears automatically
```

**Programmatic Access:**
```python
from mock_data.campaign_data import get_campaign_data, get_personalized_opening

# Get campaign intelligence
campaign_data = get_campaign_data("CUST001")
print(campaign_data['intent'])           # "ADDITIONAL_FUNDS"
print(campaign_data['urgency_level'])    # "LOW"
print(campaign_data['customer_type'])    # "REPEAT_CUSTOMER"

# Generate personalized opening
opening = get_personalized_opening("CUST001", "Rajesh Kumar", campaign_data)
```

---

### 🧠 Persuasion Strategy Engine

The system **automatically selects the optimal sales approach** based on customer psychology and profile.

#### Customer Profile Types

**1. FIRST_TIME_CAUTIOUS**
- **Who:** New borrowers with no loan history
- **Approach:** Educational and patient
- **Tone:** Warm, reassuring
- **Key Phrases:**
  - "Let me explain how this works step by step..."
  - "There are no hidden charges, I'll show you the complete breakdown..."
  - "You're in complete control throughout the process..."
- **Focus:** Process explanation, trust building, transparency

**2. REPEAT_LOYAL**
- **Who:** Existing customers with good repayment history
- **Approach:** Upgrade pitch with appreciation
- **Tone:** Grateful, celebratory
- **Key Phrases:**
  - "As a valued customer for X years, you're pre-approved..."
  - "Your excellent repayment record qualifies you for special rates..."
  - "We've reserved this exclusive offer just for you..."
- **Focus:** Relationship value, loyalty rewards, exclusive benefits

**3. HIGH_CREDIT_AFFLUENT**
- **Who:** 800+ credit score, high income (₹1L+)
- **Approach:** Premium offering
- **Tone:** Confident, professional
- **Key Phrases:**
  - "You qualify for our best rate of 10.99% p.a."
  - "Your excellent credit profile gets you instant approval..."
  - "Higher limits available up to ₹35 lakhs..."
- **Focus:** Best rates, instant approval, premium service

**4. BUDGET_CONSCIOUS**
- **Who:** Lower income (<₹50K), first-time borrowers
- **Approach:** EMI-focused affordability
- **Tone:** Practical, empathetic
- **Key Phrases:**
  - "Just ₹8,500 per month - that's less than your monthly dining expenses..."
  - "Flexible tenure options to fit your budget..."
  - "No prepayment charges - pay off early if you can..."
- **Focus:** Monthly affordability, flexible terms, value for money

**5. SKEPTICAL_RESEARCHER**
- **Who:** Multiple visits, rate comparisons, detail-oriented
- **Approach:** Transparent and data-driven
- **Tone:** Factual, detailed
- **Key Phrases:**
  - "Here's the complete breakdown with all charges..."
  - "Total cost of ₹5L loan = ₹1,85,000 interest over 5 years..."
  - "Zero hidden fees - processing fee 3.5% + GST upfront..."
- **Focus:** Complete transparency, competitive comparison, detailed calculations

**6. URGENT_NEED**
- **Who:** Medical emergency, time-sensitive situations
- **Approach:** Speed and empathy
- **Tone:** Reassuring, efficient
- **Key Phrases:**
  - "We can approve this in 2 hours and disburse within 24 hours..."
  - "I understand the urgency, let's fast-track this..."
  - "Minimal documentation needed - just 4 documents..."
- **Focus:** Quick approval, fast disbursement, minimal hassle

#### Strategy Selection Logic

```python
# Automatic profile determination based on:
- Credit Score (≥800 = Affluent, 700-799 = Standard, <700 = Cautious)
- Income Level (≥₹1L = Affluent, ₹50K-₹1L = Standard, <₹50K = Budget)
- Campaign Source (Referral = Trust, Medical = Urgent, etc.)
- Browsing Behavior (Multiple visits = Skeptical)
- Previous Interactions (Existing customer = Loyal)
```

#### Customizing Strategies

Add new profiles in `mock_data/persuasion_strategy.py`:

```python
CUSTOMER_PROFILES["YOUR_PROFILE"] = {
    "description": "Young professionals, tech-savvy",
    "strategy": "DIGITAL_FIRST",
    "tone": "modern_casual",
    "pace": "FAST",
    "focus_areas": ["digital_process", "instant_approval"],
    "technique": {
        "key_phrases": [
            "100% digital, no branch visits...",
            "Instant approval on your phone...",
            "E-sign and done!"
        ],
        "proof_elements": ["app_ratings", "processing_time", "success_stories"],
        "objection_anticipation": ["documentation_hassle", "trust_online"]
    }
}
```

---

### ⚠️ Intelligent Objection Handling System

**Real-time detection** of customer concerns with **proven counter-strategies**.

#### Objection Types & Success Rates

| Objection | Detection Phrases | Counter Strategy | Success Rate |
|-----------|-------------------|------------------|--------------|
| **Interest Rate High** | "rate seems high", "expensive interest" | Market Comparison + Savings Calculation | 68% |
| **EMI Too High** | "can't afford", "EMI too much" | Tenure Extension + Flexibility Options | 75% |
| **No Immediate Need** | "just exploring", "not urgent" | Urgency Creation + Pre-approval Benefits | 52% |
| **Repayment Fear** | "what if I can't repay", "job loss" | Flexible Options + Insurance Coverage | 71% |
| **Hidden Charges** | "any hidden fees", "extra charges" | Complete Transparency + Written Guarantee | 82% |
| **Documentation Hassle** | "too much paperwork", "complicated process" | Minimal Docs Pitch + Digital Process | 77% |
| **Credit Score Worry** | "my CIBIL is low", "bad credit" | Pre-check Assurance + Alternate Solutions | 65% |
| **Better Offer Elsewhere** | "bank offered better", "cheaper elsewhere" | Total Cost Comparison + Service Edge | 73% |

#### Counter-Strategy Examples

**For "Interest rate seems high":**
```
🎯 Market Rate Comparison Strategy

"I understand your concern about the rate. Let me give you perspective:

Market Comparison:
┌─────────────────────────┬──────────┐
│ Bank Personal Loans     │ 13-15%   │
│ Credit Card EMI         │ 18-24%   │
│ Tata Capital            │ 10.99%   │ ✓
└─────────────────────────┴──────────┘

Real Savings Example:
₹5,00,000 loan over 5 years:
• At our 11.99% = ₹1,85,000 interest
• At bank's 14% = ₹2,45,000 interest
• You SAVE ₹60,000 with us!"

Success Rate: 68%
```

**For "EMI is too high":**
```
🎯 Tenure Extension Strategy

"Let's adjust the tenure to make it comfortable:

Current: ₹5L at 36 months = ₹16,600/month

Adjusted Options:
• 48 months = ₹12,800/month (₹3,800 less!)
• 60 months = ₹10,800/month (₹5,800 less!)
• 72 months = ₹9,400/month (₹7,200 less!)

Flexibility:
✓ Prepay anytime after 12 months (zero charges)
✓ 25% prepayment allowed with minimal fee
✓ Reduce tenure by paying extra EMIs"

Success Rate: 75%
```

**For "What if I can't repay?":**
```
🎯 Flexible Repayment Strategy

"We've designed safety nets for exactly this concern:

Protection Options:
1. Payment Holiday: Skip 2 EMIs in case of emergency
2. Loan Insurance: Coverage for job loss/disability
3. Tenure Extension: Restructure during hardship
4. Grace Period: 15 days grace on each EMI
5. Part Payment: Pay 50% if facing temporary crunch

Real Case Study:
Mr. Sharma faced a job loss in month 8. We:
• Extended his tenure by 12 months
• Reduced EMI from ₹18K to ₹13K
• Zero penalty, zero extra charges
• He successfully completed repayment!"

Success Rate: 71%
```

#### Detection in Action

When customer types: **"The interest rate seems too high compared to what my friend got from his bank"**

```
⚠️ OBJECTION DETECTED
═══════════════════════════════════════
Type: INTEREST_RATE_HIGH
Confidence: 85%
Severity: HIGH
Trigger: "interest rate seems too high", "compared to", "bank"

Recommended Counter-Strategy:
Strategy: Market Rate Comparison
Success Rate: 68%
Approach: Show competitive rates + total savings calculation
```

Agent automatically receives context and responds accordingly.

#### How to Use

**Automatic Detection (Built-in):**
The system automatically detects objections in customer messages when running `main.py`.

**Manual Detection:**
```python
from mock_data.objection_handler import detect_objection, get_objection_response

message = "The EMI is too much for my budget"
detected = detect_objection(message)

if detected:
    objection = detected[0]
    print(f"Type: {objection['type']}")           # EMI_TOO_HIGH
    print(f"Confidence: {objection['confidence']}") # 0.90
    
    # Get counter-strategy
    response = get_objection_response(objection['type'], {})
    print(response['response_template'])  # Full counter-strategy
```

#### Adding Custom Objections

In `mock_data/objection_handler.py`:

```python
OBJECTION_TYPES["YOUR_OBJECTION"] = {
    "category": "TRUST",
    "severity": "MEDIUM",
    "common_phrases": [
        "don't trust NBFCs",
        "prefer banks",
        "never heard of Tata Capital"
    ],
    "counter_strategies": ["brand_credibility"]
}

COUNTER_STRATEGIES["brand_credibility"] = {
    "name": "Brand Trust Building",
    "approach": "Leverage Tata group credibility",
    "response_template": """
"I appreciate your concern about trust. Let me share:

Tata Capital Credentials:
✓ Part of 150+ year old Tata Group
✓ ₹70,000+ Crore AUM
✓ RBI Regulated & Registered NBFC
✓ 4.2/5 Rating on Google (50,000+ reviews)
✓ Serving 5+ Million customers since 2007

Awards & Recognition:
• Best NBFC 2023 - Economic Times
• AA+ Credit Rating - CRISIL
• ISO 27001 Certified

Would you like to see our RBI registration or speak to existing customers?"
    """,
    "success_rate": 0.79,
    "best_for": ["skeptical_researcher", "first_time_cautious"]
}
```

---

## 📄 Salary Slip Upload & Verification - Complete Workflow

### Overview

For loan amounts **between 1× and 2× the pre-approved limit**, the system requires salary slip verification to ensure EMI affordability.

**Eligibility Rule:** EMI must be ≤ 50% of monthly salary

### Complete Workflow

#### Step 1: File Upload
Agent requests: "Please upload your latest salary slip (PDF or image)"

**Supported Formats:**
- ✅ PDF files (.pdf)
- ✅ Image files (.jpg, .jpeg, .png, .tiff, .bmp)

**Upload Methods:**
```python
# In main.py conversation
Customer: "Here is my salary slip"
Agent: "Please provide the file path"
Customer: "D:\documents\salary_slip.pdf"
```

#### Step 2: Text Extraction

**For PDF Files:**
Uses **PyPDF2** library to extract embedded text
```python
from PyPDF2 import PdfReader

reader = PdfReader(file_path)
text = ""
for page in reader.pages:
    text += page.extract_text()
```

**For Image Files:**
Uses **Tesseract OCR** via pytesseract
```python
from PIL import Image
import pytesseract

image = Image.open(file_path)
text = pytesseract.image_to_string(image)
```

#### Step 3: AI-Powered Salary Extraction

**Priority-based extraction** using advanced regex patterns:

| Priority | Salary Type | Pattern Examples |
|----------|-------------|------------------|
| **Very High** | Net Pay, Take Home | "NET PAY: ₹60,900", "TAKE HOME: 60900.00" |
| **High** | Bank Credit | "SALARY CREDIT: ₹60,900", "CREDIT TO BANK: 60900" |
| **Medium** | Total Net Pay | "TOTAL NET PAY: ₹60,900" |
| **Low** | Gross Salary | "GROSS EARNINGS: ₹75,000" |
| **Very Low** | Basic Salary | "BASIC SALARY: ₹45,000" |

**Extraction Result:**
```python
{
    "status": "success",
    "monthly_salary": 60900.00,
    "confidence": "very_high",
    "salary_type": "Net Pay",
    "all_amounts_found": [
        {"amount": 60900.00, "type": "Net Pay", "confidence": "very_high"},
        {"amount": 75000.00, "type": "Gross Earnings", "confidence": "low"},
        {"amount": 45000.00, "type": "Basic Salary", "confidence": "very_low"}
    ],
    "method": "regex_extraction"
}
```

#### Step 4: EMI Affordability Check

**Formula:**
```
EMI Ratio = (Monthly EMI / Monthly Salary) × 100

✅ If EMI Ratio ≤ 50% → APPROVE
❌ If EMI Ratio > 50% → REJECT or SUGGEST LOWER AMOUNT
```

**Example Calculation:**
```
Loan Amount: ₹10,00,000
Tenure: 60 months
Interest Rate: 12% p.a.
EMI: ₹22,244

Verified Salary: ₹60,900
EMI Ratio: (22,244 / 60,900) × 100 = 36.5%

Result: ✅ APPROVED (36.5% < 50%)
```

#### Step 5: Decision & Action

**Scenario A: Approved**
```
✅ SALARY VERIFICATION SUCCESSFUL

Verified Details:
• Monthly Salary: ₹60,900 (Net Pay)
• Monthly EMI: ₹22,244
• EMI/Salary Ratio: 36.5%
• Status: WITHIN LIMITS ✓

Your loan of ₹10,00,000 is APPROVED!
Proceeding to sanction letter generation...
```

**Scenario B: Rejected**
```
⚠️ EMI EXCEEDS AFFORDABILITY LIMIT

Analysis:
• Monthly Salary: ₹60,900
• Requested EMI: ₹32,000
• EMI/Salary Ratio: 52.5% ❌

Alternative Options:
1. Reduce loan amount to ₹7,50,000
   → New EMI: ₹28,500 (46.8%) ✓
   
2. Extend tenure to 72 months
   → New EMI: ₹27,200 (44.7%) ✓
```

### Testing the Workflow

**Step 1: Generate Sample Salary Slips**
```bash
cd test_documents
python generate_sample_pdfs.py
```

Creates:
- `sample_salary_slip_1.pdf` - Amit Patel (₹60,900 net pay)
- `sample_salary_slip_2.pdf` - Priya Sharma (₹1,01,925 net pay)

**Step 2: Run Test Suite**
```bash
python test_salary_slip_upload.py
```

Verifies:
- ✅ PDF text extraction
- ✅ Salary amount identification
- ✅ Priority-based selection (Net Pay over Basic)
- ✅ EMI calculation
- ✅ Affordability verification

**Step 3: Live Test**
```bash
python main.py
```

1. Select: **CUST001 - Amit Patel**
2. Request: **₹12,00,000** (1.7× pre-approved limit of ₹7L)
3. Agent asks for salary slip
4. Provide: `D:\ey_techathon\LoanAI\test_documents\sample_salary_slip_1.pdf`
5. System auto-processes and approves ✓

### Required Dependencies

```bash
# Install all salary verification dependencies
pip install PyPDF2 Pillow pytesseract reportlab

# Tesseract OCR Engine (system-level)
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

### File Structure

```
LoanAI/
├── loan_master_agent/
│   └── sub_agents/
│       └── underwriting_agent/
│           └── agent.py                    # Contains all salary verification functions
├── test_documents/
│   ├── sample_salary_slip_1.pdf           # Test PDF 1
│   ├── sample_salary_slip_2.pdf           # Test PDF 2
│   ├── generate_sample_pdfs.py            # PDF generator
│   └── test_salary_slip_upload.py         # Test suite
└── requirements.txt
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `extract_text_from_pdf()` | Extract text from PDF files |
| `extract_text_from_image()` | OCR from image files |
| `extract_salary_from_text()` | AI-powered salary identification |
| `upload_and_verify_salary_slip()` | Complete upload + verification cycle |
| `verify_salary_with_amount()` | EMI affordability check |

---

## 📈 Key Deliverables

1. ✅ Master Agent orchestrating multiple worker agents
2. ✅ Sales Agent for loan negotiation
3. ✅ Verification Agent for KYC
4. ✅ Underwriting Agent for credit evaluation with salary slip verification
5. ✅ Sanction Letter Generator with PDF creation
6. ✅ Synthetic customer data (12 customers)
7. ✅ Mock CRM, Credit Bureau, and Offer Mart APIs
8. ✅ Complete end-to-end loan journey
9. ✅ **Pre-Conversation Intelligence Layer** with campaign tracking (8 campaign types)
10. ✅ **Smart AI-Driven Persuasion** (LLM-based, no hard-coded profiles) - **Powered by Mistral AI**
11. ✅ **Intelligent Objection Handling** with 8 objection types and counter-strategies
12. ✅ **Salary Slip Upload & OCR Verification** with affordability checking
13. ✅ **⚡ Parallel Agentic Processing** - 3× faster approvals with background data pre-loading
14. ✅ **💚 Emotional Intelligence** - Mistral AI-powered sentiment detection & adaptive strategies
15. ✅ **📈 Self-Improving Feedback Loop** - Analytics dashboard with week-over-week tracking
16. ✅ **🎁 Contextual Cross-Sell Engine** - Smart product recommendations (5 products)

---

## 🤖 Technology Stack

**AI Models:**
- **Mistral AI** (mistral-large-2411) - Powers ALL agents and intelligence
- **Google ADK** - Agent framework

**Intelligence Features:**
- ✅ Sentiment Analysis (Mistral AI)
- ✅ Smart Persuasion (Mistral AI)
- ✅ Objection Handling (Pattern matching + AI)
- ✅ Analytics Tracking (JSON-based)
- ✅ Cross-Sell Engine (Relevance scoring)

**Backend:**
- Python 3.10+
- LiteLLM (Model integration)
- WeasyPrint (PDF generation)
- PyPDF2 & Tesseract (OCR)

## 🛡️ Assumptions Made

1. All customers have existing bank accounts for disbursement
2. KYC data is pre-verified for most customers
3. Credit scores are fetched from a centralized bureau
4. Pre-approved offers are valid for 30 days
5. Salary slip verification uses OCR (PyPDF2 + Tesseract) for automated extraction
6. Sanction letters are professional PDF documents with Tata Capital branding
7. Campaign data is configured for intelligence layer (8 campaign types)
8. Objection detection uses pattern matching with 75-90% confidence
9. Persuasion strategies are applied automatically based on customer profiling

## 📞 Support

For any queries:
- Toll-free: 1800-XXX-XXXX
- Email: support@tatacapital.com

---

**Built with Google ADK (Agent Development Kit) and Mistral AI**
