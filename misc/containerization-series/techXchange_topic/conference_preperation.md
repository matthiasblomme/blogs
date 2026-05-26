# Digest — TechXchange 2026 abstract prep (for the ACE-on-containers talk)

## Context

Karen at IBM (Champions program) suggested Matthias submit a TechXchange 2026 abstract on something "ACE field-related" — a real-world story IBM dev teams cannot easily tell themselves: how ACE is *actually* deployed, tuning/deployment best practices, modernization-to-containers success stories. Matthias has a 6-part (soon 7-part) container blog series and is well-placed to do exactly this.

Karen also shared a 1h04 IBM Champions Enablement session (April 8, 2026) — "How to prepare your conference abstract and what reviewers look for" — as raw material. The big .mp4 and the .docx are the same content: the .docx is the meeting transcript with embedded slide screenshots, so the digest below covers both. (Confirmed: extracted 63 876 characters of dialogue from the .docx; the .mp4 adds visual chrome but no new substance.)

This file digests both sources into the keypoints, guidelines and pitfalls Matthias needs *before* drafting the abstract. The drafting itself is the **next step**, not this file.

---

## 1. The IBM topic suggestion in one paragraph

> "How about something very much ACE *field-related* — how ACE is actually deployed for real (deployment best practices, tuning best practices) or examples of successful modernization projects moving to containers? This is harder for IBM development to blog about or present. It would be great to have real-life success stories to point people at in the community, and could become a series."

Matthias' follow-up to Karen confirmed: containers-with-all-dependencies is the angle he can "go on and on about", and he's already submitting.

---

## 2. Hard facts about the 2026 conference (use these to frame the abstract)

| Item | Value |
|---|---|
| Submission deadline | **22 May 2026** |
| Acceptance notifications | **30 June 2026** |
| Conference location | Atlanta |
| Co-located | HashiConf 2026, i-Doug NA, COMMON Navigate (separate submission paths for HashiConf and COMMON) |
| Tracks (down from 12 to 5) | AI productivity • Data management • Security & governance • **Hybrid cloud management** • Hybrid cloud infrastructure |
| Most likely track for this talk | **Hybrid cloud management** (Red Hat, Terraform, IBM Cloud, automation portfolio) — ACE-on-containers sits squarely here |
| Session types | (a) **Technology breakout** — 45 min (down from 60), traditional breakout room, deeper teaching/demos. (b) **Tech talk** — 20 min, small sandbox stage, drop-in audience |
| Title field | 100 **characters** |
| Abstract field | 800 **characters** (not words — verify this on the form, but the speaker said characters) |
| "Why should this idea be considered?" justification | Required, free text |
| Speaker count | **One speaker preferred**. Co-presenter only with written justification. (Important change vs. prior years.) |
| Champions form perk | "Not on the list" product option — pick this if the product dropdown doesn't fit and explain in the abstract |

---

## 3. What reviewers actively look for (positive signals)

Direct quotes / paraphrases from the three reviewers on the call (Melissa Gurney Greene, Angie Borman, Graeme Noseworthy):

- **"How exciting is it as a technical person to attend it?"** — gut-check from Melissa
- **Use cases that help the most people** — production experience, lessons learned, specific keywords
- **Education, not entertainment, not sharing** — does it move an attendee from 101 → 102, or 102 → beyond? Sharing what you know ≠ teaching how to do it.
- **The "so what"** — does it make someone in the audience better at their job?
- **The "now what"** — what's the concrete takeaway they walk out with?
- **The conference promise to attendees**: "You will leave a better, more qualified professional than the day you show up." Frame your abstract through that lens.
- **Originality and personal voice** — passion has to come through. "You be you."

---

## 4. What gets you declined (negative signals — avoid these)

- **Buzzword bingo** — Melissa's instant-no list:
    - "transformational synergy"
    - "digital transformation"
    - any high-level marketing word without specifics
- **Sales / marketing pitch** — this is a *learning* conference; IBM applies the same rule to its own staff in the sandbox
- **Vague verbs** — "we transformed our deployment" tells a reviewer nothing
    - Instead: *"We took our production deployment cycle from 9 months to 9 minutes by..."* — concrete, quantifiable, real
