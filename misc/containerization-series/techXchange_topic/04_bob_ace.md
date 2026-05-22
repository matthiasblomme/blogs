# Submission 4: Developing ACE integrations with Bob

Fields below match the TechXchange 2026 Call for Sessions form. Status: **skeleton, dialog not started.**

---

## Session Type

Tech Talk (20 minutes)

## Software/infrastructure products

- IBM App Connect Enterprise (primary)
- Probably worth listing the AI-side tooling Bob wraps, depending on what the dropdown offers.
- Fall back to the Champions "Not on the list" option if needed.

## Technical Level

200 or 300 (intermediate). Assumes familiarity with ACE development. Doesn't require familiarity with the specific AI tooling.

## Industry

Cross-industry.

## Session Title

Hey Bob, let's build an ACE Application

## Session Abstract 

Bob handles the basics of an ACE application well. The harder part is the team-specific patterns: which nodes to use, what conventions to follow, where the subflows go. ESQL is getting better, but flow architecture is the real bottleneck. A custom skill closes that gap. It walks Bob through your predefined guidelines as the flow takes shape, so the patterns stick and node selection follows the rules your team already lives by. Live demo included, in whatever time the 20 minutes leaves us.

Three takeaways: Bob handles basics well, but ACE patterns and node selection are the real bottleneck. A custom skill encodes your team's guidelines into the workflow. The result is AI that builds flows the way your team does.

## Why should this idea be considered for IBM TechXchange 2026?

Most AI productivity sessions show what generic AI can do. Fewer show what to do when generic isn't enough for your specific work. Using Bob to build ACE flows is fine for the basics. Generating ESQL has caught up. The harder gap is ACE-specific patterns and node selection. A custom skill that encodes your team's guidelines is what makes Bob useful for the actual flow work, not just the basics. The 20-minute Tech Talk includes a live demo of the skill building a flow against predefined guidelines. The audience walks out with a pattern they can adapt to their own setup, not an idea to file away for later.

---

## Notes & parked items

**Track fit**: most likely AI productivity (one of the five 2026 tracks). Hybrid cloud management is a fallback if the AI angle doesn't carry the abstract.

**Source material:**
- The Bob skill itself: `D:\GIT\bob_modes\` (the directory of skills, including the blog_buddy skill referenced in memory).
- Lived experience of using Bob for ACE integration development: the specific issues encountered, what was useful, what fell short.
- Possibly comparable to how the container blog series works: practical, opinionated, plain.

**Open questions for the dialog when we start:**
- Is this a "how I use Bob" talk, a "what Bob can and can't do" talk, or a "lessons learned applying AI to integration work" talk? Different angles.
- Single sharp angle for the 20-min format vs. broader survey.
- How much to name the underlying AI tooling (Claude, etc.) vs. keep it as "Bob" / generic.
