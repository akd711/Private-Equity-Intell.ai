# API Documentation

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-api-domain.com`

## Authentication

Currently, the API uses basic authentication. Future versions will implement JWT-based authentication via NextAuth.js.

## API Endpoints

### Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Founder Research Module

### 1. Ingest Founder Data

**POST** `/api/founder/ingest`

Collect and index founder information from multiple sources.

**Request Body:**
```json
{
  "founder_name": "John Doe",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "twitter_url": "https://twitter.com/johndoe",
  "pitch_deck_path": "/path/to/deck.pdf",
  "user_notes": "Optional internal notes",
  "consent_obtained": true
}
```

**Response:**
```json
{
  "success": true,
  "collection_name": "founder_john_doe",
  "documents_ingested": 15,
  "message": "Founder data ingested successfully"
}
```

### 2. Analyze Founder

**POST** `/api/founder/analyze?founder_name={name}&report_id={id}`

Generate comprehensive founder assessment.

**Query Parameters:**
- `founder_name` (required): Name of the founder
- `report_id` (optional): Custom report ID

**Response:**
```json
{
  "summary": "Analysis summary...",
  "key_points": ["Point 1", "Point 2"],
  "risk_level": "Medium",
  "scorecard": {
    "leadership": 7.5,
    "execution": 8.0,
    "domain_fit": 7.0,
    "risk": 3.5,
    "signal_strength": 6.5
  },
  "key_strengths": ["Strength 1", "Strength 2"],
  "key_risks": ["Risk 1", "Risk 2"],
  "suggested_questions": ["Question 1", "Question 2"],
  "citations": [...],
  "provenance": {...},
  "confidence_score": 0.8,
  "report_id": "uuid"
}
```

### 3. Get Founder Report

**GET** `/api/founder/report/{report_id}`

Retrieve a previously generated founder report.

**Response:** Same as Analyze Founder response

### 4. Upload Pitch Deck

**POST** `/api/founder/upload-pitch-deck`

Upload a pitch deck PDF for processing.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (PDF file)

**Response:**
```json
{
  "success": true,
  "filename": "pitch_deck.pdf",
  "page_count": 15,
  "file_path": "/app/uploads/pitch_deck.pdf",
  "message": "Pitch deck processed successfully"
}
```

---

## Legal Assistant Module

### 1. Translate Legal Document

**POST** `/api/legal/translate`

Translate legal document to plain English with risk assessment.

**Request Body:**
```json
{
  "document_path": "/path/to/contract.pdf",
  "document_text": "Alternative: provide raw text",
  "document_type": "contract"
}
```

**Response:**
```json
{
  "summary": "Document analysis summary...",
  "key_points": ["Key point 1", "Key point 2"],
  "risk_level": "High",
  "clauses": [
    {
      "clause_id": 1,
      "type": "indemnity",
      "text": "Original clause text...",
      "tldr": "One sentence summary",
      "explanation": "Plain English explanation",
      "business_impact": ["Impact 1", "Impact 2"],
      "risk_level": "High",
      "page_number": 3,
      "redlines": ["Suggested change 1"],
      "negotiation_points": ["Negotiation tip 1"]
    }
  ],
  "redlines": ["Overall redline 1", "Overall redline 2"],
  "citations": [...],
  "confidence_score": 0.85,
  "lawyer_required": true,
  "lawyer_required_reason": "High-risk clauses detected",
  "legal_disclaimer": "⚠️ LEGAL DISCLAIMER...",
  "report_id": "uuid"
}
```

### 2. Get Legal Report

**GET** `/api/legal/report/{report_id}`

Retrieve a legal translation report.

**Response:** Same as Translate Legal Document response

### 3. Upload Legal Document

**POST** `/api/legal/upload-document`

Upload a legal document (PDF, DOCX, or TXT).

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (document file)

**Response:**
```json
{
  "success": true,
  "filename": "contract.pdf",
  "file_path": "/app/uploads/contract.pdf",
  "page_count": 25,
  "message": "Document processed successfully"
}
```

---

## Credit Analysis Module

### 1. Analyze Credit Facility

**POST** `/api/credit/analyze`

Comprehensive credit facility agreement analysis.

**Request Body:**
```json
{
  "document_path": "/path/to/credit_agreement.pdf",
  "document_text": "Alternative: raw text",
  "agreement_url": "Alternative: URL to agreement"
}
```

**Response:**
```json
{
  "summary": "Credit facility summary...",
  "key_points": ["Key finding 1", "Key finding 2"],
  "risk_level": "Medium",
  "loan_amount": "$10,000,000",
  "interest_rate": "SOFR + 4.5%",
  "margin": "4.5%",
  "maturity_date": "5 years from closing",
  "covenants": [
    {
      "name": "Minimum EBITDA",
      "description": "Maintain minimum EBITDA of $2M quarterly",
      "type": "financial",
      "risk_level": "Medium"
    }
  ],
  "events_of_default": ["Event 1", "Event 2"],
  "security_collateral": ["All assets", "Receivables"],
  "fees": ["Commitment fee: 0.5%", "Admin fee: $5,000"],
  "risk_heatmap": {
    "interest_rate": "Medium",
    "covenants": "High",
    "default_provisions": "Medium",
    "fees": "Low"
  },
  "hidden_costs": ["Hidden cost 1", "Hidden cost 2"],
  "negotiation_points": ["Point 1", "Point 2"],
  "worst_case_scenario": "Worst case description...",
  "lawyer_attention_items": ["Item 1", "Item 2"],
  "cost_saving_opportunities": ["Opportunity 1"],
  "aggressive_terms": ["Term 1", "Term 2"],
  "unusual_covenants": ["Covenant 1"],
  "cross_default_risks": ["Risk 1"],
  "ambiguous_language": ["Ambiguity 1"],
  "citations": [...],
  "confidence_score": 0.80,
  "lawyer_required": true,
  "lawyer_required_reason": "Aggressive terms detected",
  "report_id": "uuid"
}
```

### 2. Get Credit Report

**GET** `/api/credit/report/{report_id}`

Retrieve a credit analysis report.

**Response:** Same as Analyze Credit Facility response

### 3. Upload Credit Agreement

**POST** `/api/credit/upload-agreement`

Upload credit facility agreement PDF.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (PDF file)

**Response:**
```json
{
  "success": true,
  "filename": "credit_agreement.pdf",
  "file_path": "/app/uploads/credit_agreement.pdf",
  "page_count": 45,
  "message": "Credit agreement processed successfully"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Report not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

---

## Rate Limiting

- **Default**: 100 requests per minute per IP
- **Configuration**: Set via `RATE_LIMIT_MAX_REQUESTS` and `RATE_LIMIT_WINDOW_MS`

When rate limit is exceeded:
```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

---

## Interactive API Documentation

The backend provides interactive API documentation via Swagger UI and ReDoc:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- Browse all available endpoints
- View request/response schemas
- Test API calls directly
- Download OpenAPI specification

---

## SDK Usage Examples

### JavaScript/TypeScript

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Analyze founder
const analyzeFounder = async (founderName: string) => {
  const response = await api.post('/api/founder/analyze', null, {
    params: { founder_name: founderName }
  });
  return response.data;
};

// Translate legal document
const translateDocument = async (filePath: string) => {
  const response = await api.post('/api/legal/translate', {
    document_path: filePath,
    document_type: 'contract'
  });
  return response.data;
};
```

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Analyze founder
def analyze_founder(founder_name: str):
    response = requests.post(
        f"{BASE_URL}/api/founder/analyze",
        params={"founder_name": founder_name}
    )
    return response.json()

# Translate legal document
def translate_document(file_path: str):
    response = requests.post(
        f"{BASE_URL}/api/legal/translate",
        json={
            "document_path": file_path,
            "document_type": "contract"
        }
    )
    return response.json()
```

### cURL

```bash
# Analyze founder
curl -X POST "http://localhost:8000/api/founder/analyze?founder_name=John%20Doe"

# Upload and translate legal document
curl -X POST "http://localhost:8000/api/legal/upload-document" \
  -F "file=@contract.pdf"

curl -X POST "http://localhost:8000/api/legal/translate" \
  -H "Content-Type: application/json" \
  -d '{"document_path":"/app/uploads/contract.pdf"}'
```

---

## Pagination

Future versions will support pagination for list endpoints:

```
GET /api/reports?page=1&limit=20
```

---

## Webhooks

Future feature: Configure webhooks to receive notifications when analysis completes.

---

## API Versioning

Current version: `v1` (implicit)

Future versions will use URL versioning:
- `/api/v1/founder/analyze`
- `/api/v2/founder/analyze`

---

## Support

For API issues or feature requests:
- GitHub Issues: https://github.com/akd711/Private-Equity-Intell.ai/issues
- API Documentation: http://localhost:8000/docs
