"""
Critical for the "boundaries" part of the prompt.
"""

def validate_action(analysis: dict) -> dict:
    """
    Check if the proposed action requires approval.
    """
    action_plan = analysis.get("action_plan", {})
    risk_level = action_plan.get("risk_level", "HIGH").upper()
    
    # Define rules
    requires_approval = risk_level in ["HIGH", "MEDIUM"]
    
    decision = {
        "approved": not requires_approval,
        "reason": f"Risk level is {risk_level}",
        "risk_level": risk_level
    }
    
    return decision
