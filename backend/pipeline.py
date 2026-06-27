from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.researcher import run_researcher
from agents.analyst import run_analyst
from agents.reporter import run_reporter

# Define the state that flows between all agents
class AgentState(TypedDict):
    company_name: str
    research: str
    analysis: str
    report: str

# Each function below is one node in the graph

def research_node(state: AgentState) -> AgentState:
    research = run_researcher(state["company_name"])
    return {**state, "research": research}

def analysis_node(state: AgentState) -> AgentState:
    analysis = run_analyst(state["company_name"], state["research"])
    return {**state, "analysis": analysis}

def report_node(state: AgentState) -> AgentState:
    report = run_reporter(
        state["company_name"],
        state["research"],
        state["analysis"]
    )
    return {**state, "report": report}

# Build the graph
def build_pipeline():
    graph = StateGraph(AgentState)

    # Add the three agent nodes
    graph.add_node("researcher", research_node)
    graph.add_node("analyst", analysis_node)
    graph.add_node("reporter", report_node)

    # Define the flow: researcher -> analyst -> reporter -> END
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "reporter")
    graph.add_edge("reporter", END)

    return graph.compile()

def run_pipeline(company_name: str) -> dict:
    print(f"\n[PIPELINE] Starting full due diligence for: {company_name}")
    pipeline = build_pipeline()
    
    initial_state = {
        "company_name": company_name,
        "research": "",
        "analysis": "",
        "report": ""
    }
    
    result = pipeline.invoke(initial_state)
    print(f"\n[PIPELINE] Complete.")
    return result

if __name__ == "__main__":
    result = run_pipeline("Microsoft")
    print("\n--- FINAL REPORT ---")
    print(result["report"])