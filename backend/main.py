from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.researcher import run_researcher
from pipeline import run_pipeline

app = FastAPI(title="AgentFlow API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanyRequest(BaseModel):
    company_name: str

@app.get("/")
def health_check():
    return {"status": "AgentFlow API is running", "version": "0.2.0"}

@app.post("/research")
def research_only(request: CompanyRequest):
    result = run_researcher(request.company_name)
    return {
        "company": request.company_name,
        "research": result
    }

@app.post("/analyse")
def full_pipeline(request: CompanyRequest):
    try:
        result = run_pipeline(request.company_name)
        return {
            "company": request.company_name,
            "research": result["research"],
            "analysis": result["analysis"],
            "report": result["report"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))