- **Too-much-too-soon** — trying to dump everything you know into 45 minutes; pick the key points and trust people to come ask you for the rest
- **Middle-of-the-road talks** — not clearly aimed at any specific persona / track; falls between two stools
- **AI-generated verbatim** — they will run analysis to flag likely-AI submissions. Not an auto-reject, but a negative indicator. Using AI as a brainstorming partner is fine; copy-pasting its output is not.
- **Listing features instead of explaining why they matter**

---

## 5. Logistics & misc rules worth remembering

- **Bring your own laptop** for either session type. Adapters provided on site. Template offered but not required (company branding OK).
- **Multi-part talks**: submit each part as a separate abstract; tag them "Part 1 of 2" / "Part 2 of 2" in the abstract and explain in the justification. Email `speaker help` to keep them connected.
- **Coaching**: pre-conference coaching sessions are planned across July–September; on-site speaker coaches available for last-minute prep (Matthias used Gary/Paul in 2025).
- **If declined**: ask for feedback; content is not wasted — recycle to user groups, online community, blog, video. Competition is high in some areas (Terraform was named as the most-competitive category historically).
- **Once accepted**: "tell the world early and often" — promotion before the conference shapes attendance and surfaces questions you can fold back into the talk. Practice standing up in an empty room; video record yourself.

---

## 6. Synthesised guidance for *this specific* abstract

Translating the reviewer signals into rules-for-Matthias for the ACE-on-containers talk:

