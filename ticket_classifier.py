from typing import Literal
from pydantic import BaseModel, Field
import config

# This defines the exact shape of data we want Gemini to return
class SupportTicket(BaseModel):
    category: Literal["Billing", "Technical", "Account", "Delivery", "Order", "Refund", "Other"] = Field(
        description="The type of issue the customer is facing"
    )
    priority: Literal["High", "Medium", "Low"] = Field(
        description="How urgent this ticket is"
    )
    sentiment: Literal["Positive", "Neutral", "Negative"] = Field(
        description="The emotional tone of the customer's message"
    )
    summary: str = Field(
        description="A short one or two line summary of the issue"
    )
    recommended_team: str = Field(
        description="The support team that should handle this ticket"
    )
    requires_human_agent: bool = Field(
        description="True if this issue is too complex or sensitive for AI alone"
    )


# This tells Gemini to always answer using the SupportTicket shape above
classifier_llm = config.llm.with_structured_output(SupportTicket)


def classify_ticket(customer_query: str) -> SupportTicket:
    """Sends the customer's message to Gemini and gets back a structured ticket."""
    ticket = classifier_llm.invoke(customer_query)
    return ticket


