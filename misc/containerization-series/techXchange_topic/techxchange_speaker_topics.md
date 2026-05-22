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

PIVOT! ACE from node-managed to operator-based

### Session Abstract

Moving ACE to containers can look like a lift and shift. Going from node-managed to operator-based is a series of decisions, not a single move. We came from a node-managed setup: multiple integration servers under a single node. The build phase came first: one image for build and test. Then a single artifact, built once, promoted across environments. Building the same code per environment is a habit worth dropping. Runtime moved to the IntegrationRuntime operator. The dashboard stayed in scope, but not for single artifact storage. More small decisions sit between them. Lift and shift won't cut it.

Three takeaways: containerizing ACE is many small decisions, not a single move. Build once and promote across environments. Some node-managed habits move with you, others belong in the past.

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