1. **Lead with the field, not the product.** The pitch is "here is what real teams hit when they containerise ACE", not "ACE features in containers". Karen and Ben already said the *field* angle is exactly what's missing.
2. **Anchor in one concrete project or pattern.** Pick one of the 6+ blog topics as the spine (e.g. handling K8s secrets for ACE, or the dependencies story). Generic best-practices decks blur together; one real engagement with messy edges stands out.
3. **State the "from / to" in numbers, not adjectives.** Pull a measurable before/after from a real deployment — startup time, image size, deploy cadence, number of integration servers reduced, secret-rotation toil eliminated. Anything quantifiable.
4. **Promise three specific takeaways in the abstract body** — the "now what" the reviewers explicitly want. Reviewers should be able to recite to themselves what an attendee walks out with.
5. **Pick the right track up front.** Default: *Hybrid cloud management*. The Red Hat / OpenShift / automation context is the natural home for ACE-on-containers. Don't try to be track-agnostic — Melissa called that "falls between two stools".
6. **Pick the right session type.** A 45-min breakout makes sense for one deep dive with a demo. The 20-min Tech Talk could work *better* if the goal is to seed a future series of field-stories (Karen's "could be a whole series" hint).
7. **Solo speaker.** Don't request a co-presenter unless it materially improves the talk — the form now treats co-presenters as an exception that needs justification.
8. **Use the "Not on the list" product field if ACE isn't in the dropdown** — Champions get that affordance, no one else does.
9. **Voice: first person, lived experience.** "I ran into…", "what we shipped", "what broke at 3am". The reviewer panel explicitly wants the "you be you" tone over polished marketing prose.
10. **AI is a sparring partner, not a ghostwriter.** Brainstorm with it, get a structure out of it, then rewrite in Matthias' voice. The 800-char limit makes that easy — there's no room for AI fluff anyway.

---

## 7. The customer-experience spine material

From [customer_experience.md](misc/containerization-series/techXchange_topic/customer_experience.md). **Important constraint: no customer is named publicly. Refer to them as "customer 1 / 2 / 3" or "a customer we worked with".** Three real engagements, each contributing a different angle to the talk:

### Customer 1 — the full mechanical journey
The decision log you cannot get from IBM dev. Every choice is stated *with* its rationale *and* a "would I do it again?" tag — which is exactly the unsexy honesty reviewers want.

- **Build images** — baked, custom, `ubi-minimal`-based; *one* image for build, test and runtime to avoid pet-runner drift. Alternative considered: dedicated on-prem runner. Honest verdict: it depends on what you're more comfortable validating — a custom image in Docker, or a runner you can SSH into.
- **Runtime** — native `IntegrationRuntime` operator. "Keep it simple. Supply bar files and config, let the operator do the rest."
- **Credentials** — Vault delivered as a ConfigMap; credentials injected into container env via startup scripts. (Pre-dated Java compute dynamic credentials.)
- **Bar file storage** — GitLab artifact storage. Chosen because the operator needs basic auth and GitLab dresses a token up as basic auth (not all artifact repos do, and the ones that do can come with a price tag). Explicitly rejected the ACE dashboard for storage because: rolling updates are automatic (not always wanted), no versioning, rollbacks become painful.
- **Config overrides** — runtime, Vault work dir, Vault key, secrets-required-at-runtime list, per-app `server.conf.yaml`, plus shared bits: package-registry secret, keystore + keystore password, the bar file for the app and bar files for every required lib.
- **Pipeline** — the glue. Devs write code and minimal config; pipeline auto-resolves transitive dependencies (recursively, until everything is in the bar list), builds all operator-required config, hashes, zips, uploads, tags. "Developers never need to know how to build those specific config files." → modernisation in one paragraph: developer experience preserved, complexity hidden in CI.

### Customer 2 — licensing forces topology decisions
PVU licensing wasn't available, so they licensed a single **worker node** and used **node labels** to pin all ACE containers there. Works — but bulk restarts get awkward because the scheduling surface is now one node wide. That's a real, repeatable architectural trade-off most talks won't admit to.

### Customer 3 — adapter patterns × cloud × licensing
Moving to containers while *also* rolling out adapter patterns means a *lot* of integration servers. Fine on a node-managed system. On cloud, every container — even at 0.1 vCPU — needs licensed capacity to spin up, which changes the cost story.

### The cross-cutting "murmering"
Startup resource contention is largely solved (or at least mitigated) by **dynamic startup scaling**. But runtime licensing isn't. That gap is exactly why customer 2's "license one or two nodes and label-pin" pattern keeps coming up.

**Why this matters for the abstract:** the talk has two natural axes now — the *technical* mechanics (customer 1), and the *economic / topology* consequences (customers 2, 3, plus the murmering). Either one alone is a good talk; the combination is the unique angle. The 45-min and 20-min versions can split exactly along that line.

## 8. Critical files & references

- Source docx (full transcript): `D:\GIT\blogs\misc\containerization-series\techXchange_topic\IBM Champions Enablement_ How to prepare your conference abstract and what reviewers look for.docx`
- Source mp4 (same content, recorded meeting): same folder
- IBM suggestion (Karen → Matthias): [misc/containerization-series/techXchange_topic/ibm_suggestion.md](misc/containerization-series/techXchange_topic/ibm_suggestion.md)
- **Customer-experience notes (3 anonymous customers + cross-cutting murmerings)**: [misc/containerization-series/techXchange_topic/customer_experience.md](misc/containerization-series/techXchange_topic/customer_experience.md) — **never name any customer publicly**
- Extracted plain-text transcript: `D:\tmp\ibm_abstract_text.txt` (63 876 chars, kept for re-reference)
- Existing container blog series: `misc/containerization-series/` (only `handling-k8s-ace-secrets/` is in the repo so far — the other 5+ posts presumably live on the published blog)
- Blog Buddy writing skill (per memory): `D:\GIT\bob_modes\blog_buddy\` — load `references/voice_guide.md` *before* drafting the abstract / talk outline

---

## 9. Decisions made & next steps

**Decisions locked in:**
- **Track**: default to Hybrid cloud management. Confirm at draft time.
- **Anonymisation**: never name customers; "customer 1/2/3" or "a customer we worked with". No internal paths.

**Three talk concepts the user wants on the table:**

1. **"Licensing shapes your cluster topology"** — 20-min Tech Talk.
   User says: "that is one I can really talk about." The strongest under-told angle. Spine: customers 2 (PVU not available → license one worker node, label-pin ACE, deal with bulk-restart fallout) and 3 (adapter patterns → many integration servers → cloud licensing changes the cost model), with the dynamic-startup-scaling murmering as the punchline (startup contention is solved, runtime licensing isn't).

2. **"Journey to containers"** — 45-min breakout.
   The full mechanical story, anchored on customer 1: custom `ubi-minimal` build image used for build/test/runtime, native `IntegrationRuntime` operator, Vault-as-ConfigMap with startup-script credential injection, GitLab artifact storage (and *why not* the dashboard), per-app `server.conf.yaml` overrides, and the pipeline that auto-resolves transitive dependencies so devs never touch operator config.

3. **"Moving to containers — what happens before"** — format TBD.
   The pre-flight talk. Not a project narrative — a *decision framework*. The choices you have to make and the work you have to do *before* you boot a single container: image strategy (baked vs runner), operator vs dashboard, bar-file artifact strategy (and the basic-auth constraint that kills some options), credentials strategy, config layering, pipeline scope. The "what nobody tells you costs the most time" angle.
    - Distinct from #2: #2 says "here's what we did and how it played out." #3 says "here are the choices you have to make and the trade-offs each one buys you." Different audience too — #3 helps people who haven't started yet; #2 helps people mid-journey or auditing their own.

**Submission plan locked in — three abstracts:**

| # | Concept | Format |
|---|---------|--------|
| 1 | Licensing shapes your cluster topology | 20-min Tech Talk |
| 2 | Journey to containers | 45-min breakout |
| 3 | Moving to containers — what happens before | 45-min breakout |

**Sharp differentiation between #2 and #3** (critical, because both are 45-min and both are about containerising ACE — reviewers will read them back-to-back):

- **#2 is retrospective.** Past tense. "Here's the path we took, here's what worked, here's what we'd change. Come for the war stories, leave with patterns you can recognise in your own future migration." Anchor on customer 1, with customers 2/3 as supporting evidence.
- **#3 is prescriptive.** Present/future tense. "You haven't started yet. Here are the four or five decision points you need to settle before you build image #1, and here's the trade-off each option locks you into." Decision framework, walk-out checklist. Customers are illustrative, not the spine.

If both abstracts read like "we containerised ACE and here's what we learned", reviewers will pick one and drop the other. The first paragraph of each abstract has to make the angle unmistakable.

**Next steps:**
1. **Load Blog Buddy voice guide** at `D:\GIT\bob_modes\blog_buddy\references\voice_guide.md` before any drafting.
2. **Pull in anything else** beyond the three customers already in `customer_experience.md` — published blog posts, draft notes, additional engagements. The more concrete decisions-with-rationale we surface, the easier all three abstracts get to write.
3. **Surface concrete from/to numbers** (startup time, image size, deploy cadence, integration servers per worker, vCPU per container, transitive dependencies auto-resolved per build, time-to-rollback, licensed-node vs full-PVU cost ratio). Specificity beats adjectives every time — single most important raw material before drafting.
4. **Draft v1 of all three abstracts side-by-side**: title (≤100 chars), abstract (≤800 chars), justification, three explicit attendee takeaways for each. Drafting them together is the only way to verify #2 and #3 don't accidentally collapse into the same talk.
5. **Differentiation check** — read the three first paragraphs aloud. If #2 and #3 sound like the same submission with different framing, rewrite #3's opening until "you haven't started yet" is the unmistakable hook.
6. **Anonymisation pass** — every draft must scrub customer names, internal paths (e.g. `D:\Projects\<name>\...`), and anything else identifying. Use "a customer we worked with" / "customer 1, 2, 3".
7. **Critique pass** against the negative-signal list in §4 — buzzword bingo, vague verbs, sales tone, AI-fluff.
8. **Confirm track** and verify the 800-char abstract limit on the actual submission form before locking copy.

---

## 10. Verification

This file's job is to make sure Matthias agrees the digest captures the IBM-side guidance correctly *before* we burn time drafting. Verify by:

- Skimming §3 (positive signals) and §4 (negative signals) — does this match the tone Matthias picked up from the video?
- Skimming §6 (guidance applied to this talk) — flag any rule that doesn't fit the story he wants to tell.
- Confirming §2 fact table — especially the 800-char abstract limit and one-speaker rule, since these are the biggest deltas vs. prior years.