"""
Founder Research Module - Service
"""
from .models import (
    FounderIngestRequest,
    FounderAnalysisResponse,
    FounderScorecard,
    Citation,
    Provenance,
    RiskLevel
)
from app.rag.pipeline import RAGPipeline
from app.scrapers.web_scraper import WebScraper
from app.parsers.document_parser import DocumentParser
from fastapi import UploadFile
import os
import uuid
from typing import Dict, Any

class FounderResearchService:
    def __init__(self):
        self.rag = RAGPipeline()
        self.scraper = WebScraper()
        self.parser = DocumentParser()
        self.reports = {}  # In-memory storage (would use DB in production)
    
    async def ingest_founder(self, request: FounderIngestRequest) -> Dict[str, Any]:
        """Ingest founder data from multiple sources"""
        collection_name = f"founder_{request.founder_name.replace(' ', '_').lower()}"
        documents = []
        metadatas = []
        ids = []
        
        # Scrape LinkedIn if provided
        if request.linkedin_url:
            linkedin_data = await self.scraper.scrape_linkedin(str(request.linkedin_url))
            if linkedin_data and not linkedin_data.get("error"):
                doc_text = f"LinkedIn Profile: {linkedin_data.get('name', '')} - {linkedin_data.get('headline', '')}"
                documents.append(doc_text)
                metadatas.append({
                    "source": "linkedin",
                    "url": str(request.linkedin_url)
                })
                ids.append(str(uuid.uuid4()))
        
        # Scrape Twitter if provided
        if request.twitter_url:
            twitter_data = await self.scraper.scrape_twitter(str(request.twitter_url))
            if twitter_data and not twitter_data.get("error"):
                doc_text = f"Twitter Profile: {request.founder_name}"
                documents.append(doc_text)
                metadatas.append({
                    "source": "twitter",
                    "url": str(request.twitter_url)
                })
                ids.append(str(uuid.uuid4()))
        
        # Process pitch deck if provided
        if request.pitch_deck_path and os.path.exists(request.pitch_deck_path):
            pdf_data = self.parser.parse_pdf(request.pitch_deck_path)
            chunks = self.parser.chunk_text(pdf_data["full_text"])
            for i, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append({
                    "source": "pitch_deck",
                    "page": i + 1
                })
                ids.append(str(uuid.uuid4()))
        
        # Add user notes
        if request.user_notes:
            documents.append(request.user_notes)
            metadatas.append({
                "source": "user_notes",
                "type": "commentary"
            })
            ids.append(str(uuid.uuid4()))
        
        # Store in vector database
        if documents:
            success = self.rag.add_documents(
                collection_name=collection_name,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            return {
                "success": success,
                "collection_name": collection_name,
                "documents_ingested": len(documents),
                "message": "Founder data ingested successfully"
            }
        
        return {
            "success": False,
            "message": "No data to ingest"
        }
    
    async def analyze_founder(self, founder_name: str, report_id: str) -> FounderAnalysisResponse:
        """Analyze founder and generate assessment"""
        collection_name = f"founder_{founder_name.replace(' ', '_').lower()}"
        
        # System prompt for founder analysis
        system_prompt = """You are an expert private equity analyst specializing in founder due diligence.
        
        Analyze the provided information about the founder and generate a comprehensive assessment.
        Focus on:
        - Leadership capabilities
        - Execution track record
        - Domain expertise
        - Risk factors
        - Signal strength (quality of available data)
        
        Be factual, cite sources, and clearly distinguish between verified facts and inferences.
        Highlight any red flags such as job hopping, inconsistencies, or unrealistic claims.
        """
        
        query = f"Analyze {founder_name} for private equity investment consideration"
        
        # Perform RAG query
        rag_result = self.rag.rag_query(
            collection_name=collection_name,
            query=query,
            system_prompt=system_prompt,
            top_k=10
        )
        
        # Generate scorecard (simplified - would use more sophisticated analysis)
        scorecard = FounderScorecard(
            leadership=7.5,
            execution=8.0,
            domain_fit=7.0,
            risk=3.5,
            signal_strength=6.5
        )
        
        # Calculate risk level based on scorecard
        avg_risk = scorecard.risk
        if avg_risk < 4:
            risk_level = RiskLevel.LOW
        elif avg_risk < 7:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.HIGH
        
        # Create citations from sources
        citations = [
            Citation(
                source=source.get("source", "Unknown"),
                url=source.get("url"),
                page=source.get("page"),
                confidence=source.get("confidence", 0.8)
            )
            for source in rag_result.get("sources", [])
        ]
        
        # Create analysis response
        analysis = FounderAnalysisResponse(
            summary=rag_result.get("response", "Analysis unavailable"),
            key_points=[
                "Strong technical background",
                "Prior startup experience",
                "Industry connections"
            ],
            risk_level=risk_level,
            scorecard=scorecard,
            key_strengths=[
                "Proven track record in similar domain",
                "Strong execution capabilities"
            ],
            key_risks=[
                "Limited fundraising experience",
                "Small team size"
            ],
            suggested_questions=[
                "What was your role in the previous exit?",
                "How do you plan to scale the team?",
                "What are the key milestones for the next 12 months?"
            ],
            citations=citations,
            provenance=Provenance(
                retrieved_facts=[],
                inferences=[],
                user_commentary=[]
            ),
            confidence_score=rag_result.get("confidence", 0.7),
            report_id=report_id
        )
        
        # Store report
        self.reports[report_id] = analysis
        
        return analysis
    
    async def get_report(self, report_id: str) -> FounderAnalysisResponse:
        """Retrieve a stored report"""
        return self.reports.get(report_id)
    
    async def process_pitch_deck(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded pitch deck"""
        # Save file temporarily
        upload_dir = "/app/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse PDF
        pdf_data = self.parser.parse_pdf(file_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "page_count": pdf_data.get("page_count", 0),
            "file_path": file_path,
            "message": "Pitch deck processed successfully"
        }
