"""
Founder Research Module - Router
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from .models import FounderIngestRequest, FounderAnalysisResponse
from .service import FounderResearchService
from typing import Optional
import uuid

router = APIRouter()
service = FounderResearchService()

@router.post("/ingest", response_model=dict)
async def ingest_founder_data(request: FounderIngestRequest):
    """
    Ingest founder data from multiple sources
    """
    try:
        if not request.consent_obtained:
            raise HTTPException(
                status_code=400,
                detail="User consent required for data collection"
            )
        
        result = await service.ingest_founder(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze", response_model=FounderAnalysisResponse)
async def analyze_founder(
    founder_name: str,
    report_id: Optional[str] = None
):
    """
    Analyze founder and generate assessment report
    """
    try:
        if not report_id:
            report_id = str(uuid.uuid4())
        
        analysis = await service.analyze_founder(founder_name, report_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/{report_id}", response_model=FounderAnalysisResponse)
async def get_founder_report(report_id: str):
    """
    Retrieve a founder analysis report by ID
    """
    try:
        report = await service.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-pitch-deck")
async def upload_pitch_deck(file: UploadFile = File(...)):
    """
    Upload and process pitch deck PDF
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        result = await service.process_pitch_deck(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
