# Submission 5 — Handling ACE secrets across the move to containers

Fields below match the TechXchange 2026 Call for Sessions form.

---

## Session Type

Tech Talk (20 minutes)

## Software/infrastructure products

- IBM App Connect Enterprise (primary)
- HashiCorp Vault (or other external secret store, if listed)
- Red Hat OpenShift / Kubernetes (if available)
- Fall back to the Champions "Not on the list" option if ACE isn't listed.

## Technical Level

200 or 300 (intermediate). Assumes familiarity with ACE secrets handling on a traditional node. Doesn't require Kubernetes operator internals.

## Industry

Cross-industry.

## Session Title (55 chars)

Keep it secret, keep it safe: ACE secrets in containers

## Session Abstract (711 chars, 89 of buffer to 800)

Don't put passwords in your flow. Or in your code. Or in base64-encoded files committed to git. Trust me, I've seen the lot, and plenty of ACE projects still ship them this way. Containers give you other options. The combination that works: ACE vaults for application secrets, Kubernetes secrets mounted, and container env vars for runtime secrets. ESQL reads from env vars at startup. Java compute fetches via the vault interface. Either way, the credential never sits in the image or the repo.

Three takeaways: passwords don't belong in flow, code, or base64 files; ACE vault, k8s secrets, and container env vars are the working combination; ESQL via env vars or Java compute via vault interface, pick by flow.

## Why should this idea be considered for IBM TechXchange 2026? (491 chars)

Passwords in flow logic, in code, in base64-encoded files committed to git. Plenty of ACE projects still ship secrets this way. Most secrets-in-containers content stops at "mount a config map" or "use an external vault". This 20-minute Tech Talk names the bad habit head-on and walks through what replaces it: ACE vault for application secrets, Kubernetes secrets for the keys that unlock them, container env vars for runtime. The audience walks out with a clear pattern that survives audit.

---

## Notes & parked items

**Title**: Lord of the Rings reference ("Keep it secret, keep it safe" — Gandalf to Frodo about the One Ring). Sits in the same playful-reference family as #1 (Bond) and #2 (Friends).

**Source material**:
- Customer 1's secrets approach from [customer_experience.md](customer_experience.md): "Vault, shipped as config map. Credentials for flows loaded into container environment with startup scripts (I think this was before the java compute dynamic credentials, or before we knew about those)."
- The six-approach inventory from [handling-k8s-ace-secrets/research.md](../handling-k8s-ace-secrets/research.md): mqsicredential/mqsisetdbparms in config files, ace vault + mqsicredentials in startup script, ace vault base 64 in git as CR config, ace vault manual upload mapped to file with config map, ace vault with pass in env and startup script for custom nodes, credentials in HashiCorp vault with ACE startup script and trigger restart.
- Blog 03 *"Things to Consider in Containers"* — Configuration Management & Secrets section names environment variables, ConfigMaps/Secrets, external secret stores, ACE vault as viable approaches.
- This blog post is not yet published — the talk will lead the writing.

**Notes for the talk content (not the abstract)**:
- Technical mechanics from this turn's input: create vault → ship to k8s; central key in k8s synced from external vault, injected into containers; at startup load needed secrets into env vars, ESQL reads env vars; alternative is Java compute mode vault interface direct retrieval.
- Worth mentioning briefly that the Java compute vault interface is the newer/cleaner path, the env var approach is what predated it (customer 1 didn't have it available at the time).
