"""MCP server for Agent Cost Token Auditor."""
import sys
import json
from client import AgentCostTokenAuditor

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "audit_agent_session_cost",
                "description": "Calculates detailed cost and token analytics across agent execution steps",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_events": {"type": "array"},
                        "session_budget_limit": {"type": "number"}
                    },
                    "required": ["session_events"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "audit_agent_session_cost":
            args = params.get("arguments", {})
            res = AgentCostTokenAuditor.audit_session(
                args.get("session_events", []),
                args.get("session_budget_limit", 0.50)
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
