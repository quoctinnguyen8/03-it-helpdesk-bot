"""Message entity for chat conversations."""

from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    """Enumeration for message types in a chat conversation."""
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    """Represents a message in a chat conversation."""
    type: MessageType
    content: str
