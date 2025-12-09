# Sub-agents module for Loan Master Agent
from .sales_agent.agent import sales_agent
from .verification_agent.agent import verification_agent
from .underwriting_agent.agent import underwriting_agent
from .sanction_letter_agent.agent import sanction_letter_agent

__all__ = [
    "sales_agent",
    "verification_agent",
    "underwriting_agent",
    "sanction_letter_agent"
]
