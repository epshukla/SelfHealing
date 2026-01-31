import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build the app
app = FastAPI(title="Self-Healing Agent API", version="1.0.0")

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... imports ...
import json
from src.agents.orchestrator import Orchestrator

# ... app setup ...

# Initialize Orchestrator
orchestrator = Orchestrator()

@app.get("/")
def health_check():
    return {"status": "running", "service": "Self-Healing Agent"}

@app.post("/simulation/start")
def start_simulation(scenario_id: str):
    """
    Trigger a specific simulation scenario.
    """
    try:
        # Load the scenario file
        path = f"simulations/scenarios/{scenario_id}.json"
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        with open(path, "r") as f:
            data = json.load(f)
            
        orchestrator.ingest_simulation(data)
        return {"message": f"Simulation {scenario_id} started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent/state")
def get_agent_state():
    """
    Get current state of the agent loop for the UI.
    """
    return orchestrator.get_state()

@app.post("/agent/approve")
def approve_action(ticket_id: str):
    """
    Human approval for high-risk actions.
    """
    result = orchestrator.approve_ticket(ticket_id)
    if result:
        return {"status": "approved", "ticket_id": ticket_id}
    else:
        raise HTTPException(status_code=400, detail="Ticket not found or not pending approval")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
