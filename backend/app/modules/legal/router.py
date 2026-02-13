"""
Legal Assistant Module - Router
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from .models import LegalTranslateRequest, LegalTranslateResponse
from .service import LegalAssistantService
import uuid

router = APIRouter()
service = LegalAssistantService()

@router.post("/translate", response_model=LegalTranslateResponse)
async def translate_legal_document(request: LegalTranslateRequest):
    """
    Translate legal document to plain English
    """
    try:
        if not request.document_path and not request.document_text:
            raise HTTPException(
                status_code=400,
                detail="Either document_path or document_text must be provided"
            )
        
        report_id = str(uuid.uuid4())
        result = await service.translate_document(request, report_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/{report_id}", response_model=LegalTranslateResponse)
async def get_legal_report(report_id: str):
    """
    Retrieve a legal translation report by ID
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

@router.post("/upload-document")
async def upload_legal_document(file: UploadFile = File(...)):
    """
    Upload legal document for processing
    """
    try:
        allowed_extensions = ['.pdf', '.docx', '.txt']
        if not any(file.filename.endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOCX, and TXT files are supported"
            )
        
        result = await service.process_document(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
