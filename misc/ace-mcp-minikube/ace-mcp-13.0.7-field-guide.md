---
title: 'IBM App Connect and MCP: a field guide as of 13.0.7'
date: 2026-06-27
author: Matthias Blomme
description: What MCP looks like across ACE software and App Connect in containers, where the docs cover it, and where you still have to read the YAML.
tags:
  - ace
  - app-connect
  - mcp
  - model-context-protocol
  - ai
  - integration
status: draft
---

![cover](../../docs/posts/Ace-Operator-Minikube/cover_field_guide.png){ .md-banner }

<!--MD_POST_META:START-->

<!--MD_POST_META:END-->


# IBM App Connect and MCP: what's actually there in 13.0.7

There are at least four different things in the App Connect product family that get called "MCP" today, and the documentation for them is spread across `docs.ibm.com`, the ACE community blog, the operator image manifest, and a handful of comments inside `server.conf.yaml`. This post pulls together what's verifiable from the docs and release blogs, what's visible in the shipped product but not yet documented, and what still needs confirmation.

Versions referenced throughout:

- ACE software **13.0.7.0** (where the on-prem MCP features ship)
- App Connect Operator **12.20.0** and the **13.0.0** line
- App Connect Dashboard **13.0.6.1-r1** (Dashboard MCP server arrives) and **13.0.7.0-r1** (Enterprise Agent arrives)

Status used in the tables below:

- `verified`: confirmed in IBM docs or in the shipped product
- `partial`: found but partial or undocumented
- `unverified`: plausible, from a single source, needs second eyes

---

## The four MCP-flavoured things in App Connect today

| #  | Component                         | Where it lives                   | What it exposes                                                      | First shipped         | Documented  |
|----|-----------------------------------|----------------------------------|----------------------------------------------------------------------|-----------------------|-------------|
| 1  | `MCP.Runtime`                     | `server.conf.yaml`               | Deployed Toolkit REST API operations as MCP tools                    | ACE 13.0.7.0          | verified    |
| 2  | `MCP.Admin`                       | `server.conf.yaml`               | "ACE administration tools"                                           | ACE 13.0.7.0          | partial     |
| 3  | `spec.mcp.runtime`                | Integration Runtime CR           | Connector-based MCP server hosted in container                       | Dashboard 13.0.6.1-r1 | verified    |
| 4  | `acemcp` / `langgraph` containers | App Connect Enterprise Agent pod | Container/runtime/flow introspection for the embedded Dashboard chat | Operator 13.0.0 line  | unverified  |

Same protocol, different audiences. Items 1, 2, and 3 expose tools to *external* MCP clients (Claude, IBM Bob, Cursor, ChatGPT, your own agent). Item 4 is internal plumbing for IBM's embedded chat experience and isn't intended for direct agent consumption.

---

## On-prem ACE: MCP in `server.conf.yaml`

ACE 13.0.7.0 introduces a top-level `MCP:` block with two sibling stanzas, `Admin:` and `Runtime:`. Both default to off / commented out. Both are separate HTTP listeners running inside the integration server process, on separate ports.

### MCP.Runtime: exposing REST APIs as MCP tools

The headline 13.0.7.0 feature. Pick an existing REST API flow already deployed to an integration server, pick which operations to expose, and they show up as MCP tools that any compliant client can list and invoke. Tool descriptions are generated from the REST API's OpenAPI specification.

**Block as shipped:**

```yaml
MCP:
  Runtime:
    #mcpStartMode: 'automatic'       # 'enabled' | 'automatic' (default) | 'disabled'
    #host: ''                        # Hostname for the MCP Runtime server; empty = FQDN
    #port: 7750                      # default 7750
    #uriSuffix: '/mcp'               # default /mcp; e.g. localhost:7750/mcp
    #mcpCredentialName: ''           # credential alias; type 'mcp', username + password
    #propagateIdentity: true         # forward incoming Authorization header to the flow
    #sslMode: 'automatic'            # 'automatic' (default) | 'disabled'
    #sslCertificate: ''              # p12 or pem path
    #sslPassword: 'mcp::sslpwd'      # passphrase or credential alias
    #requireClientCert: true         # mTLS
    #caPath: '/path/to/CA/certificates'
    #tlsCipherList: ''
    #tlsTrace: false
```

`mcpStartMode` semantics matter:

1. **`enabled`**. Listener comes up at server start even with zero tools deployed.
2. **`automatic`** (default). Listener starts when at least one tool is deployed, stops when the last one is removed.
3. **`disabled`**. Listener never starts.

