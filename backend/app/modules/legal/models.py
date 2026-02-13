"""
Legal Assistant Module - Models
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class ClauseType(str, Enum):
    DEFINITION = "definition"
    COVENANT = "covenant"
    INDEMNITY = "indemnity"
    TERMINATION = "termination"
    LIABILITY = "liability"
    GENERAL = "general"

class LegalClause(BaseModel):
    clause_id: int
    type: str
    text: str
    tldr: str
    explanation: str
    business_impact: List[str]
    risk_level: RiskLevel
    page_number: Optional[int] = None
    redlines: List[str] = []
    negotiation_points: List[str] = []

class Citation(BaseModel):
    source: str
    url: Optional[str] = None
    page: Optional[int] = None
    confidence: float

class LegalTranslateRequest(BaseModel):
    document_path: Optional[str] = None
    document_text: Optional[str] = None
    document_type: str = "contract"

class LegalTranslateResponse(BaseModel):
    summary: str
    key_points: List[str]
    risk_level: RiskLevel
    clauses: List[LegalClause]
    redlines: List[str]
    citations: List[Citation]
    confidence_score: float
    lawyer_required: bool
    lawyer_required_reason: Optional[str] = None
    legal_disclaimer: str
    report_id: str
