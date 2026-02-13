from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from app.modules.founder import router as founder_router
from app.modules.legal import router as legal_router
from app.modules.credit import router as credit_router

app = FastAPI(
    title="PE Intelligence AI API",
    description="AI-powered intelligence platform for private equity professionals",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        os.getenv("NEXTAUTH_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(founder_router.router, prefix="/api/founder", tags=["Founder Research"])
app.include_router(legal_router.router, prefix="/api/legal", tags=["Legal Assistant"])
app.include_router(credit_router.router, prefix="/api/credit", tags=["Credit Analysis"])

@app.get("/")
async def root():
    return {
        "message": "PE Intelligence AI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
