# TechXchange 2026 abstract drafts — v1

Three submissions, all in the Hybrid cloud management track. Customer names never appear. Voice per Blog Buddy guide: plain, dry, direct, no em dashes, straight quotes, no marketing fluff, takeaways stated as outcomes not features.

Character budgets:
- Title: 100 chars max
- Abstract: 800 chars max (form said "characters" in the call — verify on the actual form)
- Justification: free text

Counts below are body-only, no labels.

---

## Submission 1 — Licensing shapes your cluster topology

**Format:** 20-min Tech Talk
**Track:** Hybrid cloud management

### Title (60 chars)
How ACE licensing rewrote our cluster topology

### Abstract (v2, post-dialog)
Running ACE in containers looks different through the lens of licensing. Containers scale on demand. Per-container licensing makes every spinup a license check. Either you over-provision or auto-scaling stops being elastic. Same with resource sizing: per-container, every CPU bump is a license bump; pinned to a worker node, you have room to tune. Runtime scoping follows suit: bundle tight and one spike raises the whole container's license usage; split wide and each flow becomes its own license event. This conversation belongs in the right rooms, with engineering at the table.

Three takeaways: scaling, sizing, and scoping each shift under the licensing model; per-container and pinned-node paths split engineering work differently; the decision belongs to engineering alongside procurement.

### Parked openers (we'll circle back)
1. *"Running ACE in containers looks different through the lens of licensing."* — shortest, currently used above
2. *"Running ACE in containers brings the usual technical conversations. Through the lens of licensing, those conversations all change shape."* — two-sentence variant
3. *"Setting up, deploying, and updating ACE in containers all look different through the lens of licensing."* — names operational areas

### Justification
Licensing constraints rarely make it onto a slide. They shape every production deployment anyway. This is the kind of session IBM development cannot easily publish, because critiquing the licensing model is not their job. It is mine, as a Champion who has watched it bend real cluster designs more than once. The two customer stories are short, concrete and ready to tell. The murmering about dynamic startup scaling closes the loop: yes, the runtime got smarter, but the bill did not.

---

## Submission 2 — Journey to containers (retrospective)

**Format:** 45-min Technology breakout
**Track:** Hybrid cloud management

### Title (60 chars)
Journey to containers: the decisions that actually mattered

### Abstract
A real ACE migration, told as a decision log. One ubi-minimal image for build, test and runtime, not a runner you have to feed. Native IntegrationRuntime operator. Vault as ConfigMap, credentials injected at startup.

No ACE dashboard for bar files. No versioning, no rollback, and it updates whether you want it to. GitLab artifact storage works because the operator wants basic auth, and GitLab dresses a token up as exactly that.

The pipeline auto-resolves transitive dependencies so developers never touch operator config. Every choice has a counterargument. You will hear those.

Three takeaways: the decisions that matter have two defensible answers, developer experience survives only when the pipeline absorbs the complexity, and the boring choices made for boring reasons hold up longest.

### Justification
This is the field talk Karen at IBM asked Champions to give: real deployment, real decisions, told by the person who shipped it instead of the person who built the product. The decision log includes choices IBM development cannot publish in the same tone, especially around the ACE dashboard and which artifact stores actually work with the operator's auth model. The 45-minute format gives space for the counterarguments, not just the choices. This sits squarely in the Hybrid cloud management track and complements, rather than overlaps with, my two other submissions.

---

## Submission 3 — Moving to containers, what happens before

**Format:** 45-min Technology breakout
**Track:** Hybrid cloud management

### Title (62 chars)
Moving to containers: what happens before you build image one

### Abstract
Most container migration talks start at the first Dockerfile. This one starts a week earlier.

Before you build image one, a few choices set everything that follows. Image strategy: baked custom image or dedicated runner, and which one are you ready to maintain in two years. Operator or dashboard, knowing the dashboard auto-updates and cannot version. Bar file storage: the operator wants basic auth, which rules out half the candidates. Credentials. Config layering. Pipeline scope.

Each of these is a trade-off, not a feature. Get them wrong and you find out on a Friday.

Three takeaways: the decisions you defer become the bugs you ship, the operator and the dashboard are not interchangeable, and the artifact repository question kills more migrations than anyone expects.

### Justification
There is plenty of content on Dockerfiles, Helm charts and operators. There is almost nothing on the choices you have to settle before any of that. This is a prescriptive companion to my retrospective "Journey to containers" submission. Where the journey talk says "this is what we did", this talk says "here is the decision tree you cannot skip". Different audience: people who are about to start, not people who are in the middle. Drawn from three real customer engagements, fully anonymised. Champion perspective, not product pitch.

---

## Differentiation check — #2 vs #3

Opening sentences read side by side:

- #2: "A real ACE migration, told as a decision log."
- #3: "Most container migration talks start at the first Dockerfile. This one starts a week earlier."

Different posture, different audience, different tense. #2 is past tense, "we chose". #3 is forward-looking, "you have to settle". A reviewer who reads both should see two clearly different talks, not the same talk in two coats of paint.

---

## Open follow-ups before submission
- Verify the abstract field limit on the actual form (call said characters, confirm).
- If the product dropdown does not include ACE, use the Champions "Not on the list" option and reference ACE in the abstract.
- Read each abstract aloud once. If a sentence sounds written rather than said, rewrite it.
- Pull a hard number from any of the customer engagements (image size, bar file count auto-resolved, integration servers per worker node, time-to-rollback, restart latency on the pinned node) and drop the strongest one into whichever abstract benefits most. Reviewers want "from / to" specificity.
