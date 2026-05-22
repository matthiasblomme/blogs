# Submission 2 — Journey to containers (retrospective)

Fields below match the TechXchange 2026 Call for Sessions form. Status: **dialog in progress.**

## Locked anchors

- **Takeaway sentence** (what an attendee says to a colleague the next day): *"Lift and shift won't cut it. I see what I need to prepare for now."*
- **Story shape**: a real ACE deployment moving from node-managed to operator-based containerized, plus everything in between. Story-led, not decision-log. Past tense, plain voice, no "actually mattered" hype.
- **Possible reshuffle on the table**: collapse #3 into a 20-minute Tech Talk version of this same body of knowledge (checklist format). Hold until #2's abstract is shaped.
- **Closing quote for the talk itself (not the abstract)**: *"Ask the questions early. It is cheaper than fixing surprises later."* (from blog 03)

---

## Session Type

Technology Breakout (45 minutes)

## Software/infrastructure products

- IBM App Connect Enterprise (primary)
- Red Hat OpenShift / Kubernetes (secondary, if available in the dropdown)
- Fall back to the Champions "Not on the list" option if ACE isn't listed.

## Technical Level

200 or 300 (intermediate). Same as #1.

## Industry

Cross-industry.

## Session Title 

PIVOT! ACE from classical on-premise to operator-based

## Session Abstract

Moving ACE to containers can look like a lift and shift. Going from classical on-premise to operator-based is a series of decisions, not a single move. We had multiple integration servers under a single integration node. The build phase came first: one image for build and test. Then a single artifact, built once, promoted across environments. Building the same code per environment is a habit worth dropping. Runtime moved to the IntegrationRuntime operator. The dashboard stayed in scope, but not for single artifact storage. More small decisions sit between them. Lift and shift won't cut it.

Three takeaways: containerizing ACE is many small decisions, not a single move. Build once and promote across environments. Some on-premise habits move with you, others belong in the past.

## Why should this idea be considered for IBM TechXchange 2026?

The IBM Champions program and the ACE team both mentioned the same gap when asked: field stories about real ACE deployments, told by the people who shipped them. IBM development covers the product side with examples and demos. Useful, but academic. Not tailored to the choices a customer ended up making day-to-day. The 45-minute format gives room for the counterarguments and what we'd do differently, not just the choices that worked. Drawn from a real customer engagement. The audience walks out knowing what they need to prepare for before their own move begins.

---

## Notes & parked items

**v0 reference text** (from `abstract_drafts.md`, pre-dialog, treat as scratch):

> A real ACE migration, told as a decision log. One ubi-minimal image for build, test and runtime, not a runner you have to feed. Native IntegrationRuntime operator. Vault as ConfigMap, credentials injected at startup.
>
> No ACE dashboard for bar files. No versioning, no rollback, and it updates whether you want it to. GitLab artifact storage works because the operator wants basic auth, and GitLab dresses a token up as exactly that.
>
> The pipeline auto-resolves transitive dependencies so developers never touch operator config. Every choice has a counterargument. You will hear those.
>
> Three takeaways: the decisions that matter have two defensible answers, developer experience survives only when the pipeline absorbs the complexity, and the boring choices made for boring reasons hold up longest.

**Source material:**
- Customer 1 from [customer_experience.md](customer_experience.md): build/runtime/credentials/bar storage/config/pipeline decisions. Rich decision log.
- Published blog series: 01.the-basics, 02.images-vs-artefacts, 04.scoping-your-runtime, 05.ace-startup-optimization, 06.upgrading-in-containers — most of the mechanical content has a blog parallel.
