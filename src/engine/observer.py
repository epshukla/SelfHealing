from collections import deque
import json
from datetime import datetime

class Observer:
    def __init__(self):
        self.signal_queue = deque()
        self.processed_signals = []

    def ingest_scenario(self, scenario_data: dict):
        """
        Ingest a scenario from the simulation.
        """
        # Add timestamp if missing
        if "timestamp" not in scenario_data:
            scenario_data["timestamp"] = datetime.now().isoformat()
        
        self.signal_queue.append(scenario_data)
        print(f"[Observer] Ingested signal: {scenario_data.get('scenario_name', 'Unknown')}")

    def get_next_signal(self):
        """
        Pop the next signal for processing.
        """
        if not self.signal_queue:
            return None
        
        signal = self.signal_queue.popleft()
        self.processed_signals.append(signal)
        return signal
