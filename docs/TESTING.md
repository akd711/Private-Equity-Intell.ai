# Testing Guide

## Overview

This guide covers testing strategies for PE Intelligence AI.

## Test Structure

```
backend/
├── tests/
│   ├── test_founder.py
│   ├── test_legal.py
│   ├── test_credit.py
│   └── test_rag.py
frontend/
├── __tests__/
│   ├── components/
│   └── pages/
```

## Backend Testing

### Setup

```bash
cd backend
pip install pytest pytest-asyncio pytest-cov
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific module
pytest tests/test_founder.py

# Verbose output
pytest -v
```

### Example Test

```python
# tests/test_founder.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_founder_analyze():
    response = client.post(
        "/api/founder/analyze",
        params={"founder_name": "Test Founder"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "scorecard" in data
    assert data["confidence_score"] > 0

def test_founder_ingest():
    payload = {
        "founder_name": "John Doe",
        "consent_obtained": True
    }
    response = client.post("/api/founder/ingest", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True
```

## Frontend Testing

### Setup

```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

### Run Tests

```bash
# Run tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Example Test

```typescript
// __tests__/components/Button.test.tsx
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/button';

describe('Button', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

## Integration Tests

### Test RAG Pipeline

```python
def test_rag_pipeline():
    from app.rag.pipeline import RAGPipeline
    
    rag = RAGPipeline()
    
    # Test embedding generation
    embeddings = rag.generate_embeddings(["test text"])
    assert len(embeddings) > 0
    assert len(embeddings[0]) == 1536
    
    # Test document addition
    success = rag.add_documents(
        collection_name="test",
        documents=["doc1", "doc2"],
        metadatas=[{"source": "test"}] * 2,
        ids=["1", "2"]
    )
    assert success is True
```

## E2E Testing

### Playwright (Recommended)

```bash
cd frontend
npm install --save-dev @playwright/test
npx playwright install
```

```typescript
// e2e/founder.spec.ts
import { test, expect } from '@playwright/test';

test('founder analysis flow', async ({ page }) => {
  await page.goto('http://localhost:3000/dashboard/founder');
  
  await page.fill('[name="founderName"]', 'John Doe');
  await page.click('button:has-text("Analyze Founder")');
  
  await expect(page.locator('text=Analysis Results')).toBeVisible();
});
```

## Mock Data

Create mock data for testing:

```python
# tests/fixtures.py
MOCK_FOUNDER_RESPONSE = {
    "summary": "Test summary",
    "scorecard": {
        "leadership": 7.5,
        "execution": 8.0,
        "domain_fit": 7.0,
        "risk": 3.5,
        "signal_strength": 6.5
    },
    "risk_level": "Medium",
    "confidence_score": 0.8
}
```

## Test Coverage Goals

- **Backend**: >80% coverage
- **Frontend Components**: >70% coverage
- **Critical Paths**: 100% coverage

## CI/CD Testing

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: |
          cd backend
          pytest

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm test
```

## Manual Testing Checklist

### Founder Module
- [ ] Upload pitch deck
- [ ] Enter LinkedIn URL
- [ ] Enter Twitter URL
- [ ] Add user notes
- [ ] Run analysis
- [ ] View scorecard
- [ ] Check citations

### Legal Module
- [ ] Upload PDF document
- [ ] Upload DOCX document
- [ ] View clause analysis
- [ ] Check risk levels
- [ ] Verify legal disclaimer

### Credit Module
- [ ] Upload credit agreement
- [ ] View loan details
- [ ] Check covenant analysis
- [ ] Review risk heatmap
- [ ] Verify hidden costs

## Performance Testing

```bash
# Use Apache Bench
ab -n 100 -c 10 http://localhost:8000/health

# Use wrk
wrk -t12 -c400 -d30s http://localhost:8000/health
```

## Security Testing

- [ ] SQL injection attempts
- [ ] XSS attempts
- [ ] File upload validation
- [ ] Rate limiting
- [ ] Authentication bypass attempts

---

For more information, see the main README and API documentation.
