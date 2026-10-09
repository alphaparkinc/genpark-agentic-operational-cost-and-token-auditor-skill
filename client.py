"""Agentic Operational Cost & Token Auditor.
100% Python Standard Library.
"""

class AgentCostTokenAuditor:
    """Tracks token consumption, calculates exact cloud costs, and identifies budget anomalies."""
    
    RATES = {
        "input_tokens_per_million": 0.50,
        "output_tokens_per_million": 2.00,
        "tool_call_fixed_charge": 0.0005
    }
    
    @classmethod
    def audit_session(cls, session_events: list, session_budget_limit: float = 0.50) -> dict:
        total_input_tokens = 0
        total_output_tokens = 0
        total_tool_calls = 0
        
        for evt in session_events:
            total_input_tokens += evt.get("prompt_tokens", 0)
            total_output_tokens += evt.get("completion_tokens", 0)
            total_tool_calls += evt.get("tool_calls_count", 0)
            
        input_cost = (total_input_tokens / 1_000_000) * cls.RATES["input_tokens_per_million"]
        output_cost = (total_output_tokens / 1_000_000) * cls.RATES["output_tokens_per_million"]
        tool_cost = total_tool_calls * cls.RATES["tool_call_fixed_charge"]
        total_cost = round(input_cost + output_cost + tool_cost, 5)
        
        exceeded = total_cost > session_budget_limit
        burn_rate = round(total_cost / max(1, len(session_events)), 5)
        
        return {
            "total_tokens": total_input_tokens + total_output_tokens,
            "total_tool_calls": total_tool_calls,
            "cost_breakdown": {
                "input_usd": round(input_cost, 5),
                "output_usd": round(output_cost, 5),
                "tools_usd": round(tool_cost, 5),
                "total_usd": total_cost
            },
            "budget_limit_usd": session_budget_limit,
            "budget_exceeded": exceeded,
            "burn_rate_per_step": burn_rate
        }