`mcpCredentialName` is a reference to an ACE credential of type `mcp`. You create it via `mqsicredentials` / the vault, and when set, every MCP request needs a Basic Auth header carrying that credential.

**Default endpoint:** `https://localhost:7750/mcp`

**Transport:** Streamable HTTP only. The older SSE transport is **not** supported.

#### Web UI flow to expose a REST API

1. Open the ACE Web UI (default `http://localhost:7600`)
2. Open the context menu on a deployed REST API
3. Pick **Expose MCP tools**
4. Select operations, set tool name / title / description / enabled per tool
5. Confirm

If `mcpStartMode` is `automatic`, the MCP server starts on first tool deployment.

#### Verifying it's running

```
curl https://localhost:7750/mcp
```

Or attach an MCP client:

- MCP Inspector, <https://github.com/modelcontextprotocol/inspector>
- Claude Desktop / Cursor / VS Code with a Streamable HTTP MCP server entry

### MCP.Admin: the undocumented sibling

This is the part that started the whole investigation. It's in the same shipped `server.conf.yaml`, immediately above the Runtime block, and IBM doesn't currently document it anywhere I can find.

**Block as shipped (literally two lines of comments):**

```yaml
MCP:
  Admin:
    # enabled: false                 # Start MCP server and register ACE administration tools
    # port: 7650                     # Port number for MCP server
```

Two properties. Default `enabled: false`. Default port **7650**.

**What it almost certainly is:** an MCP server that registers integration-server administration operations as tools, so an MCP-enabled agent can introspect or operate the server itself. List runtimes, list deployed flows, query status, possibly start/stop. Same idea as the `acemcp` container in the Enterprise Agent pod (see below), but for standalone.

**What we don't know without testing:**

- The exact set of tools registered when `enabled: true`
- Whether it inherits TLS and auth from `RestAdminListener` or is plaintext + unauthenticated by default
- Whether the exposed tools are read-only (mqsilist-style) or include mutating actions like start/stop/deploy
- Whether IBM plans a formal announcement in 13.0.8.0 or whether it's a quiet ship-then-document approach
- Whether there are hidden additional properties (sslMode, mcpCredentialName, propagateIdentity) that just aren't surfaced in the default YAML

