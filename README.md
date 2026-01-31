# Agentic AI for Self-Healing Support (Headless E-commerce Migration)

## Override Context
**Hackathon Demo**: Optimized for explainability, controlled autonomy, and a clear agent loop.
**Scenario**: Self-healing support for a SaaS platform migrating merchants to headless architecture.

## Problem Statement
A migration to headless architecture has caused:
- Broken checkouts
- Webhook failures
- Deprecated API usage
- Frontend-backend mismatches

Support teams are overwhelmed. This Agent steps in to Observe, Reason, Decide, and Act.

## Architecture & Tech Stack
- **Backend**: Python (FastAPI)
- **Frontend**: React + Vite (Dynamic Dashboard)
- **Agent components**:
    - **Orchestrator**: State machine managing the `Observe -> Reason -> Decide -> Act -> Feedback` loop.
    - **Observer**: Ingests simulated signals (logs, webhooks).
    - **Reasoner**: OpenAI-powered analysis (Chain of Thought).
    - **Guardrails**: Risk-based permission system (High risk = Human-in-the-loop).
- **Data**: In-memory vector store & state for demo speed.
- **Simulation**: JSON-based scenarios driving the agent.

## Folder Structure
```
self_healing/
├── src/
│   ├── agents/          # Orchestrator & Tool definitions
│   ├── engine/          # Observer, Reasoning (LLM), Guardrails
│   ├── data/            # Knowledge base & Vector store
│   └── state/           # In-memory persistence
├── simulations/         # JSON scenarios (e.g. Broken Checkout)
├── ui/                  # React Dashboard & Trace Viewer
├── main.py              # FastAPI Entry Point
└── README.md
```

## Setup
1. **Install Dependencies**: `pip install fastapi uvicorn openai` (plus frontend deps)
2. **Environment**: Set `OPENAI_API_KEY`.
3. **Run**: `python main.py` (Starts Backend) & `npm run dev` (Starts Frontend).
