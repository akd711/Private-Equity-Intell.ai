"""
Document parsing utilities for PDF, DOCX, and other formats
"""
import fitz  # PyMuPDF
from docx import Document
from typing import List, Dict, Any
import re

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        """Parse PDF and extract text with page numbers"""
        try:
            doc = fitz.open(file_path)
            pages = []
            full_text = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                pages.append({
                    "page_number": page_num + 1,
                    "text": text
                })
                full_text.append(text)
            
            doc.close()
            
            return {
                "pages": pages,
                "full_text": "\n\n".join(full_text),
                "page_count": len(pages)
            }
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return {"pages": [], "full_text": "", "page_count": 0}
    
    @staticmethod
    def parse_docx(file_path: str) -> Dict[str, Any]:
        """Parse DOCX and extract text"""
        try:
            doc = Document(file_path)
            paragraphs = []
            full_text = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
                    full_text.append(para.text)
            
            return {
                "paragraphs": paragraphs,
                "full_text": "\n\n".join(full_text),
                "paragraph_count": len(paragraphs)
            }
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return {"paragraphs": [], "full_text": "", "paragraph_count": 0}
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # Try to find a natural break point (sentence end)
            if end < text_length:
                # Look for sentence endings
                chunk = text[start:end]
                last_period = max(
                    chunk.rfind('. '),
                    chunk.rfind('.\n'),
                    chunk.rfind('? '),
                    chunk.rfind('! ')
                )
                if last_period > 0:
                    end = start + last_period + 1
            
            chunks.append(text[start:end])
            start = end - overlap if end < text_length else end
        
        return chunks
    
    @staticmethod
    def extract_clauses(text: str) -> List[Dict[str, Any]]:
        """Extract legal clauses from text"""
        # Simple clause detection based on numbered sections or headers
        clauses = []
        
        # Split by common legal section patterns
        patterns = [
            r'\n\s*\d+\.\s+[A-Z]',  # Numbered sections
            r'\n\s*\([a-z]\)\s+',    # Lettered subsections
            r'\n\s*Article\s+\d+',   # Article sections
            r'\n\s*Section\s+\d+'    # Section headers
        ]
        
        combined_pattern = '|'.join(patterns)
        sections = re.split(combined_pattern, text)
        
        for i, section in enumerate(sections):
            if section.strip():
                clauses.append({
                    "clause_id": i + 1,
                    "text": section.strip(),
                    "type": "general"  # Would need NLP to classify properly
                })
        
        return clauses if clauses else [{"clause_id": 1, "text": text, "type": "general"}]
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\'\/]', '', text)
        return text.strip()
