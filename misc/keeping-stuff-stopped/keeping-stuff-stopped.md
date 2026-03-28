---
date: 2026-03-31
title: Keeping stuff stopped in IBM ACE
description: How to start an IBM ACE integration server without starting everything
  in it, and how to keep flows stopped across deployments.
tags:
- ace
- operations
---

![cover](cover.png){ .md-banner }

<!--MD_POST_META:START-->

<!--MD_POST_META:END-->

# Keeping stuff stopped in IBM ACE

Sometimes you need to start an integration server, but you don't want everything inside it to start with it. Maybe you're
doing maintenance on a specific flow. Maybe you're deploying a new version that shouldn't go live yet. Maybe you just need
the server up for inspection without processing traffic.

Whatever the reason, ACE gives you a few tools to control what starts and what doesn't. But they don't all behave the
same way, and mixing them up can lead to surprises. Let's walk through them.

## .stopped files

The most direct way to prevent a flow or application from starting is a `.stopped` file. When the integration server starts, 
it checks each application's run directory for a file literally named `.stopped`. If one is found, the flows in that application,
or the entire application, won't start.

The file lives here for a node manged environment:

```
{MQSI_WORKPATH}/components/{NodeNAme}/servers/{ServerName}/overrides/{ApplicationName}/.stopped
{MQSI_WORKPATH}/components/{NodeNAme}/servers/{ServerName}/overrides/{ApplicationName}/{namespace}/{flowname}/.stopped
```

And here for Standalone Integration Servers:

```
...
```

You don't need anything in the file. Its presence is enough. Create it before starting the server, and the application
sits idle while everything else comes up normally.

```bash
touch /home/aceuser/ace-server/run/MyApplication/.stopped
```

This works on both standalone integration servers and integration servers connected to a node. The server starts, sees
the file, skips the application, and moves on.

This approach survives a lot of things that would otherwise bring your flows back to life: restarts, crashes, anything
short of a deploy. Which brings us to the next problem.

## mqsistopmsgflow and mqsistartmsgflow

If the server is already running and you want to stop a specific flow without restarting anything, you can use the
`mqsistopmsgflow` and `mqsistartmsgflow` admin commands.

The commands work slightly differently depending on whether you're targeting a standalone integration server or one
managed by a node.

**Standalone integration server:**

```bash
mqsistopmsgflow --admin-host <hostname> --admin-port <port> --application <ApplicationName> --flow <MessageFlowName>
```

**Integration server on a node:**

```bash
mqsistopmsgflow <integrationNodeName> --integration-server <IntegrationServerName> --application <ApplicationName> --flow <MessageFlowName>
```

**Start it again (same pattern):**

```bash
mqsistartmsgflow --admin-host <hostname> --admin-port <port> --application <ApplicationName> --flow <MessageFlowName>
```

The default admin port for a standalone integration server is `7600`. You can also target an entire application by
omitting `--flow`, or use `--all-applications` to hit everything in the server at once.

These commands are great for operational control. They're immediate and don't require a restart. But there's a catch that
catches people off guard.

### The deploy problem

If you stop a flow using `mqsistopmsgflow` and then deploy a new BAR file for that application, the flow comes back up.
Deployment resets the started state. The server doesn't know that you deliberately stopped the flow before the deploy
happened, so it starts everything fresh.

This means `mqsistopmsgflow` is useful for temporary operational holds, but it's not a reliable way to keep something
stopped across deployments.

To do that properly, you need either a `.stopped` file (which persists across deploys) or something in the BAR itself.

## startMode

The BAR file has a property called `startMode` that controls whether an application or flow starts automatically after
being deployed or when the server restarts.

The `startMode` property controls whether flows start automatically. There are three valid values:

| Value | Behaviour |
|---|---|
| `maintained` | Default. Starts on deploy, stays running until explicitly stopped. |
| `automatic` | Always started after deploy, redeploy, or server restart. |
| `manual` | Never starts automatically. Must always be started explicitly. |

Setting `startMode` to `manual` tells the server not to start the application automatically. It gets deployed, it's
present in the server, but it doesn't process anything until you explicitly start it.

You set this in the BAR file's overrides. In the toolkit, this shows up in the BAR editor under the properties for
the application or library. Via command line, you'd pass it as part of an override properties file. The property is
set at flow level using `#` as a separator:

```properties
MyMessageFlow#startMode=manual
```

> **Note:** IBM documentation shows the flow-level syntax clearly. If you want to apply `startMode` at the application
> level rather than per-flow, verify the exact syntax — it may require using `mqsiapplybaroverride` with `-k` for the
> application name rather than the properties file format above.

Pass the override file to `ibmint deploy` using `--overrides-file`:

```bash
ibmint deploy --input-bar-file MyApplication.bar \
              --output-work-directory /home/aceuser/ace-server \
              --overrides-file overrides.properties
```

With `startMode=manual`, the application survives a deploy in a stopped state. You can deploy a new version, it lands in
the server, and nothing starts until you call `mqsistartmsgflow` or flip the startMode back to `automatic`.

This is the right tool when you need long-lived control that survives the deploy cycle.

## Deploying without starting — needs more research

There's a related question worth exploring: can you deploy a BAR file to a running server and have the flows *not* start,
without setting `startMode=manual` ahead of time in the BAR itself?

In older IIB/broker setups, some deployment commands had flags or behaviors that controlled whether flows were started
after deploy. In modern ACE with `ibmint deploy`, it's not entirely clear if there's a direct equivalent flag. The
`startMode` approach above is the cleanest known path, but it requires the property to already be in the BAR or override
file.

> **TODO:** Test whether `ibmint deploy` has a flag or behavior that deploys content without starting it, regardless of
> what's in the BAR. Also worth checking: if a `.stopped` file exists when a deploy happens, does it actually suppress
> the post-deploy start?

This section needs more testing before drawing conclusions. Will update once verified.

## Summary

| Approach | When it works | Survives deploy? | Survives restart? |
|---|---|---|---|
| `.stopped` file | Before server start | Yes | Yes |
| `mqsistopmsgflow` | While server is running | No | No |
| `startMode=manual` | At deploy time (in BAR) | Yes | Yes |

The three tools cover different scenarios. If you need to start a server clean and keep certain things idle from the
beginning, `.stopped` files are your friend. If you need runtime operational control, reach for `mqsistopmsgflow`. If
you need something that holds across the deploy cycle, `startMode=manual` is the right answer.

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#AppConnectEnterprise(ACE)
