"""
detection.py — Pydantic schemas for scam detection API.

Defines the request and response data shapes for the detection endpoint.
Pydantic validates incoming JSON automatically — FastAPI uses these schemas
to generate OpenAPI docs as well.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ScamCategory(str, Enum):
    """Known categories of scam content that the model can classify."""
    PHISHING    = "phishing"
    LOTTERY     = "lottery"
    INVESTMENT  = "investment"
    ROMANCE     = "romance"
    TECH_SUPPORT = "tech_support"
    UNKNOWN     = "unknown"


class DetectionRequest(BaseModel):
    """Payload sent by the client to request scam analysis."""
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The message or content to analyze for scam indicators",
        examples=["Congratulations! You have been selected to receive $1,000,000."],
    )
    language: Optional[str] = Field(
        default="en",
        description="ISO 639-1 language code of the input text",
    )


class DetectionResponse(BaseModel):
    """Result returned by the scam detection endpoint."""
    is_scam: bool = Field(..., description="True if the text is classified as a scam")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score (0–1)")
    category: ScamCategory = Field(..., description="Type of scam detected")
    explanation: Optional[str] = Field(None, description="Human-readable reason for the classification")
    processed_text: Optional[str] = Field(None, description="Cleaned/normalized version of the input")
