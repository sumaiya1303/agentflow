# AgentFlow — Multi-Agent Financial Due Diligence Platform

> Local-first AI orchestration system that generates institutional-grade due diligence reports in under 60 seconds. Zero data egress — all processing runs on your machine.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)
![React](https://img.shields.io/badge/React-Vite-blue)
![Ollama](https://img.shields.io/badge/Ollama-LLaMA3-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## What It Does

AgentFlow takes a company name and autonomously runs three specialized AI agents in sequence:

```
User Input → [Researcher Agent] → [Analyst Agent] → [Reporter Agent] → Due Diligence Report
```

All three agents run locally using Ollama and LLaMA3. No API keys. No cloud calls. No data leaves your machine.

---

## Demo

| Company | Research | Risk Rating | Time |
|---|---|---|---|
| Microsoft | ✅ | MEDIUM | 42.6s |
| JPMorgan Chase | ✅ | MEDIUM | 40.1s |
| Stripe | ✅ | MEDIUM/HIGH | 35.3s |
| 999999 (junk input) | ✅ Handled gracefully | CRITICAL | 17.5s |

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   React Frontend                 │
│              (Vite + Axios + Markdown)           │
└───────────────────────┬─────────────────────────┘
                        │ HTTP POST /analyse
┌───────────────────────▼─────────────────────────┐
│                 FastAPI Backend                  │
│            Input validation + logging            │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│              LangGraph Pipeline                  │
│                                                  │
│   ┌─────────────┐   ┌─────────────┐   ┌───────┐ │
│   │  Researcher │──▶│   Analyst   │──▶│Reporter│ │
│   │    Agent    │   │    Agent    │   │ Agent  │ │
│   └─────────────┘   └─────────────┘   └───────┘ │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│              Ollama — LLaMA3 (Local)             │
│         All inference runs on your machine       │
└─────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| LLM Runtime | Ollama + LLaMA3 | Local inference, zero data egress |
| Agent Orchestration | LangGraph | State machine pipeline between agents |
| Agent Framework | LangChain | Prompt templates and chain management |
| Backend API | FastAPI | REST endpoints with validation and logging |
| Frontend | React + Vite | Company input and report display UI |
| Language | Python 3.14 | Core backend and agent logic |

---

## Project Structure

```
agentflow/
├── backend/
│   ├── agents/
│   │   ├── researcher.py     # Agent 1: Company research
│   │   ├── analyst.py        # Agent 2: Risk and financial analysis
│   │   └── reporter.py       # Agent 3: Due diligence report generation
│   ├── pipeline.py           # LangGraph orchestration
│   ├── main.py               # FastAPI app and endpoints
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   └── App.css           # Styling
│   └── package.json
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) installed and running
- LLaMA3 model pulled locally

### 1. Clone the Repository

```bash
git clone https://github.com/sumaiya1303/agentflow.git
cd agentflow
```

### 2. Pull the LLaMA3 Model

```bash
ollama pull llama3
```

### 3. Start the Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000`

### 4. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### 5. Run a Due Diligence Report

- Open `http://localhost:5173`
- Type any company name
- Click **Run Analysis**
- Three agents fire automatically
- Full report renders in 30-60 seconds

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/research` | Run researcher agent only |
| POST | `/analyse` | Run full three-agent pipeline |

### Example Request

```bash
curl -X POST http://127.0.0.1:8000/analyse \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Tesla"}'
```

### Example Response

```json
{
  "company": "Tesla",
  "research": "...",
  "analysis": "...",
  "report": "...",
  "duration_seconds": 38.4
}
```

---

## Key Design Decisions

**Why local LLMs?**
Financial due diligence involves sensitive company data. Sending that data to external APIs creates compliance, confidentiality, and data sovereignty risks. Running LLaMA3 locally via Ollama eliminates all of these concerns.

**Why LangGraph over a simple chain?**
LangGraph provides explicit state management between agents. Each agent receives the full accumulated state — the analyst gets the researcher's output, the reporter gets both. This structured handoff produces higher quality outputs than a linear prompt chain.

**Why three separate agents instead of one prompt?**
Specialization. Each agent has a focused system prompt optimized for its task. A single monolithic prompt produces lower quality output across all three tasks simultaneously.

---

## Roadmap

- [ ] Add PDF export of due diligence reports
- [ ] Support multiple LLM models (Mistral, Gemma)
- [ ] Add company comparison mode (side by side)
- [ ] Implement report history and local storage
- [ ] Add Docker containerization for one-command setup
- [ ] Build financial data retrieval via SEC EDGAR API

---

## Interview Talking Points

**What problem does this solve?**
Financial due diligence is time-intensive and expensive. This tool automates the initial research and risk assessment phase for finance professionals who need fast, private analysis.

**What was the hardest technical challenge?**
Orchestrating state between three agents using LangGraph so each agent receives and builds on the previous agent's output without losing context.

**Why is zero data egress important?**
Finance professionals cannot send client or deal data to external APIs due to confidentiality obligations. Local inference removes that barrier entirely.

**What would you add next?**
SEC EDGAR API integration for real financial data, PDF export, and a company comparison mode for side-by-side due diligence.

---

## License

MIT

---

*Built with Python, LangChain, LangGraph, Ollama, FastAPI, and React.*