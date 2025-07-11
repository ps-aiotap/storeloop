from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Optional

@dataclass
class ConversationContext:
    customer_name: str
    interaction_history: List[str]
    last_contact_date: datetime
    tags: List[str]
    channel: Literal["whatsapp", "email", "upwork", "phone"]
    mode: Literal["storeloop", "aiotap"]
    customer_id: Optional[int] = None
    lead_stage: Optional[str] = None

@dataclass
class ReplyContext:
    message_text: str
    customer_context: ConversationContext
    intent: Optional[str] = None
    urgency: Literal["low", "medium", "high"] = "medium"

@dataclass
class FollowUpContext:
    customer_context: ConversationContext
    days_since_contact: int
    previous_followups: List[str]
    campaign_type: Optional[str] = None

@dataclass
class IntentContext:
    message_text: str
    customer_history: List[str]
    mode: Literal["storeloop", "aiotap"]
    channel: str