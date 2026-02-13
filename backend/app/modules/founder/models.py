"""
Founder Research Module - Models
"""
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class FounderIngestRequest(BaseModel):
    founder_name: str
    linkedin_url: Optional[HttpUrl] = None
    twitter_url: Optional[HttpUrl] = None
    pitch_deck_path: Optional[str] = None
    user_notes: Optional[str] = None
    consent_obtained: bool = False

class FounderScorecard(BaseModel):
    leadership: float  # 0-10
    execution: float   # 0-10
    domain_fit: float  # 0-10
    risk: float        # 0-10 (higher = more risk)
    signal_strength: float  # 0-10

class Citation(BaseModel):
    source: str
    url: Optional[str] = None
    page: Optional[int] = None
    confidence: float

class Provenance(BaseModel):
    retrieved_facts: List[Dict[str, Any]]
    inferences: List[Dict[str, Any]]
    user_commentary: List[Dict[str, Any]]

class FounderAnalysisResponse(BaseModel):
    summary: str
    key_points: List[str]
    risk_level: RiskLevel
    scorecard: FounderScorecard
    key_strengths: List[str]
    key_risks: List[str]
    suggested_questions: List[str]
    citations: List[Citation]
    provenance: Provenance
    confidence_score: float
    report_id: str
