import os
import json
from openai import OpenAI

class Reasoner:
    def __init__(self):
        # API Key is loaded from env by dotenv in main.py, but we ensure it here
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not found. LLM reasoning will fail.")
        self.client = OpenAI(api_key=api_key)

    def reason(self, observation: dict) -> dict:
        """
        Analyze the observation using LLM Chain of Thought.
        Returns detailed analysis.
        """
        print(f"[Reasoner] Analyzing: {observation.get('scenario_name')}")
        
        system_prompt = """
        You are an expert Site Reliability Engineer (SRE).
        Analyze the provided system signals (logs, errors, metrics).
        
        You MUST respond in strict JSON format with the following st ructure:
        {
            "root_cause": "Detailed explanation of what went wrong",
            "confidence": 0.0 to 1.0,
            "evidence": ["List of log lines or metrics used for conclusion"],
            "alternatives": ["List of other possible causes considered but rejected"],
            "action_plan": {
                "title": "Short title of action",
                "description": "Step by step execution plan",
                "risk_level": "LOW|MEDIUM|HIGH",
                "risk_reason": "Why is it this risk level?"
            }
        }
        
        Risk assessment rules:
        - LOW: Read-only operations, safe restarts of stateless services.
        - MEDIUM: Configuration changes, scaling.
        - HIGH: Database writes, deleting data, public-facing API changes, cost-impacting actions.
        """

        user_content = f"""
        Scenario: {observation.get("scenario_name", "Unknown")}
        Description: {observation.get("description", "")}
        Logs/Signals:
        {json.dumps(observation.get("logs", []), indent=2)}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", # Use a capable model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            analysis = json.loads(content)
            return analysis
            
        except Exception as e:
            print(f"[Reasoner] Error: {e}")
            # Fallback for demo stability
            return {
                "root_cause": "LLM Analysis Failed",
                "confidence": 0.0,
                "evidence": [str(e)],
                "alternatives": [],
                "action_plan": {
                    "title": "Manual Investigation Required",
                    "description": "The reasoning engine encountered an error.",
                    "risk_level": "HIGH",
                    "risk_reason": "System failure"
                }
            }
