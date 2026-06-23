# ACE MCP, open questions (personal notes)

Not for the blog. Things still worth chasing across the ACE MCP write-ups.

- Why MCP.Runtime tool calls stall on 13.0.7.2: most return in milliseconds, the odd one hangs, and it gets worse with a second client connected. Fits the one-client-per-lifetime pattern but looser.
- The `mcp::basicAuthOverride username password` secret payload: decode an auto-generated Dashboard MCP secret to confirm.
- `spec.pod.containers.acemcp.*` and `spec.pod.containers.langgraph.*`: run `oc explain` against the live CRD to confirm the customisation paths.
- Operator and Dashboard versions where the Enterprise Agent first shipped GA: working answer is operator 13.0.0 / Dashboard 13.0.7.0-r1 or later, not yet confirmed.
- Whether MCP.Admin is preview or production: ask IBM rep.
