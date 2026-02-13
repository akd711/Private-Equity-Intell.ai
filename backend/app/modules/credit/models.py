"""
Credit Facility Analysis Module - Models
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Covenant(BaseModel):
    name: str
    description: str
    type: str  # financial or operational
    risk_level: RiskLevel

class Citation(BaseModel):
    source: str
    url: Optional[str] = None
    page: Optional[int] = None
    confidence: float

class CreditAnalyzeRequest(BaseModel):
    document_path: Optional[str] = None
    document_text: Optional[str] = None
    agreement_url: Optional[str] = None

class CreditAnalysisResponse(BaseModel):
    summary: str
    key_points: List[str]
    risk_level: RiskLevel
    
    # Credit facility details
    loan_amount: Optional[str] = None
    interest_rate: Optional[str] = None
    margin: Optional[str] = None
    maturity_date: Optional[str] = None
    
    # Analysis
    covenants: List[Covenant]
    events_of_default: List[str]
    security_collateral: List[str]
    fees: List[str]
    
    # Risk assessment
    risk_heatmap: Dict[str, RiskLevel]
    hidden_costs: List[str]
    negotiation_points: List[str]
    worst_case_scenario: str
    lawyer_attention_items: List[str]
    cost_saving_opportunities: List[str]
    
    # Flags
    aggressive_terms: List[str]
    unusual_covenants: List[str]
    cross_default_risks: List[str]
    ambiguous_language: List[str]
    
    citations: List[Citation]
    confidence_score: float
    lawyer_required: bool
    lawyer_required_reason: Optional[str] = None
    report_id: str
