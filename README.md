# 🏦 BFSI Personal Loan Chatbot - Tata Capital Digital Sales Assistant

A multi-agent AI system for automating personal loan sales process for a Non-Banking Financial Company (NBFC). This solution simulates a human-like sales process using an Agentic AI approach with a Master Agent orchestrating multiple Worker Agents.

## 📋 Problem Statement

The NBFC (Tata Capital) wants to improve its sales success rate for personal loans by using an AI-driven conversational approach. The solution simulates a human-like sales process where the Master Agent handles customer conversations, engages customers in a personalized manner, and collaborates with multiple Worker AI agents to complete the loan process.

## 🎯 Solution Overview

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MASTER AGENT                                      │
│                  (Loan Master Agent - Orchestrator)                       │
│    • Manages conversation flow                                            │
│    • Coordinates worker agents                                            │
│    • Starts and ends conversations                                        │
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
```

## 🚀 Features

### Master Agent (Orchestrator)
- Manages end-to-end conversation flow
- Welcomes customers and understands their needs
- Delegates to appropriate worker agents
- Ensures smooth handoffs between agents

### Worker Agents

#### 1. Sales Agent
- Presents pre-approved loan offers
- Calculates EMI for different amounts and tenures
- Negotiates loan terms
- Initiates loan application

#### 2. Verification Agent
- Fetches KYC details from CRM
- Verifies phone and address
- Checks PAN and Aadhar verification
- Completes KYC verification

#### 3. Underwriting Agent
- Fetches credit score from credit bureau (out of 900)
- Evaluates loan eligibility based on rules:
  - Credit score ≥ 700 required
  - Amount ≤ pre-approved limit → Instant approval
  - Amount ≤ 2× pre-approved limit → Salary slip required, EMI ≤ 50% salary
  - Amount > 2× pre-approved limit → Reject
- Handles salary slip verification
- Approves or rejects loan

#### 4. Sanction Letter Agent
- Generates PDF sanction letter
- Sends via email and SMS
- Processes customer acceptance
- Provides loan journey summary

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
├── main.py                      # Entry point
├── utils.py                     # Utility functions
├── README.md                    # Documentation
├── mock_data/                   # Synthetic data
│   ├── __init__.py
│   ├── customer_data.py         # Customer database
│   ├── crm_data.py              # KYC/CRM data
│   ├── credit_bureau.py         # Credit scores
│   └── offer_mart.py            # Loan offers
└── loan_master_agent/           # Agent modules
    ├── __init__.py
    ├── agent.py                 # Master agent
    └── sub_agents/
        ├── __init__.py
        ├── sales_agent/
        │   ├── __init__.py
        │   └── agent.py
        ├── verification_agent/
        │   ├── __init__.py
        │   └── agent.py
        ├── underwriting_agent/
        │   ├── __init__.py
        │   └── agent.py
        └── sanction_letter_agent/
            ├── __init__.py
            └── agent.py
```

## 📦 Installation

1. **Prerequisites**
   ```bash
   python >= 3.10
   ```

2. **Install dependencies**
   ```bash
   pip install google-adk python-dotenv litellm
   ```

3. **Set up environment**
   Create a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

   **Note:** This project uses Mistral AI's large language model via LiteLLM. Get your Mistral API key from [Mistral AI Console](https://console.mistral.ai/).

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

### Method 2: ADK Web UI (Browser-Based Testing)

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

## 📈 Key Deliverables

1. ✅ Master Agent orchestrating multiple worker agents
2. ✅ Sales Agent for loan negotiation
3. ✅ Verification Agent for KYC
4. ✅ Underwriting Agent for credit evaluation
5. ✅ Sanction Letter Generator
6. ✅ Synthetic customer data (12 customers)
7. ✅ Mock CRM, Credit Bureau, and Offer Mart APIs
8. ✅ Complete end-to-end loan journey

## 🛡️ Assumptions Made

1. All customers have existing bank accounts for disbursement
2. KYC data is pre-verified for most customers
3. Credit scores are fetched from a centralized bureau
4. Pre-approved offers are valid for 30 days
5. Salary slip verification is simulated (in production, would use OCR/document AI)
6. Sanction letters are generated as text (in production, would be actual PDF)

## 📞 Support

For any queries:
- Toll-free: 1800-XXX-XXXX
- Email: support@tatacapital.com

---

**Built with Google ADK (Agent Development Kit) and Mistral AI**
