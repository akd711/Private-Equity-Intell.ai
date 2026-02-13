# Quick Start Guide

Get PE Intelligence AI running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/akd711/Private-Equity-Intell.ai.git
cd Private-Equity-Intell.ai
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Required: OPENAI_API_KEY=sk-your-key-here
nano .env  # or use your preferred editor
```

### 3. Start the Application

```bash
# Start all services (frontend, backend, databases)
docker-compose up -d

# Check if services are running
docker-compose ps
```

### 4. Access the Application

Open your browser and navigate to:

- **Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. Use the Platform

#### Founder Research

1. Go to http://localhost:3000/dashboard/founder
2. Enter founder name (e.g., "John Doe")
3. Add LinkedIn URL, Twitter URL, or upload pitch deck (PDF)
4. Add optional notes
5. Click "Analyze Founder"
6. View scorecard, strengths, risks, and suggested questions

#### Legal Document Translator

1. Go to http://localhost:3000/dashboard/legal
2. Upload a legal document (PDF, DOCX, or TXT)
3. Click "Translate to Plain English"
4. Review clause-by-clause analysis
5. Check risk levels and suggested redlines

#### Credit Facility Analysis

1. Go to http://localhost:3000/dashboard/credit
2. Upload a credit agreement (PDF)
3. Click "Analyze Credit Facility"
4. Review loan details, covenants, and risk assessment
5. Check hidden costs and negotiation points

## Troubleshooting

### Services won't start

```bash
# Check Docker is running
docker --version

# View logs
docker-compose logs -f

# Restart services
docker-compose restart
```

### Can't connect to OpenAI

- Verify your API key in `.env` is correct
- Check your OpenAI account has credits
- Ensure API key has proper permissions

### Frontend can't reach backend

- Check `NEXT_PUBLIC_API_URL` in `.env`
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in backend

### Database connection failed

```bash
# Reset database
docker-compose down -v
docker-compose up -d

# Check database is running
docker-compose exec postgres pg_isready
```

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove all data (reset)
docker-compose down -v
```

## Development Mode

### Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Run Backend Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
# API available at http://localhost:8000
```

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [API Documentation](docs/API.md) for endpoint details
- Review [Architecture Documentation](docs/ARCHITECTURE.md)
- See [Deployment Guide](docs/DEPLOYMENT.md) for production deployment

## Demo Credentials

For testing authentication (basic setup):
- Email: `demo@example.com`
- Password: `demo`

**Note:** Update authentication implementation for production use!

## Support

- **Issues**: Open a GitHub issue
- **Documentation**: See `/docs` directory
- **API Docs**: http://localhost:8000/docs

---

**Enjoy using PE Intelligence AI! 🚀**
