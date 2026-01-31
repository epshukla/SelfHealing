import requests
import json
import time

def main():
    print("Fetching Agent Traces...")
    try:
        res = requests.get("http://localhost:8000/agent/state")
        data = res.json()
        
        tickets = data.get("tickets", [])
        if not tickets:
            print("No active traces found.")
            return

        for t in tickets:
            print(f"\n[Ticket #{t['id']}] Status: {t['status']}")
            print(f"Scenario: {t.get('signal', {}).get('scenario_name')}")
            print("-" * 40)
            for step in t.get("steps", []):
                print(f"{step['timestamp']} | {step['stage']:<10} | {step['message']}")
                if step.get("output"):
                    print(json.dumps(step["output"], indent=2))
            print("=" * 60)

    except Exception as e:
        print(f"Error fetching traces: {e}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
