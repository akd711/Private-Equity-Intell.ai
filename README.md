# PE Intelligence AI

**AI-powered intelligence platform for private equity professionals**

PE Intelligence AI combines advanced RAG (Retrieval-Augmented Generation) architecture with specialized modules to help private equity professionals make informed investment decisions.

## 🎯 Overview

This platform combines three core AI-powered modules:

1. **Founder Research**: Automated founder due diligence from LinkedIn, Twitter, and pitch decks
2. **Legal Document Translator**: Plain-English translation of legal documents with risk assessment
3. **Credit Facility Analysis**: Comprehensive credit agreement analysis with hidden cost identification

## ✨ Features

### Founder Research Module
- Multi-source data ingestion (LinkedIn, Twitter, pitch decks)
- Automated founder assessment with 5-point scorecard
- Red flag detection (job hopping, inconsistencies, unrealistic claims)
- Key strengths and risks identification
- Suggested due diligence questions
- Confidence scoring and source citations

### Legal Document Translator
- Clause-by-clause plain-English translation
- Risk level assessment (Low/Medium/High)
- TL;DR summaries for each clause
- Business impact analysis
- Suggested redlines and negotiation points
- Lawyer escalation recommendations
- Legal disclaimer and compliance warnings

### Credit Facility Analysis
- Automated extraction of key terms (loan amount, rate, margin, maturity)
- Financial and operational covenant identification
- Risk heatmap visualization
- Hidden cost analysis
- Negotiation leverage points
- Worst-case scenario modeling
- Cost-saving opportunity detection
- Aggressive terms and unusual covenant flagging

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │   Founder    │    Legal     │    Credit    │            │
│  │   Research   │  Translator  │   Analysis   │            │
│  └──────────────┴──────────────┴──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (FastAPI + Python)                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              RAG Pipeline                             │  │
│  │  Parsing → Chunking → Embedding → Vector DB →        │  │
│  │  Retrieval → LLM Generation → Validation             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
    ┌──────────────────┐    ┌──────────────────┐
    │   PostgreSQL     │    │    ChromaDB      │
    │   (pgvector)     │    │  (Vector Store)  │
    └──────────────────┘    └──────────────────┘
```

### RAG Pipeline

1. **Document Ingestion**: Parse PDFs, DOCX, and web content
2. **Text Cleaning & Normalization**: Remove artifacts and normalize formatting
3. **Chunking with Metadata**: Split documents into semantic chunks
4. **Embeddings Generation**: Use OpenAI text-embedding-3-large
5. **Vector Storage**: Store in ChromaDB with metadata
6. **Retrieval**: Configurable top-K retrieval with distance scoring
7. **LLM Generation**: GPT-4 for analysis with context
8. **Post-processing**: Validation and confidence scoring

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: Shadcn/ui (Radix UI)
- **State Management**: React Hooks
- **API Client**: Axios

### Backend
- **Framework**: FastAPI (Python)
- **Language**: Python 3.11+
- **AI/ML**: 
  - OpenAI GPT-4 for generation
  - LangChain for RAG orchestration
  - ChromaDB for vector storage
  - OpenAI embeddings (text-embedding-3-large)

### Document Processing
- **PDF**: PyMuPDF
- **Word**: python-docx
- **Multi-format**: Unstructured library

### Web Scraping
- **Browser Automation**: Playwright
- **Parsing**: BeautifulSoup4
- **Rate Limiting**: Built-in

### Database
- **Primary**: PostgreSQL with pgvector extension
- **ORM**: Prisma (frontend), SQLAlchemy (backend)
- **Vector DB**: ChromaDB

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions (recommended)

## 📦 Project Structure

```
Private-Equity-Intell.ai/
├── frontend/                 # Next.js frontend
│   ├── app/
│   │   ├── (dashboard)/     # Dashboard routes
│   │   │   ├── page.tsx     # Dashboard home
│   │   │   ├── founder/     # Founder research
│   │   │   ├── legal/       # Legal translator
│   │   │   ├── credit/      # Credit analysis
│   │   │   ├── reports/     # Historical reports
│   │   │   └── settings/    # User settings
│   │   ├── api/             # API routes
│   │   ├── globals.css
│   │   └── layout.tsx
│   ├── components/          # React components
│   │   └── ui/              # Shadcn/ui components
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   └── utils.ts         # Utilities
│   ├── public/              # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── Dockerfile
├── backend/                  # Python FastAPI service
│   ├── app/
│   │   ├── modules/
│   │   │   ├── founder/     # Founder research module
│   │   │   │   ├── models.py
│   │   │   │   ├── router.py
│   │   │   │   └── service.py
│   │   │   ├── legal/       # Legal assistant module
│   │   │   │   ├── models.py
│   │   │   │   ├── router.py
│   │   │   │   └── service.py
│   │   │   └── credit/      # Credit analysis module
│   │   │       ├── models.py
│   │   │       ├── router.py
│   │   │       └── service.py
│   │   ├── rag/
│   │   │   └── pipeline.py  # RAG implementation
│   │   ├── scrapers/
│   │   │   └── web_scraper.py
│   │   └── parsers/
│   │       └── document_parser.py
│   ├── requirements.txt
│   ├── main.py              # FastAPI app
│   └── Dockerfile
├── database/
│   └── schema.prisma        # Prisma schema
├── docker-compose.yml       # Docker orchestration
├── .env.example             # Environment variables template
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/akd711/Private-Equity-Intell.ai.git
cd Private-Equity-Intell.ai
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key and other configurations:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://pe_user:pe_password@postgres:5432/pe_intelligence
CHROMA_HOST=chroma
CHROMA_PORT=8000
```

### 3. Start with Docker Compose

```bash
docker-compose up -d
```

This will start:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **ChromaDB**: http://localhost:8001

### 4. Access the Application

Open your browser and navigate to:
- **Dashboard**: http://localhost:3000

### 5. API Documentation

FastAPI provides automatic API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Development Setup

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend API will be available at http://localhost:8000

### Database Setup

```bash
# Initialize Prisma
cd database
npx prisma generate
npx prisma db push
```

## 📋 Environment Variables

Create a `.env` file in the root directory with these variables:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/pe_intelligence

# Vector Database
CHROMA_HOST=localhost
CHROMA_PORT=8001

# Auth
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=http://localhost:3000

# Storage
BLOB_READ_WRITE_TOKEN=your_blob_token_here

# Rate Limiting
RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_WINDOW_MS=60000

# Feature Flags
ENABLE_LINKEDIN_SCRAPING=false
ENABLE_TWITTER_SCRAPING=false

# Backend
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_PORT=8000
```

