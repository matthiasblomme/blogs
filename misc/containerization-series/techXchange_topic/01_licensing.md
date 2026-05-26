# Submission 1: Licensing as the lens for ACE in containers

Fields below match the TechXchange 2026 Call for Sessions form. Status is **dialog-in-progress**; locked items marked LOCKED.

---

## Session Type

Tech Talk (20 minutes)

## Software/infrastructure products

- IBM App Connect Enterprise (primary)
- Red Hat OpenShift / Kubernetes (secondary, if available in the dropdown)
- Fall back to the Champions "Not on the list" option if ACE isn't listed.

## Technical Level

200 or 300 (intermediate). Built on assumed familiarity with ACE and containers, but does not require deep K8s internals.

## Industry

Cross-industry.

## Session Title 

License to scale: ACE in containers


## Session Abstract

Running ACE in containers looks different through the lens of licensing. Containers scale on demand, ideally. Per-container licensing makes every spinup a license check. You over-provision or auto-scaling stops being elastic. Same with resource sizing: per-container, every CPU bump is a license bump; pinned to a worker node, you have room to tune. Runtime scoping follows suit: bundle tight and one spike raises the whole container's license usage; split wide and each flow becomes its own license event. This conversation belongs in the right rooms, with engineering at the table.

Three takeaways: scaling, sizing, and scoping all look different under the licensing model. Per-container and pinned-node paths split engineering work differently. Engineering belongs at the table, not just procurement.

## Why should this idea be considered for IBM TechXchange 2026?

The IBM Champions program and the ACE team both mentioned field stories as the gap worth filling. Licensing rarely gets its own session, even though it shapes how containers actually scale, get sized, and get scoped. This Tech Talk walks through real customer engagements: PVU not available, adapter patterns multiplying integration servers on cloud, dynamic startup resources changing the comparison. The 20-minute format means one sharp angle, not a survey. The audience walks out knowing why licensing belongs in the conversation when engineering picks a container topology, and what it costs not to have it there.


---

## Notes & parked items

**Parked opener variants** (in case we want to revisit):
- *Running ACE in containers brings the usual technical conversations. Through the lens of licensing, those conversations all change shape.*
- *Setting up, deploying, and updating ACE in containers all look different through the lens of licensing.*

**Source material drawn on:**
- Customer notes (anonymized): three engagements covering PVU-not-available with node-labeling, adapter-pattern integration server multiplication on cloud, and the dynamic-startup-scaling murmuring. See `customer_experience.md`.
- Published blog 04 *"Scoping your runtimes"*, the "Licensing cost" subsection is the seed of the runtime-scoping beat in the abstract.
- Published blog 03 *"Things to Consider in Containers"*, the Scaling section is the seed of the auto-scaling beat.
- IBM Rob Convery blog (Oct 2025) on dynamic CPU allocation for faster startup, supports the "dynamic startup resources changed the comparison" point if we use it in the talk.

**Parked titles**

(Parked alternatives: *ACE in containers: the licensing conversation* (45), *Suit up: the licensing lens on ACE in containers* (49), *Running ACE in containers, through the licensing lens* (54), *The licensing lens on ACE in containers* (40), *Licensing decisions for ACE in containers* (41), *ACE in containers: have you met licensing?*)