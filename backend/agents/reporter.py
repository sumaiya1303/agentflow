from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = OllamaLLM(model="llama3")

reporter_prompt = PromptTemplate(
    input_variables=["company_name", "research", "analysis"],
    template="""
    You are a professional due diligence report writer for institutional investors.
    Using the research and analysis provided, write a complete due diligence report.

    Company: {company_name}
    Research: {research}
    Analysis: {analysis}

    Write the report in this exact structure:

    ================================================
    DUE DILIGENCE REPORT: {company_name}
    ================================================

    EXECUTIVE SUMMARY
    -----------------
    [2-3 sentence summary of the company and overall investment risk posture]

    COMPANY OVERVIEW
    ----------------
    [Key facts: what they do, business model, market position]

    FINANCIAL ASSESSMENT
    --------------------
    [Revenue, profitability, debt, liquidity summary]

    RISK ANALYSIS
    -------------
    [All identified risks by category with severity noted]

    COMPETITIVE POSITION
    --------------------
    [Advantages and vulnerabilities]

    OVERALL RISK RATING: [LOW / MEDIUM / HIGH / CRITICAL]
    ------------------------------------------------------
    [Justification paragraph]

    RECOMMENDATION
    --------------
    [Proceed with investment / Proceed with caution / Do not proceed]
    [One paragraph rationale]

    ================================================
    END OF REPORT
    ================================================

    Write professionally. Be direct. Avoid vague language.
    """
)

chain = reporter_prompt | llm | StrOutputParser()

def run_reporter(company_name: str, research: str, analysis: str) -> str:
    print(f"\n[REPORTER AGENT] Writing due diligence report for: {company_name}")
    output = chain.invoke({
        "company_name": company_name,
        "research": research,
        "analysis": analysis
    })
    print(f"[REPORTER AGENT] Report complete.")
    return output

if __name__ == "__main__":
    test_research = "Apple Inc makes iPhones and services. Revenue $380B annually."
    test_analysis = "Low risk. Strong cash position. Market leader. Minor regulatory exposure."
    output = run_reporter("Apple Inc", test_research, test_analysis)
    print("\n--- REPORT OUTPUT ---")
    print(output)