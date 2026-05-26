# TechXchange speaker topics

## 01.Licensing

### Session Type

Tech Talk (20 minutes)

### Software/infrastructure products

- IBM App Connect Enterprise (primary)
- Red Hat OpenShift / Kubernetes (secondary, if available in the dropdown)
- Fall back to the Champions "Not on the list" option if ACE isn't listed.

### Technical Level

200 or 300 (intermediate). Built on assumed familiarity with ACE and containers, but does not require deep K8s internals.

### Industry

Cross-industry.

### Session Title

License to scale: ACE in containers


### Session Abstract


Running ACE in containers looks different through the lens of licensing. Containers scale on demand, ideally. Per-container licensing makes every spinup a license check. You over-provision or auto-scaling stops being elastic. Same with resource sizing: per-container, every CPU bump is a license bump; pinned to a worker node, you have room to tune. Runtime scoping follows suit: bundle tight and one spike raises the whole container's license usage; split wide and each flow becomes its own license event. This conversation belongs in the right rooms, with engineering at the table.

Three takeaways: scaling, sizing, and scoping all look different under the licensing model. Per-container and pinned-node split engineering work differently. Engineering belongs at the table, not just procurement.

### Why should this idea be considered for IBM TechXchange 2026?

The IBM Champions program and the ACE team both mentioned field stories as the gap worth filling. Licensing rarely gets its own session, even though it shapes how containers actually scale, get sized, and get scoped. This Tech Talk walks through real customer engagements: PVU not available, adapter patterns multiplying integration servers on cloud, dynamic startup resources changing the comparison. The 20-minute format means one sharp angle, not a survey. The audience walks out knowing why licensing belongs in the conversation when engineering picks a container topology, and what it costs not to have it there.

## 02.Journey

### Session Type

Technology Breakout (45 minutes)

### Software/infrastructure products

- IBM App Connect Enterprise (primary)
- Red Hat OpenShift / Kubernetes (secondary, if available in the dropdown)
- Fall back to the Champions "Not on the list" option if ACE isn't listed.

### Technical Level

200 or 300 (intermediate). Same as #1.

### Industry

Cross-industry.

### Session Title

PIVOT! ACE from classical on-premise to operator-based

### Session Abstract

Moving ACE to containers can look like a lift and shift. Going from classical on-premise to operator-based is a series of decisions, not a single move. We had multiple integration servers under a single integration node. The build phase came first: one image for build and test. Then a single artifact, built once, promoted across environments. Building the same code per environment is a habit worth dropping. Runtime moved to the IntegrationRuntime operator. The dashboard stayed in scope, but not for single artifact storage. More small decisions sit between them. Lift and shift won't cut it.

Three takeaways: containerizing ACE is many small decisions, not a single move. Build once and promote across environments. Some on-premise habits move with you, others belong in the past.

### Why should this idea be considered for IBM TechXchange 2026?

The IBM Champions program and the ACE team both mentioned the same gap when asked: field stories about real ACE deployments, told by the people who shipped them. IBM development covers the product side with examples and demos. Useful, but academic. Not tailored to the choices a customer ended up making day-to-day. The 45-minute format gives room for the counterarguments and what we'd do differently, not just the choices that worked. Drawn from a real customer engagement. The audience walks out knowing what they need to prepare for before their own move begins.


## 03.Bob and ACE

### Session Type

Tech Talk (20 minutes)

### Software/infrastructure products

- IBM App Connect Enterprise (primary)
- Probably worth listing the AI-side tooling Bob wraps, depending on what the dropdown offers.
- Fall back to the Champions "Not on the list" option if needed.

### Technical Level

200 or 300 (intermediate). Assumes familiarity with ACE development. Doesn't require familiarity with the specific AI tooling.

### Industry

Cross-industry.

### Session Title

Hey Bob, let's build an ACE Application

### Session Abstract

Bob handles the basics of an ACE application well. The harder part is the team-specific patterns: which nodes to use, what conventions to follow, where the subflows go. ESQL is getting better, but flow architecture is the real bottleneck. A custom skill closes that gap. It walks Bob through your predefined guidelines as the flow takes shape, so the patterns stick and node selection follows the rules your team already lives by. Live demo included, in whatever time the 20 minutes leaves us.

Three takeaways: Bob handles basics well, but ACE patterns and node selection are the real bottleneck. A custom skill encodes your team's guidelines into the workflow. The result is AI that builds flows the way your team does.

### Why should this idea be considered for IBM TechXchange 2026?

Most AI productivity sessions show what generic AI can do. Fewer show what to do when generic isn't enough for your specific work. Using Bob to build ACE flows is fine for the basics. Generating ESQL has caught up. The harder gap is ACE-specific patterns and node selection. A custom skill that encodes your team's guidelines is what makes Bob useful for the actual flow work, not just the basics. The 20-minute Tech Talk includes a live demo of the skill building a flow against predefined guidelines. The audience walks out with a pattern they can adapt to their own setup, not an idea to file away for later.

## Submission 5: Handling ACE secrets across the move to containers

Fields below match the TechXchange 2026 Call for Sessions form.

### Session Type

Tech Talk (20 minutes)

### Software/infrastructure products

- IBM App Connect Enterprise (primary)
- HashiCorp Vault (or other external secret store, if listed)
- Red Hat OpenShift / Kubernetes (if available)
- Fall back to the Champions "Not on the list" option if ACE isn't listed.

### Technical Level

200 or 300 (intermediate). Assumes familiarity with ACE secrets handling on a traditional node. Doesn't require Kubernetes operator internals.

### Industry

Cross-industry.

### Session Title (55 chars)

Keep it secret, keep it safe: ACE secrets in containers

### Session Abstract (711 chars, 89 of buffer to 800)

Don't put passwords in your flow. Or in your code. Or in base64-encoded files committed to git. Trust me, I've seen the lot, and plenty of ACE projects still ship them this way. Containers give you other options. The combination that works: ACE vaults for application secrets, Kubernetes secrets mounted, and container env vars for runtime secrets. ESQL reads from env vars at startup. Java compute fetches via the vault interface. Either way, the credential never sits in the image or the repo.

Three takeaways: passwords don't belong in flow, code, or base64 files. ACE vault, k8s secrets, and container env vars are the working combination. ESQL via env vars or Java compute via vault interface, pick by flow.

### Why should this idea be considered for IBM TechXchange 2026? (491 chars)

Passwords in flow logic, in code, in base64-encoded files committed to git. Plenty of ACE projects still ship secrets this way. Most secrets-in-containers content stops at "mount a config map" or "use an external vault". This 20-minute Tech Talk names the bad habit head-on and walks through what replaces it: ACE vault for application secrets, Kubernetes secrets for the keys that unlock them, container env vars for runtime. The audience walks out with a clear pattern that survives audit.
