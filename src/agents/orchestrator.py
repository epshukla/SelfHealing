import uuid
from datetime import datetime
from src.engine.observer import Observer
from src.engine.reasoning import Reasoner
from src.engine.guardrails import validate_action

class Orchestrator:
    def __init__(self):
        self.observer = Observer()
        self.reasoner = Reasoner()
        self.state = {
            "active_tickets": {},  # ticket_id -> data
            "history": []
        }

    def ingest_simulation(self, scenario_data):
        self.observer.ingest_scenario(scenario_data)
        # Auto-process for the demo loop
        self.process_next()

    def process_next(self):
        """
        Run one iteration of the Observe -> Reason -> Decide -> Act loop.
        """
        signal = self.observer.get_next_signal()
        if not signal:
            return None

        ticket_id = str(uuid.uuid4())[:8]
        print(f"[Orchestrator] Processing ticket {ticket_id} for {signal.get('scenario_name')}")

        # 1. Observe
        ticket = {
            "id": ticket_id,
            "timestamp": datetime.now().isoformat(),
            "status": "observing",
            "signal": signal,
            "steps": []
        }
        self._log_step(ticket, "Observe", "Signal detected")

        # 2. Reason
        ticket["status"] = "reasoning"
        self._log_step(ticket, "Reason", "Analyzing root cause...")
        analysis = self.reasoner.reason(signal)
        ticket["analysis"] = analysis
        self._log_step(ticket, "Reason", "Analysis complete", output=analysis)

        # 3. Decide (Guardrails)
        ticket["status"] = "deciding"
        decision = validate_action(analysis)
        ticket["decision"] = decision
        
        if decision["approved"]:
            self._log_step(ticket, "Decide", "Auto-approval granted", output=decision)
            self.execute_action(ticket)
        else:
            self._log_step(ticket, "Decide", "Requires human approval", output=decision)
            ticket["status"] = "pending_approval"
        
        # Save state
        self.state["active_tickets"][ticket_id] = ticket
        return ticket

    def approve_ticket(self, ticket_id):
        if ticket_id in self.state["active_tickets"]:
            ticket = self.state["active_tickets"][ticket_id]
            if ticket["status"] == "pending_approval":
                self._log_step(ticket, "Approval", "User approved action")
                self.execute_action(ticket)
                return True
        return False

    def execute_action(self, ticket):
        ticket["status"] = "acting"
        action = ticket["analysis"]["action_plan"]
        self._log_step(ticket, "Act", f"Executing: {action['title']}")
        
        # Simulate execution
        ticket["status"] = "resolved"
        self._log_step(ticket, "Feedback", "Action completed successfully")

    def _log_step(self, ticket, stage, message, output=None):
        step = {
            "stage": stage,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "output": output
        }
        ticket["steps"].append(step)

    def get_state(self):
        return {
            "tickets": [v for k,v in self.state["active_tickets"].items()]
        }