## 📖 API Documentation

### Founder Research API

**POST /api/founder/ingest**
```json
{
  "founder_name": "John Doe",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "twitter_url": "https://twitter.com/johndoe",
  "user_notes": "Optional notes",
  "consent_obtained": true
}
```

**POST /api/founder/analyze?founder_name=John Doe**

**GET /api/founder/report/{report_id}**

### Legal Assistant API

**POST /api/legal/translate**
```json
{
  "document_path": "/path/to/document.pdf",
  "document_type": "contract"
}
```

**GET /api/legal/report/{report_id}**

### Credit Analysis API

**POST /api/credit/analyze**
```json
{
  "document_path": "/path/to/agreement.pdf"
}
```

**GET /api/credit/report/{report_id}**

## 🔒 Security & Compliance

### Data Privacy
- All data collection requires explicit user consent
- PII handling follows GDPR guidelines
- Data retention policies configurable
- Audit logs for all operations

### Security Features
- Authentication via NextAuth.js
- Role-based access control
- Rate limiting on all endpoints
- Input sanitization to prevent injection attacks
- Encryption at rest for stored documents
- CORS configuration for API security

### Legal Disclaimers
- Clear "not legal advice" warnings on all legal analyses
- Lawyer escalation recommendations for high-risk content
- Confidence scores on all AI-generated content
- Source attribution and citation tracking

### Consent Management
- Web scraping requires explicit user consent
- robots.txt compliance for scraping
- Rate limiting to respect platform ToS
- Privacy warnings before data collection

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

## 🚢 Deployment

### Frontend Deployment (Vercel)
1. Push your code to GitHub
2. Import repository in Vercel
3. Set environment variables
4. Deploy

### Backend Deployment (Railway/Render)
1. Create new project
2. Connect GitHub repository
3. Set environment variables
4. Deploy from `backend/` directory

### Database Deployment
- **Supabase**: Managed PostgreSQL with pgvector
- **Railway**: PostgreSQL addon
- **AWS RDS**: PostgreSQL with pgvector extension

## 📊 Monitoring

### Metrics Tracked
- Analysis accuracy
- Hallucination rate
- Source coverage ratio
- Latency (p50, p95, p99)
- User ratings
- Cost per analysis

### Logging
- All API requests/responses logged
- Error tracking with stack traces
- Audit logs for compliance
- Performance metrics

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

ISC License

## ⚠️ Disclaimers

### Legal Disclaimer
This platform provides AI-generated analysis for informational purposes only. It does not constitute legal, financial, or investment advice. Always consult qualified professionals before making legal or financial decisions.

### AI Disclaimer
The analyses provided by this platform use AI models that may:
- Contain errors or hallucinations
- Miss important information
- Misinterpret context
- Provide incorrect assessments

Always verify AI-generated content with original sources and expert review.

## 📞 Support

For issues, questions, or contributions:
- **GitHub Issues**: [Report a bug](https://github.com/akd711/Private-Equity-Intell.ai/issues)
- **Documentation**: See this README and inline code documentation

## 🗺️ Roadmap

- [ ] Enhanced founder social media analysis
- [ ] Integration with CRM systems
- [ ] Advanced financial modeling for credit analysis
- [ ] Multi-language support for legal documents
- [ ] Custom AI model fine-tuning
- [ ] Mobile app development
- [ ] Real-time collaboration features
- [ ] Advanced reporting and analytics dashboard

---

**Built with ❤️ for private equity professionals**