**How to find out (and what I'm doing in minikube):**

1. Set `enabled: true`, restart the integration server
2. Connect MCP Inspector to `http://localhost:7650/` (try `https://` first if the RestAdminListener is on HTTPS)
3. Run `tools/list`. That *is* the documentation until IBM publishes a reference
4. Test a read-only tool first; only escalate if you trust the environment

Once we have `tools/list` output, this section can be replaced with the real list.

> "Vindication!" - Captain Holt, Brooklyn Nine-Nine

---

## In containers: App Connect Dashboard MCP servers

Distinct from the on-prem feature. The Dashboard wizard creates MCP servers built on App Connect **connectors**, not on Toolkit REST APIs. You authenticate to Salesforce / Slack / Insightly / etc., pick the actions you want, and those become MCP tools.

### Availability

- App Connect Operator **12.20.0** or later
- Dashboard at **`13.0.6.1-r1`** or later
- Hosting: Red Hat OpenShift, or IBM Cloud Kubernetes Service at integration runtime **`13.0.6.2-r1`** or later
- Other Kubernetes flavours: no automatic ingress, so you handle routing yourself

### What the wizard generates

For each MCP server you create:

1. A new integration runtime named after the MCP server, preconfigured for hosting MCP
2. A configuration of type **`Accounts`** (`mcpServerName-acc`) holding application credentials
3. A configuration of type **`REST Admin SSL files`** (`mcpServerName-ir-adminssl`)
4. A configuration of type **`setdbparms.txt`** (`mcpServerName-mcp-ba-creds`) holding the MCP endpoint's basic auth credentials
5. A BAR file (`mcpServerName-{generatedID}-MCP`) deployed to that runtime

On OpenShift a route is created automatically. On IKS you enable ingress on the runtime CR:

```yaml
spec:
  ingress:
    enabled: true
  version: '13.0.6.2-r1'
  license:
    accept: true
    license: L-CKFT-S6CHZW
    use: AppConnectEnterpriseProduction
```

### Integration Runtime CR: MCP knobs

```yaml
spec:
  mcp:
    runtime:
      disabled: false                              # default false; runtime container hosts the MCP server
      basicAuth:
        disabled: false                            # default false; Basic Auth on by default
        secretName: my-mcp-basic-auth-secret       # auto-generated if omitted
      tls:
        disabled: false                            # default false; TLS on by default, self-signed cert generated
        secretName: my-mcp-tls-secret              # auto-generated if omitted
```

### TLS secret format

Standard Kubernetes TLS secret:

```bash
oc create secret tls my-mcp-tls-secret --cert=certificate.crt --key=private.key
```

### Basic Auth secret format (unverified)

Reported but unverified. The secret has a `configuration` field whose base64-decoded value is

```
mcp::basicAuthOverride username password
```

The `mcp::` prefix matches the `setdbparms.txt` credential convention used elsewhere in App Connect, and the on-prem yaml uses the same prefix in `mcp::sslpwd`. The exact keyword `basicAuthOverride` is what I couldn't confirm in any IBM doc page. **Decode an auto-generated secret from a real Dashboard-created MCP server before scripting against it.**

---

## The App Connect Enterprise Agent (different beast)

This is the embedded Dashboard chat feature. It uses MCP internally (not as a public endpoint for your agents) and is what you've probably seen referenced as IBM's "agentic AI chat experience" for App Connect.

### What it is

An embedded AI chat inside the Dashboard UI. You click a chat button, ask "which integration runtimes are running?" or "what does flow X expose?", and it answers using watsonx.ai-hosted LLMs and live introspection of your container deployment.

Per the IBM docs, the Agent:

- Provides realtime visibility into container topologies, licensing, and usage
- Inspects deployed message flows for triggers, exposure, dependencies, and deprecated components
- Offers guidance about deployment changes across runtimes, resources, flows, credentials, and policies
- Queries the IBM knowledge base (docs, TechXchange, support cases) for pre-trained content

### Enabling

```yaml
spec:
  agents:
    enabled: true
    customSecretName: secretName
  api:
    enabled: true
  version: '13.0'
  logFormat: json
```

The Dashboard API must be enabled because the Agent uses it to retrieve information from the managed App Connect environment.

The custom secret needs watsonx.ai credentials:

```yaml
stringData:
  WATSONX_API_KEY: your-api-key
  WATSONX_HOST_URL: your-watsonx-host-url
  WATSONX_PROJECT_ID: your-project-id
```

### What runs in the pod

Two containers are documented in the operator image manifest:

- **`acemcp`**, internal MCP server exposing container topology, runtime status, flow metadata, etc., as tools
- **`langgraph`**, the orchestration loop driving the chat agent

Image references confirmed in the IBM Cloud Pak image manifest: `cp/appc/ace-mcp`, `cp/appc/ace-mcp-prod`, `cp/appc/ace-kube-mcp`, `cp/appc/ace-kube-mcp-prod`, `cp/appc/ace-langgraph-agents-prod`. There are both `ace-mcp` and `ace-kube-mcp` variants, and the purpose of the distinction isn't documented.

### `spec.pod.containers.acemcp.*` and `spec.pod.containers.langgraph.*` (unverified)

Reported as the customisation paths on the Dashboard CR. The pattern matches how the operator lets you override container resources, image, and pull policy on other Dashboard/Designer containers, so it's plausible. Confirm with:

```bash
oc explain dashboard.spec.pod.containers
```

against your actual operator install.

---

## Security notes

Same hygiene as anywhere MCP is exposed:

1. Expose the **minimum** set of tools, especially for `MCP.Admin` if and when you turn it on
2. Avoid mutating tools unless you've thought through what an LLM doing the wrong thing can break
3. Use Basic Auth at minimum (via `mcpCredentialName` for Runtime, via `setdbparms` for Dashboard MCP servers)
4. Use TLS. Default-on for both Runtime and Dashboard MCP, but verify when you swap to your own certs
5. For sensitive environments, terminate at a gateway with finer-grained auth (OAuth, mTLS, scope enforcement). IBM's own ContextForge MCP Gateway is one option
6. Tool **descriptions** matter. Agents use them to decide when to call a tool. Sloppy descriptions cause sloppy tool selection
7. Use dedicated, least-privilege backend credentials for any account the MCP tools wrap

---

## What's still open

1. **What tools `MCP.Admin` actually registers**. Top priority. The minikube test should answer this.
2. **Whether `MCP.Admin` honours its own TLS/auth or inherits from `RestAdminListener`**. Comments don't say.
3. **The exact basic auth secret payload for Dashboard MCP servers** (`mcp::basicAuthOverride` vs whatever it actually is). Decode an auto-generated secret.
4. **Operator/Dashboard versions where the Agent and `acemcp` first shipped GA**. Operator 13.0.0 / Dashboard 13.0.7.0-r1+ is the working answer, not yet confirmed.
5. **Whether `MCP.Admin` is preview/unsupported or production**. Worth asking your IBM rep.

---

## Reference list

### Official IBM documentation

| Status     | Topic                                                                                  | Link |
|------------|----------------------------------------------------------------------------------------|------|
| verified   | Creating and managing MCP servers (Dashboard)                                          | <https://www.ibm.com/docs/en/app-connect/13.0.x?topic=dashboard-creating-managing-mcp-servers> |
| verified   | Creating a Model Context Protocol (MCP) server                                         | <https://www.ibm.com/docs/en/app-connect/13.0.x?topic=cmms-creating-mcp-server> |
| verified   | Exposing a REST API as an MCP tool                                                     | <https://www.ibm.com/docs/en/app-connect/13.0.x?topic=tools-exposing-rest-api-as-mcp-tool> |
| partial    | Configuring MCP properties (server.conf.yaml reference). Runtime properties only, no Admin | <https://www.ibm.com/docs/en/app-connect/13.0.x?topic=tools-configuring-mcp-properties> |
| verified   | Using the IBM App Connect Enterprise Agent                                             | <https://www.ibm.com/docs/en/app-connect/13.0.x?topic=dashboard-using-app-connect-enterprise-agent> |
| verified   | Integration Runtime reference. Custom resource values (`spec.mcp.runtime.*`)           | <https://www.ibm.com/docs/en/app-connect/certc_install_integrationruntimeoperandreference.html#crvalues> |

### Release notes and blog posts

| Status     | Topic | Link |
|------------|-------|------|
| verified   | Ben Thompson, ACE 13.0.7.0 features (MCP REST API exposure) | <https://community.ibm.com/community/user/blogs/ben-thompson1/2026/03/26/ace-13-0-7-0> |
| verified   | Ben Thompson, ACE 13.0.6.0 features | <https://community.ibm.com/community/user/blogs/ben-thompson1/2025/12/11/ace-13-0-6-0> |
| verified   | ACE 13.0 release notes / fix list | <https://www.ibm.com/support/pages/ibm-app-connect-enterprise-130-release-notes> |

### Community and ecosystem

| Status     | Topic | Link |
|------------|-------|------|
| verified   | IBM MCP repository (MQ, watsonx.data, OpenPages, BAW, z/OS Connect, API Connect for GraphQL, webMethods, etc.) | <https://github.com/IBM/mcp> |
| verified   | ContextForge MCP Gateway (AI gateway fronting MCP/A2A/REST) | <https://github.com/IBM/mcp-context-forge> |
| verified   | MCP Inspector (test harness) | <https://github.com/modelcontextprotocol/inspector> |
| verified   | Model Context Protocol spec | <https://modelcontextprotocol.io/docs/getting-started/intro> |
| verified   | IBM Cloud Pak image manifest (confirms `ace-mcp` / `ace-langgraph-agents-prod`) | <https://github.com/IBM/cloud-pak/blob/master/reference/image-manifests/ibm-cp-integration.yaml> |

### Unverified items worth chasing

| Status     | Item | Notes |
|------------|------|-------|
| unverified | `mcp::basicAuthOverride username password` secret payload | Decode an auto-generated Dashboard MCP secret to confirm |
| unverified | `spec.pod.containers.acemcp.*` and `spec.pod.containers.langgraph.*` | `oc explain` against the live CRD |
| partial    | `MCP.Admin` properties beyond `enabled` and `port` | Likely inherits from RestAdminListener; not stated |
| partial    | Operator / Dashboard versions for Agent GA | Working answer: Operator 13.0.0 / Dashboard 13.0.7.0-r1+ |
| partial    | Tools registered by `MCP.Admin` | Test on minikube, run `tools/list`, capture |

---

## Appendix: minimal test setup for `MCP.Admin`

```yaml
# server.conf.yaml, minimal Admin MCP enablement
MCP:
  Admin:
    enabled: true
    port: 7650
```

```bash
# restart the integration server
mqsistop <node>
mqsistart <node>

# or for an independent server
# (Ctrl-C the IntegrationServer process and re-launch with --work-dir)
```

```bash
# point MCP Inspector at it
npx @modelcontextprotocol/inspector
# then in the UI: Streamable HTTP, URL = http://localhost:7650/  (try https:// if RestAdminListener is on TLS)
```

Capture the output of `tools/list` and `tools/call` for any read-only tool. That's the documentation that doesn't exist yet.
