# Draft tracker

Status of everything in `misc/` that isn't published to `docs/posts/` yet.
Ordered by completeness. Last full audit: **2026-08-12**.

Statuses: `ready` (one review pass from publishable) · `text-done` (prose finished,
assets/sections missing) · `outline` (notes only, no draft) · `empty` (file exists,
no content).

## Blog drafts

| Status | Draft | ~Words | Missing / next step |
|--------|-------|-------:|---------------------|
| ready | [Validate node or ResetContentDescriptor?](misc/validate-node-or-rcd/validate-node-or-rcd.md) | 1,550 | Rewritten 2026-08-24 to the decision-guide angle (was the incident detective story). All claims measured: 22 requests on ACE 13.0.8.1 incl. Validate node, double-RCD, ASBITSTREAM and JCN toBitstream variants; repro in `C:\Users\Bmatt\IBM\ACET13\workspace\RCDInvalidCharRepro`. Review pass + cover image. |
| ready | [The two ROWs in ESQL](misc/esql-row-function-vs-row-variable/esql-row-function-vs-row-variable.md) | 850 | Drafted 2026-09-03 from the RowOverrideTest diagnostic (`D:\GIT\Ace_test_cases\RowOverrideTest`, three cases Level-3 verified on 13.0.8.1 same day). Voice/angle review + cover image. |
| ready | [Visdeurbel part 2 - prompt tuning](misc/visdeurbel-automated-detection/02.visdeurbel-prompt-tuning.md) | 3,500 | Review pass. Links to part 3, so publish together or in quick succession. |
| ready | [Visdeurbel part 3 - model training](misc/visdeurbel-automated-detection/03.visdeurbel-model-training.md) | 2,700 | Review pass. |
| ready | [Retrieving IIB resources](misc/retreiving-iib-resources/retreiving-iib-resources.md) | 1,500 | Review pass; add the standard "Written by" footer. Companion [discussion-post.md](misc/retreiving-iib-resources/discussion-post.md) is finished. |
| ready | [ACE user environment variables](misc/ace-user-environment-variables/ace-user-environment-variables.md) | 600 | Review pass. Deliberately compact - done as is. |
| text-done | [Hursley 2026 event recap](misc/ace-hursley-2026/ace-hursley-2026.md) | 1,200 | Rough draft 2026-09-02. Needs: photos from Google Photos (list in HTML comment at top), fact-check of version numbers against release notes, NDA scrub (MCP greyed-out exchange, futures line), confirm the pre-emptive auth exchange framing. |
| text-done | [Bob modes](misc/Bob/bob-modes.md) | 1,500 | Four screenshot placeholders to fill; one empty `##` heading near the end needs a title. |
| text-done | [Dynamic startup resources](misc/ace-dynamic-resources/dynamic_startup_resources.md) | 700 | Back half is five TODO sections - blocked on testing on the cgroup-v2 cluster. IBM docs link for `spec.startupResources` still to locate. |
| outline | [Fasttrack snack: Bob](misc/fasttrack-snack-bob/fasttrack-snack-bob.md) | 300 | Demo abstract is written; the post itself isn't started (`## Demo` is empty). |
| outline | [Custom input node development](misc/custom-input-node/custom-input-node-developmend.md) | 50 | Working notes only. |
| outline | [SFTP proxy](misc/sftp-proxy/sftp-proxy.md) | 25 | 8-line setup outline. |
| outline | [Dynamic policy assign](misc/dynamic-policy-assign/dynamic-policy-assign.md) | 35 | 5-line outline. |
| empty | [Using Project Bob to create an ACE app](misc/fasttrack-snack-bob/using-project-bob-to-create-ace-app.md) | 0 | Frontmatter only. |
| empty | [ACE development best practices](misc/ace-development-best-practices/ace-development-best-practices.md) | 0 | Empty file. |
| empty | [Cron input node](misc/cron-input-node/cron-input-node.md) | 0 | Empty file. |

## Not blog drafts (tracked so they don't get mistaken for one)

- [ai_training.md](misc/ai-training-prompt-engineering/ai_training.md) - slide deck + speaker notes for a talk.
- `misc/MQ/` - three heartbeat/keepalive reference notes.
- `misc/containerization-series/` - research, the Madhan blog comparison, and TechXchange abstract material (the series itself is fully published).
- [claud_code_ha/manual.md](misc/claud_code_ha/manual.md), [ace-mcp-open-questions.md](misc/ace-mcp-minikube/ace-mcp-open-questions.md) - notes.

## Published but copies still in misc/

ACE MCP 13.0.7 field guide, MCP on ACE minikube setup, rest-request-basic-auth  - 
live in `docs/posts/`, the `misc/` copies are stale.
