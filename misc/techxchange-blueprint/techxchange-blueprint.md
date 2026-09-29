---
title: 'Too many sessions? The IBM Champions built you a planner'
date: 2026-09-28
author: Matthias Blomme
description: The IBM Champions built a Growth Blueprint kiosk for the IBM Community
  booth at TechXchange 2026. Four questions, three minutes, and you walk away with
  sessions, Champions to meet and groups to join. Plus a stripped-down version you
  can run now if you can't wait.
tags:
- techxchange
- ibm-champion
- ibm-community
- bob
- event
status: draft
reading_time: 5 min
---

<!--
Teaser, text complete. Open before publishing: see the list below.
Post-event update idea: a photo of the booth once it's set up.

Sources for the booth facts:
- notes/meetings/2026-09-21-ibm-champions-working-group-kickoff-onenote.md
  (Learn to Earn journey, location, laptops, go-live time)
- D:/Projects/Bob/txc26-growth-blueprint (the prototype; screenshots taken from a local
  run on 2026-09-28, branch fix/main-repairs-and-pass-on-sign-in, mocked sign-in and
  mocked LLM text)
- Planner skill: D:/GIT/bobmodes/bobmodes/techxchange-planner, public repo
  https://github.com/matthiasblomme/bobmodes

Publishing: everywhere (own blog + IBM Community), but Jan Willem reviews it first.

Check before publishing:
- Screenshots are the prototype with mocked sign-in ("Hi, Sam") and mocked text. The
  booth build may look different by the event. Retake closer to the date if it changed.
- Teaser: two screenshots only (start screen, top of a blueprint). The question screens
  and the Champions crop are in git history (commit 9471a95) if you want one back.
- The name wall is from your brief, not from the kickoff note. Tied to finishing the
  blueprint (intro only); unsure whether it's that or the full journey - reviewer check.
- "Runs in IBM Bob": skill fixes merged to public bobmodes main 2026-09-28
  (PR #11, merge 9f35809). Done.
- img_planner.png: copy of the planner post's img.png (your Tuesday, one pick per slot),
  so both posts show the same plan.
- Planner post link is relative (../techxchange-planner-skill/...), the house style for
  cross-post links. It resolves once this post moves to docs/posts/<slug>/; the planner
  post is on main at docs/posts/techxchange-planner-skill/ (PR #59). The IBM Community
  version needs the absolute URL instead.
- Community MCP mention (Higher Logic built it for this activation): check with Jan
  Willem / the IBM Community team that it can be named publicly before the event.
- The kickoff note says the blueprint also recommends booths. Neither the prototype nor
  the merged plan does, so booths are left out. Confirm with Jan Willem.
- "What you get" facts: Jan Willem's plan + merged plan (doc-kb my-knowledge,
  Conferences/2026_TechXchange/ChampionsWorkingGroup/), kickoff call recording note.
  Community action on the spot and the QR pass are planned behaviour; the prototype
  shows the post as a draft only.
-->

# Too many sessions? The IBM Champions built you a planner

For everybody going to TechXchange: congratulations. For those of you who aren't going: well, you're missing out. (To paraphrase, an old Flemish children's TV show.)

There's so much happening at the event that it's hard to build a proper agenda around what you like, what you want to see, and how much time you have at the venue. So you don't spend your first morning scrolling through 1137 sessions, the IBM Champions community built a blueprint helper for you.

It's an app you'll find at the IBM Community booth, where you can build your own TechXchange event blueprint. Based on your interests, when you're there, and what you want to do. Four questions, three minutes, and you have your personalized event plan. Finish it and your name goes up on the wall. Finish the whole booth journey and you earn a professional headshot and a giveaway.

## Where to find it

The IBM Community booth is in the Advocacy neighborhood of the Sandbox, diagonally across from the Champions Lounge. Look for a lab-style table with six laptops and a monitor next to it explaining what to do. That same monitor runs blogging workshops at set times, and those are in the session catalog.

It goes live when the Sandbox opens, Monday October 26 at 6 p.m.

The app is built with IBM Bob, by Jan Willem Steur, myself, and a group of testers who clicked through it more times than they'd like to admit. Champions building something for the rest of the community, which is more or less the point of being a Champion. It runs on OpenShift, and it talks to the IBM Community through a brand new Community MCP server. So when you join a group or post a question from the booth, that happens right there, under your own name.

Do you fancy helping to build the next thing like this? Then have a look at the IBM Champions program. What it is, and what it takes to get nominated, is on the [IBM Champions program overview](https://www.ibm.com/community/champions-program/). Writing about what you do, like this blog, is one way to get there.

![Start screen of the Growth Blueprint kiosk](img.png)

## What you get

Sign in with your IBMid, tell it what you're into, what you want out of the week and which days you're there. So instead of browsing the catalog, decoding topic groups and guessing who to meet, you get a plan:

- sessions worth your time, Champion-led sessions and AMAs first. Only on days you're there, nothing that's already over, and no two at the same time.
- IBM Champions to go talk to. Only the ones who opted in, so they're happy to meet you for a 1:1 in the Champions Lounge or the booth lounge. Send them a message in the TechXchange mobile app to set it up.
- IBM Community groups to join.
- what to do in the next 30 minutes.

Every pick comes with the reason it's on your list.

Before you leave the laptop, you do one thing in the community right there: join a group, post a question, or answer one. Then you get a QR code. It opens your blueprint on your phone, and it's your proof at the headshot station. The rest you'll see at the booth.

![A blueprint, fresh out of the kiosk](img_4.png)

The screenshots are from the prototype, so the version at the booth might look a bit different.

## What happens after your blueprint

The blueprint is one step of the IBM Community booth's Learn to Earn journey, built around this year's Build with Purpose theme:

1. Sign up for the IBM Community at the welcome desk.
2. Build your blueprint.
3. Add your ideas to the IBM Community wall, what you'd like to see in the community. There's a giant Jenga game in the same area, if you need a break.
4. Earn your professional headshot and the giveaway.

There's nothing to win, but you can earn. You walk away with a decent headshot for your LinkedIn profile, which, judging by some profiles, a lot of people could use.

## Can't wait?

If you want to start planning now, I have something for that too. It's a Bob skill that scrapes the TechXchange session catalog, works out what you care about, and builds a day-by-day plan with alternates. Re-run it when the schedule changes and it tells you which picks clash. It's in my public skills repo, folder [techxchange-planner](https://github.com/matthiasblomme/bobmodes/tree/main/bobmodes/techxchange-planner), and the whole story is in [Let Bob plan your TechXchange week](../techxchange-planner-skill/techxchange-planner-skill.md).

I used it for my own week. Two talks to give, the champion program on top, and more ACE and MQ sessions than I could ever attend. This is my Tuesday, as Bob planned it:

![My Tuesday, as Bob planned it](img_planner.png)

Drop the folder in `~/.bob/skills/`, open Bob, and ask:

```
Which sessions should I attend at TechXchange?
```

But it's a stripped-down version of what's waiting at the booth. The planner gives you sessions, and that's it. No Champions to meet, no groups to join, no headshot, no giveaway, and no name on the wall. And the first scrape takes about six minutes. Run it again later and it asks whether to reuse what it already has.

So use it to get a head start, and then come to the booth for the rest. Three minutes, and the kiosk does the scrolling for you.

And for those of you who aren't going:

> "When I get sad, I stop being sad and be awesome instead." - Barney, How I Met Your Mother

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#TechXchange \
\#Bob
