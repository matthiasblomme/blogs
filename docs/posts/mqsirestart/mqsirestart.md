---
date: 2026-04-02
title: mqsirestart
author: Matthias Blomme
description: mqsirestart solves all your restart needs!
tags:
- ace
- mqsistop
- mqsistart
- mqsirestart
reading_time: 5 min
---

![cover](cover.png){ .md-banner }

<!--MD_POST_META:START-->
<div class="md-post-meta">
  <div class="md-post-meta-left">Matthias Blomme · 2026-4-02 · ⏱ 5 min</div>
  <div class="md-post-meta-right"><span class="post-share-label">Share:</span> <a class="post-share post-share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fmatthiasblomme.github.io%2Fblogs%2Fposts%2Fmqsirestart%2Fmqsirestart%2F" target="_blank" rel="noopener" title="Share on LinkedIn">[<span class="in">in</span>]</a></div>
</div>
<hr class="md-post-divider"/>
<div class="md-post-tags"><span class="md-tag">ace</span> <span class="md-tag">mqsistop</span> <span class="md-tag">mqsistart</span> <span class="md-tag">mqsirestart</span></div>
<!--MD_POST_META:END-->


# mqsirestart — the best thing since sliced bread

Are you tired of having to perform **2 separate commands** just to restart an integration server or node?

Are you tired of precious seconds ticking away while you hunt and peck for that second command?

Are you tired of getting an urgent call mid-restart, forgetting to type `mqsistart`, and causing an **unplanned outage** that your manager is now asking questions about?

Are you tired of **typos**? Of `mqsistpo`? Of `mqsisart`? Of the shame?

**WELL. NO. MORE.**

> *"I used to type two commands every single time. Two! Can you imagine? That's one too many." — A relieved IBM ACE administrator, probably*

---

# Introducing: `mqsirestart`

The **ONE command** that does it ALL.

`mqsirestart` offers the exact same familiar interface as `mqsistart` and `mqsistop` — except it does **BOTH**. In one go. Back to back. Like clockwork. Like a dream. Like a well-oiled integration middleware machine.

✅ **Drastically** cuts time between your stop and start command  
✅ Eliminates the gap where things go wrong — and oh, things go wrong  
✅ Keeps your **uptime high** and your **incident count low**  
✅ Works on integration **servers** *and* integration **nodes** — yes, BOTH  

And the best part? You already know how to use it. It's `mqsistart` and `mqsistop`. Combined. *That's it.* We didn't reinvent the wheel — we just stopped making you spin it **twice**.

---

# Here's how to use it

**Restart an integration server:**

```
> mqsirestart.cmd ACE13 --integration-server IS
Stopping integration server IS on node ACE13

BIP1188I: Stopping the integration server with URI '/apiv2/servers/IS'...
BIP1189I: The integration server with URI '/apiv2/servers/IS' is reported as stopped.
BIP8071I: Successful command completion.

Starting integration server IS on node ACE13

BIP1186I: Starting the integration server with URI '/apiv2/servers/IS'...
BIP1187I: The integration server with URI '/apiv2/servers/IS' is reported as started.
BIP8071I: Successful command completion.
```

**Restart an integration node:**

```
> mqsirestart.cmd ACE13
Stopping integration node ACE13

BIP8071I: Successful command completion.

Starting integration node ACE13

BIP8096I: Successful command initiation, check the system log to ensure that the component started without problem and that it continues to run without problem.

```

Same flags. Same syntax. Same you — just *better*.

---

# But wait — there's MORE!

Because `mqsirestart` doesn't just save you time. It saves you from **yourself**.

We've all been there. It's 4:47 PM on a Friday. You type `mqsistop`. You get a Slack notification. You glance away. You forget. You leave for the weekend. Monday morning, 8:03 AM — your inbox is a war zone. `mqsirestart` removes that whole scenario from your life. **Completely.** Stop and start happen together, sequentially, automatically, *reliably*.

> *"I'm not saying mqsirestart saved my marriage, but I'm not saying it didn't."  
> — Anonymous, Senior Integration Engineer*

---

# So what are you waiting for?

Stop juggling two commands like it's 2009. Stop living in a world of unnecessary risk. Stop the madness.

Use `mqsirestart` today — your integration environment will thank you, your team will thank you, and honestly? **You'll thank you.**

Availabe as a free download for a limited time, [get yours now!](https://github.com/matthiasblomme/ACE_MQ_Tooling/blob/656191e1205827fe461cb42e7f58044a8bd01afe/ACE/Administration/mqsirestart.cmd)!

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#AppConnectEnterprise
