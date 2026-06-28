from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import logging
from agents.researcher import run_researcher
from pipeline import run_pipeline
from fastapi.responses import StreamingResponse
from utils.pdf_generator import generate_pdf
from io import BytesIO

# Set up logging so you can see what is happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AgentFlow API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanyRequest(BaseModel):
    company_name: str

    # Validation — reject empty or too-short input
    def validate_input(self):
        if not self.company_name or len(self.company_name.strip()) < 2:
            raise ValueError("Company name must be at least 2 characters")
        if len(self.company_name) > 100:
            raise ValueError("Company name too long. Max 100 characters.")
        return self.company_name.strip()

@app.get("/")
def health_check():
    return {
        "status": "AgentFlow API is running",
        "version": "0.3.0",
        "agents": ["researcher", "analyst", "reporter"]
    }

@app.post("/research")
def research_only(request: CompanyRequest):
    try:
        company = request.validate_input()
        logger.info(f"Research request for: {company}")
        result = run_researcher(company)
        return {
            "company": company,
            "research": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Research failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Research agent failed. Check backend logs.")

@app.post("/analyse")
def full_pipeline(request: CompanyRequest):
    try:
        company = request.validate_input()
        logger.info(f"Full pipeline request for: {company}")

        start = time.time()
        result = run_pipeline(company)
        duration = round(time.time() - start, 2)

        logger.info(f"Pipeline complete for {company} in {duration}s")

        # Validate all three agents returned content
        if not result.get("research"):
            raise HTTPException(status_code=500, detail="Researcher agent returned empty output")
        if not result.get("analysis"):
            raise HTTPException(status_code=500, detail="Analyst agent returned empty output")
        if not result.get("report"):
            raise HTTPException(status_code=500, detail="Reporter agent returned empty output")

        return {
            "company": company,
            "research": result["research"],
            "analysis": result["analysis"],
            "report": result["report"],
            "duration_seconds": duration
        }

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Pipeline failed for {request.company_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")
    
@app.post("/export-pdf")
def export_pdf(request: CompanyRequest):
    try:
        company = request.validate_input()
        logger.info(f"PDF export request for: {company}")

        start = time.time()
        result = run_pipeline(company)
        duration = round(time.time() - start, 2)

        if not result.get("report"):
            raise HTTPException(status_code=500, detail="Pipeline returned empty report")

        pdf_bytes = generate_pdf(
            company=company,
            research=result["research"],
            analysis=result["analysis"],
            report=result["report"],
            duration=duration
        )

        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=agentflow_{company.replace(' ', '_')}_report.pdf"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF export failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")