---
date: '2026-03-27'
title: IBM Storage Strategy Days 2026
author: Matthias Blomme
description: 'No middleware this time: two days of IBM Storage'
tags:
- IBM
- AI
- Storage
- Flash
- Ceph
- Fusion
- London
---

![cover](cover.png){ .md-banner }

<!--MD_POST_META:START-->
<div class="md-post-meta">
  <div class="md-post-meta-left">Matthias Blomme · 2026-03-25 · ⏱ 1 min</div>
  <div class="md-post-meta-right"><span class="post-share-label">Share:</span> <a class="post-share post-share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fmatthiasblomme.github.io%2Fblogs%2Fposts%2Fstorage-days-2026%2Fstorage-days-2026%2F" target="_blank" rel="noopener" title="Share on LinkedIn">[<span class="in">in</span>]</a></div>
</div>
<hr class="md-post-divider"/>
<div class="md-post-tags"><span class="md-tag">IBM</span> <span class="md-tag">AI</span> <span class="md-tag">Storage</span> <span class="md-tag">Flash</span> <span class="md-tag">Ceph</span> <span class="md-tag">Fusion</span> <span class="md-tag">London</span></div>
<!--MD_POST_META:END-->

# No middleware this time: two days at the IBM Storage Strategy Event

No middleware this time, sorry. I wanted to know more about storage for a change.

That alone already made this event a bit different for me. Usually I end up orbiting around integration, middleware, agents, automation, and whatever else is happening closer to the application side. This time I deliberately looked lower in the stack. Personal growth, apparently.

After two days at the IBM Storage Strategy Event, I did not come away with some sudden urge to become a storage specialist, but I did leave with a new appreciation for the people who are. There is a lot going on with storage. What stuck with me most, though, was something a bit more interesting than that. Storage is clearly being pushed much closer to the center of the AI conversation, and not just as the place where data happens to sit until something smarter comes along.

That much was hard to miss over those two days. I did not walk away thinking storage had suddenly become glamorous. I did walk away thinking it is becoming a lot harder to treat it as background infrastructure.

## Why this actually caught my attention

What made it interesting for me is that I did not go there expecting storage to suddenly become the most interesting part of the stack. If anything, I expected a couple of useful updates, a few product slides, and the usual amount of strategic wording wrapped around infrastructure.

Instead, what kept coming back was how directly storage is now being tied to AI. Not in the vague “AI-ready” way that gets pasted onto everything these days, but in a more practical sense. The message underneath a lot of it was pretty clear: if AI is going to do anything useful with enterprise data, then storage is no longer just sitting quietly in the background.

That was probably the part that landed best for me over those two days. The real bottleneck is not just the model, or the GPU, or your benchmark numbers, or all of the above. It is the data. Where it sits, how fast you can get to it, how well it moves, how much it costs, and how painful it is to manage once it has to work in a real environment.

That shift in emphasis is what made the event interesting to me. Not storage on its own, but storage being pulled much closer to where AI either becomes useful, or falls apart.

## How I started reading the event

It took me a little while to notice it, later than I would care to admit, but these three principles were actually a pretty useful way to make sense of the event.

[Screenshot placeholder: slide showing Portfolio and Product Simplification, AI Everywhere, and Platform Delivery as a Service]

Portfolio and Product Simplification mostly showed up as hardware updates and improvements. That gave that part of the event a more familiar structure: what is new, what is better, what is being streamlined, and where things are being cleaned up.

AI Everywhere was broader, and also the part that came back the most. That covered how storage supports AI workloads, how AI is being used in provisioning and management, and the more concrete AI use cases and customer stories. That part felt like the most active thread running through the event.

Platform Delivery as a Service was where things like Fusion, Ceph, Red Hat AI, and Ansible for storage provisioning started to fit together a bit better for me. That was less about one specific storage box or update, and more about how the whole thing gets packaged, delivered, and operated.

Once I started looking at the sessions through those three buckets, the event became easier to follow. Some sessions sat very clearly in one of them, others overlapped a bit, but at least there was a structure underneath it all.

## A few things I kept noticing

Once I had that structure in my head, a few things became hard to miss.

Ceph showed up a lot. Fusion too. CAS as well, especially later in the day. KV cache had a pretty strong presence as well. None of those felt like random mentions. They were clearly part of where a lot of the attention was going.

What also stood out is that this was not only about storage keeping up with AI workloads. It was also about storage helping shape how those workloads get used in practice. Your own data kept coming back as the real value point in all of that. Not AI as a generic layer on top, but AI that actually has access to the data that makes it useful for a business in the first place.

There were also a few side moments that stuck with me for different reasons. Bob made an appearance too, which I did not expect here, but it fit better than I thought. And yes, somehow even tape managed to work its way back into the story as well. With a bold statement.

That mix says quite a lot about the event itself. On one side, very current AI themes like CAS, KV cache, inferencing, and data access. On the other, tape walking back in like it still has unfinished business. Storage covers a lot of ground, apparently.

## Wrapping this up

After two days at the IBM Storage Strategy Event, that is probably the clearest takeaway for me: AI needs storage, and storage needs AI.

That sounds neat, maybe a little too neat, but it does capture what kept showing up across the event. Storage is not being treated as the quiet bit underneath anymore. It is being pushed forward as part of how AI workloads get fed, managed, governed, and turned into something useful with real enterprise data.

I did not leave as a storage expert, and that was never the plan. I did leave with a better understanding of why storage specialists have been busy all along, and why the rest of us probably need to pay a bit more attention as well.