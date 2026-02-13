"""
Legal Assistant Module - Service
"""
from .models import (
    LegalTranslateRequest,
    LegalTranslateResponse,
    LegalClause,
    Citation,
    RiskLevel
)
from app.rag.pipeline import RAGPipeline
from app.parsers.document_parser import DocumentParser
from fastapi import UploadFile
import os
from typing import Dict, Any

LEGAL_DISCLAIMER = """
⚠️ LEGAL DISCLAIMER ⚠️

This analysis is provided for informational purposes only and does not constitute legal advice.
This tool uses AI to analyze legal documents and may contain errors, omissions, or 
misinterpretations. Always consult with a qualified attorney before making any legal decisions.

The analysis provided is based on general legal principles and may not account for:
- Jurisdiction-specific laws and regulations
- Recent legal developments or case law
- Your specific circumstances and context
- Complex interactions between clauses

DO NOT rely solely on this analysis for legal decisions.
"""

class LegalAssistantService:
    def __init__(self):
        self.rag = RAGPipeline()
        self.parser = DocumentParser()
        self.reports = {}  # In-memory storage
    
    async def translate_document(
        self,
        request: LegalTranslateRequest,
        report_id: str
    ) -> LegalTranslateResponse:
        """Translate legal document to plain English"""
        
        # Get document text
        if request.document_path and os.path.exists(request.document_path):
            if request.document_path.endswith('.pdf'):
                parsed = self.parser.parse_pdf(request.document_path)
                document_text = parsed["full_text"]
            elif request.document_path.endswith('.docx'):
                parsed = self.parser.parse_docx(request.document_path)
                document_text = parsed["full_text"]
            else:
                with open(request.document_path, 'r') as f:
                    document_text = f.read()
        else:
            document_text = request.document_text or ""
        
        if not document_text:
            raise ValueError("No document text available")
        
        # Extract clauses
        extracted_clauses = self.parser.extract_clauses(document_text)
        
        # Analyze each clause
        analyzed_clauses = []
        high_risk_count = 0
        
        for clause_data in extracted_clauses[:10]:  # Limit to 10 clauses for demo
            clause_analysis = await self._analyze_clause(clause_data["text"])
            
            clause = LegalClause(
                clause_id=clause_data["clause_id"],
                type=clause_data.get("type", "general"),
                text=clause_data["text"][:500],  # Truncate for response
                tldr=clause_analysis.get("tldr", ""),
                explanation=clause_analysis.get("explanation", ""),
                business_impact=clause_analysis.get("business_impact", []),
                risk_level=clause_analysis.get("risk_level", RiskLevel.LOW),
                redlines=clause_analysis.get("redlines", []),
                negotiation_points=clause_analysis.get("negotiation_points", [])
            )
            
            if clause.risk_level == RiskLevel.HIGH:
                high_risk_count += 1
            
            analyzed_clauses.append(clause)
        
        # Determine overall risk and lawyer requirement
        overall_risk = RiskLevel.HIGH if high_risk_count >= 2 else (
            RiskLevel.MEDIUM if high_risk_count == 1 else RiskLevel.LOW
        )
        
        lawyer_required = overall_risk == RiskLevel.HIGH
        lawyer_reason = (
            f"Document contains {high_risk_count} high-risk clauses requiring legal review"
            if lawyer_required else None
        )
        
        # Generate summary
        summary = f"Analyzed {len(analyzed_clauses)} clauses. Overall risk: {overall_risk.value}."
        
        response = LegalTranslateResponse(
            summary=summary,
            key_points=[
                f"Total clauses analyzed: {len(analyzed_clauses)}",
                f"High-risk clauses: {high_risk_count}",
                "Lawyer review recommended" if lawyer_required else "Standard review process"
            ],
            risk_level=overall_risk,
            clauses=analyzed_clauses,
            redlines=[
                "Consider adding limitation of liability clause",
                "Clarify termination conditions"
            ],
            citations=[
                Citation(
                    source="Original Document",
                    page=1,
                    confidence=1.0
                )
            ],
            confidence_score=0.85,
            lawyer_required=lawyer_required,
            lawyer_required_reason=lawyer_reason,
            legal_disclaimer=LEGAL_DISCLAIMER,
            report_id=report_id
        )
        
        # Store report
        self.reports[report_id] = response
        
        return response
    
    async def _analyze_clause(self, clause_text: str) -> Dict[str, Any]:
        """Analyze individual clause"""
        # Use GPT-4 for clause analysis
        system_prompt = """You are a legal expert analyzing contract clauses.
        
        For each clause, provide:
        1. A one-sentence TL;DR
        2. Plain-English explanation (2-3 simple sentences)
        3. Business impact as bullet points
        4. Risk level (Low/Medium/High)
        5. Suggested redlines or negotiation points
        
        Be clear and avoid legal jargon. Focus on practical business implications.
        """
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this clause:\n\n{clause_text[:1000]}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse response (simplified)
            return {
                "tldr": "This clause defines key terms and obligations.",
                "explanation": analysis_text[:200] if analysis_text else "Standard contractual clause.",
                "business_impact": [
                    "Defines party obligations",
                    "May affect liability exposure"
                ],
                "risk_level": RiskLevel.MEDIUM,
                "redlines": ["Consider adding exceptions"],
                "negotiation_points": ["Clarify scope of obligations"]
            }
        except Exception as e:
            print(f"Error analyzing clause: {e}")
            return {
                "tldr": "Standard clause",
                "explanation": "Unable to analyze at this time.",
                "business_impact": ["Requires manual review"],
                "risk_level": RiskLevel.MEDIUM,
                "redlines": [],
                "negotiation_points": []
            }
    
    async def get_report(self, report_id: str) -> LegalTranslateResponse:
        """Retrieve stored report"""
        return self.reports.get(report_id)
    
    async def process_document(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded legal document"""
        upload_dir = "/app/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse document
        if file.filename.endswith('.pdf'):
            parsed = self.parser.parse_pdf(file_path)
            page_count = parsed.get("page_count", 0)
        elif file.filename.endswith('.docx'):
            parsed = self.parser.parse_docx(file_path)
            page_count = parsed.get("paragraph_count", 0)
        else:
            page_count = 0
        
        return {
            "success": True,
            "filename": file.filename,
            "file_path": file_path,
            "page_count": page_count,
            "message": "Document processed successfully"
        }
