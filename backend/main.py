from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.researcher import run_researcher

app = FastAPI(title="AgentFlow API", version="0.1.0")

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
    return {"status": "AgentFlow API is running"}

@app.post("/research")
def research_company(request: CompanyRequest):
    result = run_researcher(request.company_name)
    return {
        "company": request.company_name,
        "research": result
    }