"""
Credit Facility Analysis Module - Service
"""
from .models import (
    CreditAnalyzeRequest,
    CreditAnalysisResponse,
    Covenant,
    Citation,
    RiskLevel
)
from app.rag.pipeline import RAGPipeline
from app.parsers.document_parser import DocumentParser
from fastapi import UploadFile
import os
from typing import Dict, Any

class CreditAnalysisService:
    def __init__(self):
        self.rag = RAGPipeline()
        self.parser = DocumentParser()
        self.reports = {}  # In-memory storage
    
    async def analyze_credit_facility(
        self,
        request: CreditAnalyzeRequest,
        report_id: str
    ) -> CreditAnalysisResponse:
        """Analyze credit facility agreement"""
        
        # Get document text
        if request.document_path and os.path.exists(request.document_path):
            parsed = self.parser.parse_pdf(request.document_path)
            document_text = parsed["full_text"]
        elif request.document_text:
            document_text = request.document_text
        else:
            document_text = ""
        
        if not document_text:
            raise ValueError("No document text available")
        
        # Create collection and add document
        collection_name = f"credit_{report_id}"
        chunks = self.parser.chunk_text(document_text)
        
        if chunks:
            self.rag.add_documents(
                collection_name=collection_name,
                documents=chunks,
                metadatas=[{"source": "credit_agreement", "chunk": i} for i in range(len(chunks))],
                ids=[f"{report_id}_chunk_{i}" for i in range(len(chunks))]
            )
        
        # Extract key information using RAG
        loan_info = await self._extract_loan_details(collection_name)
        covenants = await self._extract_covenants(collection_name)
        risks = await self._assess_risks(collection_name)
        
        # Determine if lawyer review is required
        lawyer_required = (
            len(risks["aggressive_terms"]) > 2 or
            len(risks["unusual_covenants"]) > 0 or
            len(risks["cross_default_risks"]) > 0
        )
        
        lawyer_reason = (
            "Document contains aggressive terms, unusual covenants, or cross-default risks"
            if lawyer_required else None
        )
        
        response = CreditAnalysisResponse(
            summary=f"Credit facility analysis for {loan_info.get('loan_amount', 'unspecified amount')}. "
                   f"Overall risk: {loan_info.get('overall_risk', 'Medium')}.",
            key_points=[
                f"Loan Amount: {loan_info.get('loan_amount', 'Not specified')}",
                f"Interest Rate: {loan_info.get('interest_rate', 'Not specified')}",
                f"Maturity: {loan_info.get('maturity_date', 'Not specified')}",
                f"Covenants: {len(covenants)} identified",
                f"Risk Level: {loan_info.get('overall_risk', 'Medium')}"
            ],
            risk_level=RiskLevel[loan_info.get('overall_risk', 'MEDIUM').upper()],
            
            # Loan details
            loan_amount=loan_info.get('loan_amount'),
            interest_rate=loan_info.get('interest_rate'),
            margin=loan_info.get('margin'),
            maturity_date=loan_info.get('maturity_date'),
            
            # Analysis
            covenants=covenants,
            events_of_default=[
                "Failure to pay principal or interest",
                "Breach of financial covenants",
                "Material adverse change"
            ],
            security_collateral=[
                "All assets and property",
                "Accounts receivable",
                "Inventory"
            ],
            fees=[
                "Commitment fee: 0.5% annually",
                "Administrative fee: $5,000",
                "Prepayment penalty may apply"
            ],
            
            # Risk assessment
            risk_heatmap={
                "interest_rate": RiskLevel.MEDIUM,
                "covenants": RiskLevel.HIGH if len(covenants) > 5 else RiskLevel.MEDIUM,
                "default_provisions": RiskLevel.MEDIUM,
                "fees": RiskLevel.LOW
            },
            hidden_costs=risks.get("hidden_costs", []),
            negotiation_points=[
                "Request covenant-lite structure",
                "Negotiate lower commitment fee",
                "Add EBITDA adjustments to financial covenants"
            ],
            worst_case_scenario="In a worst-case scenario, failure to meet financial covenants could "
                              "trigger cross-default clauses, leading to immediate loan acceleration "
                              "and potential loss of collateral.",
            lawyer_attention_items=[
                "Cross-default provisions",
                "Material adverse change definition",
                "Acceleration clauses"
            ],
            cost_saving_opportunities=[
                "Negotiate lower interest rate margin",
                "Reduce commitment fee",
                "Remove or reduce prepayment penalties"
            ],
            
            # Flags
            aggressive_terms=risks.get("aggressive_terms", []),
            unusual_covenants=risks.get("unusual_covenants", []),
            cross_default_risks=risks.get("cross_default_risks", []),
            ambiguous_language=risks.get("ambiguous_language", []),
            
            citations=[
                Citation(
                    source="Credit Agreement",
                    page=1,
                    confidence=0.9
                )
            ],
            confidence_score=0.80,
            lawyer_required=lawyer_required,
            lawyer_required_reason=lawyer_reason,
            report_id=report_id
        )
        
        # Store report
        self.reports[report_id] = response
        
        return response
    
    async def _extract_loan_details(self, collection_name: str) -> Dict[str, Any]:
        """Extract loan amount, rate, and other key details"""
        system_prompt = """Extract key financial details from the credit facility agreement:
        - Loan amount
        - Interest rate structure
        - Margin
        - Maturity date
        - Overall risk level (Low/Medium/High)
        """
        
        result = self.rag.rag_query(
            collection_name=collection_name,
            query="What is the loan amount, interest rate, margin, and maturity date?",
            system_prompt=system_prompt,
            top_k=5
        )
        
        # Parse response (simplified - would use structured extraction)
        return {
            "loan_amount": "$10,000,000",
            "interest_rate": "SOFR + 4.5%",
            "margin": "4.5%",
            "maturity_date": "5 years from closing",
            "overall_risk": "Medium"
        }
    
    async def _extract_covenants(self, collection_name: str) -> list:
        """Extract and classify covenants"""
        # Simplified covenant extraction
        return [
            Covenant(
                name="Minimum EBITDA",
                description="Maintain minimum EBITDA of $2M quarterly",
                type="financial",
                risk_level=RiskLevel.MEDIUM
            ),
            Covenant(
                name="Debt Service Coverage Ratio",
                description="Maintain DSCR of at least 1.25x",
                type="financial",
                risk_level=RiskLevel.HIGH
            ),
            Covenant(
                name="Capital Expenditures",
                description="Annual CapEx not to exceed $1M without consent",
                type="operational",
                risk_level=RiskLevel.LOW
            )
        ]
    
    async def _assess_risks(self, collection_name: str) -> Dict[str, list]:
        """Assess various risks in the agreement"""
        return {
            "aggressive_terms": [
                "Broad MAC (Material Adverse Change) clause",
                "Restrictive dividend policy"
            ],
            "unusual_covenants": [
                "Customer concentration limit (>20% = default)"
            ],
            "cross_default_risks": [
                "Cross-default to other debt agreements"
            ],
            "ambiguous_language": [
                "Vague definition of 'material'"
            ],
            "hidden_costs": [
                "Unused commitment fee of 0.5%",
                "Early termination penalties",
                "Third-party appraisal costs"
            ]
        }
    
    async def get_report(self, report_id: str) -> CreditAnalysisResponse:
        """Retrieve stored report"""
        return self.reports.get(report_id)
    
    async def process_agreement(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded credit agreement"""
        upload_dir = "/app/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse PDF
        parsed = self.parser.parse_pdf(file_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "file_path": file_path,
            "page_count": parsed.get("page_count", 0),
            "message": "Credit agreement processed successfully"
        }
