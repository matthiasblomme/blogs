---
title: 'Four questions, three minutes: your TechXchange blueprint'
date: 2026-09-28
author: Matthias Blomme
description: TODO - the IBM Champions are building a Growth Blueprint helper for the
  IBM Community booth at TechXchange 2026. What it does, where to find it, and a
  stripped-down version you can run now if you can't wait.
tags:
- techxchange
- ibm-champion
- ibm-community
- bob
- event
status: draft
---

<!--
TEMPLATE, not a draft. Your intro is kept as written; everything under it is
outline + verified filler for you to write out.

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
  booth build may look different by the event. Say "prototype" or retake closer to the date.
- img_5.png is the Champions section cropped to Jan Willem and you (Juan Martin cut off).
-->

# Four questions, three minutes: your TechXchange blueprint

For everybody going to TechXchange: congratulations. For those of you who aren't going: well, you're missing out. (To paraphrase Samson, an old Flemish children's TV show. Google it.)

> "When I get sad, I stop being sad and be awesome instead." - Barney, How I Met Your Mother

There's so much happening at the event that it's hard to build a proper agenda around what you like, what you want to see, and how much time you have at the venue. So you don't spend your first morning scrolling through a thousand sessions, the IBM Champions community is building a blueprint helper for you.

It's an app you'll find at the IBM Community booth, where you can build your own TechXchange blueprint based on your interests, when you're there, and what you want to do. Four questions, three minutes, and you have your personalized event plan. Finish it and your name goes up on the wall, and there's a headshot and a giveaway in it for you.

<!-- Credits (your answer): Jan Willem, you and the testers built it; frame it as the
Champions community working for the global community. Place it where it fits best,
probably "Where to find it" or the closing. -->

## Where to find it

<!--
Filler, verified from the kickoff:
- IBM Community booth, Advocacy neighborhood of the Sandbox, diagonally across from
  the Champions Lounge.
- Six laptops at one lab-style table, a monitor with instructions next to it.
- Goes live when the Sandbox opens: Monday October 26, 6:00 p.m.
- Built with IBM Bob ("attendee experience powered by Bob").
-->

![Start screen of the Growth Blueprint kiosk](img.png)

## Four questions, three minutes

<!--
Filler, from the prototype:
- Sign in with your IBMid through the IBM Community. Sign out at the end (booth staff
  help make sure you did).
- Q1 technology areas (match the conference tracks), Q2 IBM products (optional,
  searchable: MQ, App Connect, Bob, ...), Q3 what you want out of the event (pick up to
  two: grow skills, meet Champions, ...), Q4 which days you're there.
- It only recommends sessions on days you're around, and never one that already ended.
- No name or email stored; individual records are deleted 30 days after the event.
  (Prototype consent text - confirm it still reads like that on the day.)

Pick 2, maybe 3, of the screenshots below. "A couple of small screenshots."
-->

![Question 1: technology areas](img_1.png)

![Question 2: products, searching for App Connect](img_2.png)

![Question 3: what you want out of TechXchange](img_3.png)

## What you walk away with

<!--
Filler, from the prototype blueprint screen:
- Sessions to prioritise, per day, each with the reason it was picked.
- IBM Champions to connect with, matched on your interests, to set up a 1:1 in the
  Champions Lounge.
- IBM Community groups to join (topic groups, user groups).
- "Your next 30 minutes": first session, and where the lounge and ideas wall are.
- An optional first post in a group.
- A QR code and pass code to take along: show it at the headshot and giveaway station.
-->

![Blueprint: your focus and sessions to prioritise](img_4.png)

![Blueprint: IBM Champions to connect with](img_5.png)

*[screenshot placeholder: the pass / QR "Take it with you" block from the booth build (the local one shows a localhost URL)]*

*[photo placeholder: the booth itself, once it's set up - optional, for a post-event update]*

## What happens after your blueprint

<!--
Filler, verified from the kickoff. The blueprint is step 2 of 4:
1. Sign up for the IBM Community at the welcome desk.
2. Build your blueprint (this thing).
3. Add your ideas to the IBM Community wall. There's a giant Jenga game in the area too.
4. Earn your professional headshot and a giveaway.
Plus (your answer, not in the kickoff note): finish it and your name goes on a wall.
No leaderboard.
Keep this short, one paragraph or a 4-line list.
-->

## Can't wait?

<!--
Callout to the techxchange-planner skill. Facts (verified):
- Claude Code skill only, no Bob mode. In https://github.com/matthiasblomme/bobmodes
  under bobmodes/techxchange-planner; install = copy the folder to ~/.claude/skills/.
- Scrapes the session catalog through the RainFocus API behind the catalog page, plus
  the agenda and FAQ pages. Last scrape 2026-09-16: 1054 activities.
- Builds your interest profile from your AI chat history, a self-description, or
  guided questions.
- Makes a slot-budgeted agenda with ranked alternates; re-run it and it clash-checks
  your picks when times change.

The "stripped-down" angle, concretely - what the planner does NOT do that the booth does:
- no IBM Champions to meet, no Community groups, no first post
- no headshot, no giveaway, no pass
- you need Claude Code, and a bit of patience with a scraper
So: sessions only. For the rest, come to the booth.
-->

*[screenshot placeholder: planner skill output - a slice of the generated agenda note, your own picks blurred or a demo profile]*

## TODO closing line

<!-- One dry line. Something about coming by the booth anyway. -->

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#TechXchange
