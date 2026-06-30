---
date: 2026-06-30
title: Reporting IBM Champion activity with a custom Bob mode
description: A custom Bob mode (and Claude skill) that assembles your IBM Champion
  act-of-advocacy submission, builds a prefilled form URL, and stops you retyping your
  Champion ID four times a year.
tags:
- bob
- ibm-champion
- airtable
- claude
- automation
---

# Reporting IBM Champion activity with a custom Bob mode

The IBM Champion program wants you to report your acts of advocacy. Blog posts, talks, videos, ideas, code, the lot. Fair enough. The reporting happens on an Airtable form behind ibm.biz/champ-report, and every single time you start from zero: your Champion Program ID, your name, two email addresses, a product dropdown with a few hundred entries, a description with a word limit, a link, a date, and a consent box. You do this a handful of times a year, which is exactly often enough to resent it and not often enough to remember the fiddly parts.

So I put it in a mode.

Same repo as the support one: [github.com/matthiasblomme/bobmodes](https://github.com/matthiasblomme/bobmodes), public, so you can grab it too.

## What it actually does

You tell it what you did. It assembles the whole submission and hands you two things: a prefilled form URL, and a copy-paste sheet for the few fields the URL can't fill. It does not submit. The consent box is yours to tick, and the final click is yours to make.

The identity fields come from a private `.env` you fill in once:

```
CHAMPION_PROGRAM_ID=...
FIRST_NAME=...
LAST_NAME=...
PRIMARY_EMAIL=...
ALTERNATE_EMAIL=...
```

That file is gitignored. After that the mode never asks who you are again.

For the activity itself it walks through, one thing at a time:

- what you did, enough to write a description and pick the type
- the act-of-advocacy type, mapped to the exact dropdown entry
- the product(s) involved
- a link, which is effectively mandatory ("lack of link may result in disqualification", says the form)
- the date
- whether IBM may amplify it

Then it drafts the "Description of this Activity" for someone who wasn't there, keeps it under the 250-word limit, and tells you the word count. At the end you get the URL and the sheet.

## How it's wired

The mode folder is small:

```
ibm-champion-report/
├── .bobmodes                # the Bob mode definition
├── .env.sample              # copy to .env, fill once, stays private
└── references/
    └── form_fields.md       # the verified field spec: every field, every prefill param, the full option lists
```

The `.bobmodes` file is the part Bob reads: a slug, a name, when to trigger, which tools it gets, and the workflow.

```yaml
customModes:
  - slug: ibm-champion-report
    name: 🏅 IBM Champion Report
    description: >-
      Use this when reporting an IBM Champion act of advocacy: a blog, talk,
      video, idea, or code contribution on the activity report form...
    roleDefinition: >-
      You help report an IBM Champion act of advocacy. Identity comes from
      .env, never from chat. You build a prefilled URL plus a copy-paste sheet...
    whenToUse: >-
      Use this mode when the user wants to report or register an IBM Champion
      activity, or mentions ibm.biz/champ-report...
    groups:
      - read
      - - edit
        - fileRegex: (\.env(\.sample)?|references/.*\.md|\.md)$
          description: Read identity, read the field reference, write the field sheet
      - command
    customInstructions: >-
      Read references/form_fields.md first. Pull identity from .env. Gather the
      activity, draft the description under 250 words, build the prefilled URL
      and the sheet. Never tick consent, never submit.
```

The `groups` block keeps it on a short leash: it can read, run commands, and only write `.env`, the field reference, and the field sheet. It is not going to wander off and edit anything else while you report a blog post.

The real reference is `references/form_fields.md`. That is where the boring, exact knowledge lives: which field prefills by name, which only prefills by an internal ID, which can't be prefilled at all, the date format, and the full dropdown lists. Which brings me to the part that took the actual work.

## Getting the prefill to actually work

Airtable lets you prefill a form with query params. The documented way is `prefill_<Field Name>=value`. Simple. Except `<Field Name>` is the column name in the underlying table, not the label you see on the form. This form relabels things. So half the obvious params silently do nothing, and the form just shrugs and shows you an empty field.

I didn't want to guess, so I calibrated it against the live form, one field at a time.

The plain ones behaved. First name, Last name, Primary Email, Alternate Email all prefill by their label, because for those the label happens to match the column name underneath.

Then it got annoying. Champion Program ID, the one number you most want filled in so you stop copy-pasting it, does nothing by label. The real column name isn't exposed anywhere on the public form. The only thing that works is the internal field ID:

```
prefill_fldt6UIOXVxQBNSgl=20240660
```

The date field is the same story. Only the field ID works, and the format is `D/M/YYYY` with the leading zeros optional.

The link field is worse. No label works, no field ID is exposed, nothing prefills it. So the mode stops pretending and leaves it as a manual paste. A link is the one thing the form threatens to disqualify you for not having, and also the one thing you can't prefill. Make of that what you will.

Two more things the calibration turned up. Single-select values have to match an option exactly. "Write a Blog or Article", which is what I would have typed, is not an option. It's "Blog or Article", or "Blog on IBM property" if your blog sits on community.ibm.com. And the product list has 516 entries, none of which is "App Connect Enterprise". The closest is "IBM App Connect". You would never know without opening the dropdown and reading the whole thing, so the mode did that once and wrote all 516 down.

All of that lives in `form_fields.md` now, so the mode builds a URL out of params that actually land instead of ones that just look right.

## Getting it into Bob

Custom modes are imported per project. The repo ships a small PowerShell importer that scans a source path for `.bobmodes` files and merges them into a target project's `.bob/custom_modes.yaml`, skipping any mode already in there.

```powershell
git clone https://github.com/matthiasblomme/bobmodes.git
cd bobmodes
.\scripts\Import-BobModes.ps1 -SourcePath ".\bobmodes" -TargetProjectPath "D:\Projects\YourProject"
```

Reload the VS Code window (`Ctrl + Shift + P`, then `Reload Window`) and **🏅 IBM Champion Report** shows up in the dropdown with a `/ibm-champion-report` command. The same workflow also ships as a Claude Code skill if you work there instead.

![img.png](img.png)

![img_1.png](img_1.png)

## Using it

You describe the activity. Recently I reported an idea I had submitted on the IBM Ideas portal:

```
Log this idea I submitted on the IBM Ideas portal as an act of advocacy:
https://ideas.ibm.com/ideas/APPC-I-1249
```

It pulled my identity from `.env`, set the type to Ideas portal, the product to IBM App Connect, drafted a description under the word limit, and handed back a URL that fills eight fields the moment you open it: the ID, name, both emails, the activity type, the product, and the date. Then a short sheet for the four it can't prefill: the description to paste, the link, the amplify box, and the consent.

![img_2.png](img_2.png)

You open the URL, paste the description and link, tick what you mean to tick, and submit. The retyping is gone. What's left is the part that actually needs a human: deciding the thing is worth reporting, and agreeing to the privacy terms.

## Wrap up

It's in the same repo as the support mode, importable with the same script. The form didn't get less fiddly, I just stopped doing the fiddly parts by hand. And I now know more about Airtable's prefill internals than I ever wanted to, which is apparently what it takes to not retype a Champion ID four times a year.

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#Bob
