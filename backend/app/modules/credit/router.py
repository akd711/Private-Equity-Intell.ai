"""
Credit Facility Analysis Module - Router
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from .models import CreditAnalyzeRequest, CreditAnalysisResponse
from .service import CreditAnalysisService
import uuid

router = APIRouter()
service = CreditAnalysisService()

@router.post("/analyze", response_model=CreditAnalysisResponse)
async def analyze_credit_facility(request: CreditAnalyzeRequest):
    """
    Analyze credit facility agreement
    """
    try:
        if not request.document_path and not request.document_text and not request.agreement_url:
            raise HTTPException(
                status_code=400,
                detail="document_path, document_text, or agreement_url must be provided"
            )
        
        report_id = str(uuid.uuid4())
        result = await service.analyze_credit_facility(request, report_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/{report_id}", response_model=CreditAnalysisResponse)
async def get_credit_report(report_id: str):
    """
    Retrieve a credit analysis report by ID
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

@router.post("/upload-agreement")
async def upload_credit_agreement(file: UploadFile = File(...)):
    """
    Upload credit facility agreement for processing
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        result = await service.process_agreement(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
