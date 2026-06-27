from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = OllamaLLM(model="llama3")

research_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="""
    You are a financial research analyst. Research the following company thoroughly.
    
    Company: {company_name}
    
    Provide the following in structured format:
    1. Company Overview (what they do, founded, headquarters)
    2. Business Model (how they make money)
    3. Key Products or Services
    4. Market Position (competitors, market share if known)
    5. Recent News or Developments (last 12 months if known)
    
    Be factual, concise, and structured. If you are uncertain, say so explicitly.
    """
)

chain = research_prompt | llm | StrOutputParser()

def run_researcher(company_name: str) -> str:
    print(f"\n[RESEARCHER AGENT] Starting research on: {company_name}")
    output = chain.invoke({"company_name": company_name})
    print(f"[RESEARCHER AGENT] Research complete.")
    return output

if __name__ == "__main__":
    test_company = "Apple Inc"
    output = run_researcher(test_company)
    print("\n--- RESEARCH OUTPUT ---")
    print(output)