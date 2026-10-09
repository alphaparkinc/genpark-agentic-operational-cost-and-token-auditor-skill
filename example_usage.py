"""Example usage for Agent Cost Token Auditor."""
from client import AgentCostTokenAuditor

if __name__ == "__main__":
    events = [
        {"prompt_tokens": 1500, "completion_tokens": 300, "tool_calls_count": 2},
        {"prompt_tokens": 2000, "completion_tokens": 500, "tool_calls_count": 1}
    ]
    report = AgentCostTokenAuditor.audit_session(events, session_budget_limit=0.05)
    print("Total Session Spend: $", report["cost_breakdown"]["total_usd"])
    print("Budget Exceeded:", report["budget_exceeded"])
