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
---

<!--
First draft. Intro is yours (with the blog-buddy fixes); the sections below it are
written from verified notes, so check tone and cut what you don't want.

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
- The name wall is from you, not from the kickoff note.
- "Runs in IBM Bob" depends on the skill fixes that were uncommitted in D:/GIT/bob_modes
  and D:/GIT/bobmodes on 2026-09-28 (times[] docs, reuse prompt, README "Claude Code
  only" lines). Push the public repo before this goes out.
- img_planner.png: Thursday table from the fixed skill's Bob run
  (D:/tmp/txc-planner-bob-v2, plain-attendee profile, 19:39), all times checked against
  that run's sessions_raw.json.
- Links to misc/techxchange-planner-skill (untracked, not on this branch). Publish the
  planner post first or together, or the link 404s.
-->

# Too many sessions? The IBM Champions built you a planner

For everybody going to TechXchange: congratulations. For those of you who aren't going: well, you're missing out. (To paraphrase Samson, an old Flemish children's TV show. Google it.)

There's so much happening at the event that it's hard to build a proper agenda around what you like, what you want to see, and how much time you have at the venue. So you don't spend your first morning scrolling through a thousand sessions, the IBM Champions community built a blueprint helper for you.

It's an app you'll find at the IBM Community booth, where you can build your own TechXchange blueprint based on your interests, when you're there, and what you want to do. Four questions, three minutes, and you have your personalized event plan. Finish it and your name goes up on the wall, and there's a headshot and a giveaway in it for you.

## Where to find it

The IBM Community booth is in the Advocacy neighborhood of the Sandbox, diagonally across from the Champions Lounge. Look for a lab-style table with six laptops and a monitor next to it explaining what to do.

It goes live when the Sandbox opens, Monday October 26 at 6 p.m.

The app is built with IBM Bob, by Jan Willem Steur, myself, and a group of testers who clicked through it more times than they'd like to admit. Champions building something for the rest of the community, which is more or less the point of being a Champion.

![Start screen of the Growth Blueprint kiosk](img.png)

## What you get

Sign in with your IBMid, tell it what you're into, what you want out of the week and which days you're there. What comes out is a blueprint with the sessions worth your time, IBM Champions to go talk to, and community groups to join. Every pick comes with the reason it's on your list.

You can take it with you on your phone. The rest you'll see at the booth.

![A blueprint, fresh out of the kiosk](img_4.png)

The screenshots are from the prototype, so the version at the booth might look a bit different.

## What happens after your blueprint

The blueprint is one step of the IBM Community booth's Learn to Earn journey:

1. Sign up for the IBM Community at the welcome desk.
2. Build your blueprint.
3. Add your ideas to the IBM Community wall, what you'd like to see in the community. There's a giant Jenga game in the same area, if you need a break.
4. Get your professional headshot and a giveaway.

That's also how your name ends up on the wall. And you walk away with a decent headshot for your LinkedIn profile, which, judging by some profiles, a lot of people could use.

*[photo placeholder: the booth itself, once it's set up - optional, for a post-event update]*

## Can't wait?

If you want to start planning now, I have something for that too. Back in August I wrote a skill that scrapes the TechXchange session catalog, works out what you care about, and builds a day-by-day plan with alternates. Re-run it when the schedule changes and it tells you which picks clash. It's in my public skills repo, folder [techxchange-planner](https://github.com/matthiasblomme/bobmodes/tree/main/bobmodes/techxchange-planner), and the whole story is in [Planning TechXchange from the session catalog API](../techxchange-planner-skill/techxchange-planner-skill.md).

It runs in IBM Bob and in Claude Code. Drop the folder in `~/.bob/skills/` or `~/.claude/skills/`, start a new session, and ask:

```
Which sessions should I attend?
```

But it's a stripped-down version of what's waiting at the booth. The planner gives you sessions, and that's it. No Champions to meet, no groups to join, no headshot, no giveaway, and no name on the wall. And the first scrape takes a while. Run it again later and it asks whether to reuse what it already has.

![One day of a planner agenda, with the clashes and alternates](img_planner.png)

So use it to get a head start, and then come to the booth for the rest. Three minutes, and the kiosk does the scrolling for you.

And for those of you who aren't going:

> "When I get sad, I stop being sad and be awesome instead." - Barney, How I Met Your Mother

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#TechXchange
