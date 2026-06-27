from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
llm = OllamaLLM(model="llama3", base_url=OLLAMA_HOST)

analyst_prompt = PromptTemplate(
    input_variables=["company_name", "research"],
    template="""
    You are a senior financial risk analyst. Based on the research provided below,
    produce a structured financial and risk analysis.

    Company: {company_name}
    Research Data: {research}

    Provide the following in structured format:
    1. Financial Health Assessment
       - Revenue trajectory (growing/stable/declining)
       - Profitability indicators
       - Debt and liquidity concerns if any

    2. Risk Assessment
       - Market risks (competition, disruption)
       - Operational risks (supply chain, key person dependency)
       - Regulatory and legal risks
       - Macroeconomic risks

    3. Competitive Position
       - Key advantages
       - Key vulnerabilities

    4. Overall Risk Rating
       - Rate as: LOW / MEDIUM / HIGH / CRITICAL
       - One paragraph justification for the rating

    Be analytical, precise, and evidence-based. Flag uncertainties explicitly.
    """
)

chain = analyst_prompt | llm | StrOutputParser()

def run_analyst(company_name: str, research: str) -> str:
    print(f"\n[ANALYST AGENT] Starting analysis on: {company_name}")
    output = chain.invoke({
        "company_name": company_name,
        "research": research
    })
    print(f"[ANALYST AGENT] Analysis complete.")
    return output

if __name__ == "__main__":
    test_research = """
    Apple Inc is a technology company founded in 1976.
    It makes iPhones, Macs, and services like Apple Music.
    Revenue exceeds $380 billion annually.
    """
    output = run_analyst("Apple Inc", test_research)
    print("\n--- ANALYST OUTPUT ---")
    print(output)