---
date: 2026-04-19
title: 'Migrating ACE to v13'
description: A walkthrough of an ACE v13 migration, from Transformation Advisor through Java 17 cleanup to what actually breaks once you flip the switch.
tags:
- ace
- migration
---

<!--MD_POST_META:START-->

<!--MD_POST_META:END-->

# Migrating ACE to v13

ACE v13 is the first release where Java 17 is the default, and that one fact drives most of the work you'll be doing during a migration. The rest is cleanup around it: old policies, old libraries, old assumptions about how your integration servers are laid out.

This is a walkthrough of the steps that actually matter. Neutral first, personal second.

## Run Transformation Advisor

Transformation Advisor (TAD) scans an exported workspace and lists the issues it finds against a specific target version. Run it against the fix pack you actually intend to install.

If a new fix pack drops mid-migration, run it again. TAD's rules change between fix packs, and the same workspace can give a different verdict on a newer target. WS-Security is the clearest example. Scanned against 13.0.6 it is listed as a hard Java 17 blocker. Scanned against 13.0.7 it is supported with UsernameToken and X509, but not yet with Kerberos, LTPA, or SAML. Same code, different answer.

This happened to me. 13.0.7 came out while I was already working through findings from the 13.0.6 scan, and half of what had been planned as Java 8 holdovers quietly turned into Java 17 candidates. Worth the second run.

So pick the highest fix pack you're willing to target, and scan against that. Scan against an older one and you might be planning work you don't need to do.

One more thing. TAD tends to inflate numbers. If a shared library imports a WS-Security dependency, every flow that pulls in that library shows up as a hit. A raw count of "over a hundred WS-Security occurrences" can collapse to one real usage once you trace it. Verify every critical finding by hand before you plan work around it.

## Check your Java code for 17

If you have Java Compute nodes or shared Java projects, they need to compile and run under a Java 17 runtime. ACE shipt with both a java 17 and a java 8 runtime, so you don't have to worry about bringing your own.

The failure modes are well known and the list is short.

- `javax.xml.bind.*` is gone. Add `jakarta.xml.bind-api` and `jaxb-runtime` (4.x) as jars, update imports to `jakarta.xml.bind.*`.
- `javax.xml.bind.DatatypeConverter` is gone. Replace with `java.time` equivalents. `ZonedDateTime.now().format(DateTimeFormatter.ISO_OFFSET_DATE_TIME)` is the usual drop-in.
- JNA needs a recent version if you talk to Windows credentials or any platform API. Versions from a few years ago will not behave on Java 17. Bump to something current.
- Third-party libraries: JSoup, Jackson, Auth0 JWT, PDFBox. The old ones either fail to run or throw reflective access warnings. Update them once, test once.
- Every `.classpath` referencing `JavaSE-1.8` has to become `JavaSE-17`.

None of this is dramatic, but there is a lot of it if you have more than a handful of Java projects. Track it per project, not per issue, so you can tell what's done. And if you are updating java projects, why not look at the code and see if you can modernize it a bit more? Never miss out on diminishing technical debt.

Worth mentioning here: [IBM Bob](https://bob.ibm.com/) treats Java as a first-class citizen and has modes aimed squarely at modernization work. Point it at your Java projects and let it do the first pass: it flags the usual suspects, produces a per-project tracker, and gets you to a short list of things that actually need a human. Not perfect, but a lot faster than grepping for `javax.xml.bind` across twenty workspaces.

## When you need to keep a server on Java 8

Some things still require Java 8 even on 13.0.7:

- WS-Security with Kerberos, LTPA, or SAML tokens.
- Any library with a native dependency you can't yet modernize.

For those cases, pin the integration server to Java 8 and let the rest of the node run Java 17. You do that with `ibmint specify jre`:

```
ibmint specify jre --version 8 --integration-node <nodeName> --integration-server <serverName>
```

Or for an independent IS:

```
ibmint specify jre --version 8 --work-directory <directory>
```

The command writes a `server.java.yaml` next to the server config, with contents like:

```yaml
---
 javaVersion: 8
 aceVersion: 13.0.6.0
```

The change takes effect the next time the server starts. To go back to the shipped default, run the same command with `--default`. Document which server runs which JVM. You will forget otherwise.

Java 8 is a holding position, not an endpoint. Every server still on Java 8 after the migration needs a follow-up ticket with an actual plan.

One thing TAD will flag that is not actually a blocker: `SSL_` prefix cipher names. The JSSE provider maps `SSL_*` and `TLS_*` names to the same underlying cipher suites, so it's more a cosmetic issue than a real one. Rename them to `TLS_` when you're in the file anyway, but don't pin a server to Java 8 over it.

## Rework WS-Security policies for Java 17

Sounds scarier than it is. Create a new policy under Java 17 and point the flow at it. Done.

WS-Security with UsernameToken and X509 is compatible with Java 17 from 13.0.7 onwards. The old WebSphere-era policies you have lying around reference callback handlers like `com.ibm.websphere.wssecurity.callbackhandler.*` which don't exist in the ACE Java 17 runtime, so reusing them verbatim will fail. Easier to just recreate: new policy, correct classnames, swap the reference in the node. No surgery on the old file, no guessing which bits carry over.

If you do want to edit an existing binding instead, the pattern is straightforward: any class starting with `com.ibm.websphere.*` or `com.ibm.ws.*` needs the ACE-native equivalent. But for anything beyond a one-off, the new-policy route is faster.

## Where you're coming from matters

Before you pick a style, check where you're starting. The jump to v13 is very different depending on which version you're on today, and the steps stack. Each older version adds its own work on top of everything the newer ones already had to do.

**ACE 12 to 13.** The easy one. Same artifact model, same concepts, `ibmint extract node` and `ibmint extract server` work directly. Most of the work is the Java 17 cleanup above, not the migration itself. This is the baseline. Everything below adds to it.

**ACE 11 to 13.** Everything from the v12 path, plus a slightly larger delta in defaults and runtime behaviour to validate. Applications, libraries, and policies already look the way v13 expects them, so the artifacts come across cleanly via `ibmint extract`.

**IIB 10 to 13.** Everything from the v11 path, plus the jump from configurable services to policies. `ibmint extract node --overwrite-existing` works for in-place, or you can extract into a fresh install. The tooling handles most of the rewrite, but watch out: same as the v10 to v12 path, the generated policies end up node-wide, not scoped to the server that actually needs them. Functionally fine, messy in practice. Plan time to split them up and move each policy onto the server that uses it.

**IIB 8 or 9 to 13.** Everything from the v10 path, plus the part where you don't really migrate, you rebuild. v8/v9 predate applications, libraries, and policies as first-class concepts. Configurable services, deployment topology, even the way additional flow instances start up, all of that has shifted under you. Direct migration from v8 is not supported, and even v9 is painful enough that the realistic path is: stand up a fresh v13 environment, create a new repo, and move services across one by one. ESQL carries over well, most of the pain is structural. Treat it as an opportunity to clean up, not as an upgrade.

If you're on v8 or v9 and someone is pitching you "automated migration", be suspicious. There is no tool that turns fifteen years of configurable services and monolithic integrations into a clean v13 layout without a human reading the code.

## Pick a migration style

IBM documents three ways to move to v13. Same target, different paths.

**In-place migration.** Migrate the integration node on the same machine, keeping the same name. Run `ibmint extract node --overwrite-existing` and the old node is replaced by a v13 node in the same spot. Clients don't need reconfiguring. The downside is obvious: the node is down while it happens, and if anything goes sideways, your rollback story is "restore from backup".

**Parallel migration.** Stand up a new v13 integration node next to the old one and move application logic across at your own pace. Both run side by side until you're happy. Safer, but you need the hardware or VM to host the parallel environment, and you have to manage two nodes for the duration.

**Extract migration.** Use `ibmint extract node` or `ibmint extract server` to pull configuration and resources out as files. Those files then get redeployed into a fresh v13 environment, usually as independent Integration Servers. It is the flexible option: the same command works whether you're doing an in-place swap, a parallel migration, or splitting a node-owned setup into independent servers.

The first two answer the question "where does the new one live". Extract answers "how do I get the config out in a form I can actually work with". That difference is the reason I went with extract.

## Why I picked extract

`ibmint extract node` pulls a node's configuration out into files you can version, review, and redeploy into v13. It is the cleanest way to move, and it is the recommended path if you're going from node-managed to Integration Server.

Run it, then read the output. All of it. It will tell you what was extracted, what was skipped, and which parts of your node did not map cleanly.

What `extract` does not bring along:

- Keystores and truststores
- Shared-classes jars
- ODBC configuration (`odbc.ini`, `odbcinst.ini`)
- Environment-specific scripts and cron jobs

Copy those over manually. If you forget, the server starts, looks healthy, and then fails the first time a flow tries to open a secure connection or load a driver.

## Controlled starts

Once v13 is installed and the extract is in place, do not start everything at once.

Deploy with flows stopped. Confirm the server comes up clean: JVM version reported correctly, logs free of class loading errors, policies visible. Then start flows in groups. Start the ones with external calls last, so you can catch TLS and cipher issues against a known-good baseline.

If a flow fails on start, the earlier groups are still clean and you can troubleshoot in isolation. If you start everything together, you get a log full of noise and no idea which flow is the real problem.

## Test, then test again

Baseline before. Compare after. The obvious ones:

- WS-Security authentication end-to-end. Send a real SOAP request, inspect the security header, confirm the downstream service accepts it.
- JSON parser defaults changed. `numberPrecisionType` is now `decimal`, `allowScientificNotation` is now `false`. If a downstream consumer expects a double or scientific notation, you will find out the hard way.
- TLS negotiation against every external endpoint. TLS 1.2 minimum. Confirm cipher suites still match on both sides.
- Credential stores if you use JNA. Test on the actual OS version, not a laptop.
- GC behaviour. G1 is still the default, but the numbers will not be identical. Baseline pause times and heap usage before you switch.

Load testing matters more than people admit. Java 17 tends to run hotter on startup and colder at steady state than Java 8. A ten-minute smoke test tells you nothing about how a flow behaves after two hours under load.

## Decide on the vault

If you haven't moved to the ACE vault yet, v13 is a reasonable forcing function. Credentials stored the old way still work, but every time you touch a policy binding or a security profile in this migration, you're already half-configuring the thing. Do it once, properly.

If you're already on the vault, nothing to do here.

## Node-managed to Integration Server (or containers)

v13 leans hard toward Integration Server topology. Node-managed setups still work, but the direction of travel is clear: independent servers, configuration in yaml, policies extracted as files, credentials in the vault. That pattern ports to containers without rework.

If you're staying node-managed for now, fine, but write down why, so the next person can revisit the decision.

## What I actually ran into

Now the personal chapter. Same migration, different tone.

The first surprise was how many TAD findings turned out to be shared-library echoes. A single real WS-Security usage produced a hundred warnings because the WS-Security-aware library was imported everywhere. The raw number is genuinely alarming until you trace it and realise almost all of it is the same single usage, reported a hundred times.

The second surprise was how much `ibmint extract` skips silently. It logs the skips, but if you're not reading the whole output you'll miss them. Keystores were the obvious one. Shared-classes jars were the one that actually caught me out, because the server started fine without them and failed only when the first flow needed them.

The third surprise was how small the Java 17 code work turned out to be in practice. Most projects were fine. The ones that broke, broke hard, but the list was short: one project heavy on JAXB, one using `DatatypeConverter`, one pulling in an old JNA. Everything else compiled with a classpath bump and a rebuild. That was not what I expected going in.

The last one was less of a surprise and more of a confirmation. The WS-Security policy fix is one line in one XML file. One classname, swapped. That's all. Once I knew which line, every other policy fell into place in minutes. Before I knew, I spent most of a day reading IBM announcements and trying to work out whether this was supposed to work at all.

## What I'd tell someone starting now

Run TAD against the latest fix pack you're willing to target, not the one you happen to have installed. Verify every critical finding by hand before you plan work around it. Know up front what `extract` does not bring along, and copy those things yourself. Start flows in groups, not all at once. Test WS-Security end-to-end, not just "did the server come up". Document every server that stays on Java 8, along with its exit plan.

Everything else is cleanup around those five.

## A short checklist

Not the full one, just the parts you'll kick yourself for skipping:

- [ ] Run Transformation Advisor against the target fix pack, not whichever one is installed.
- [ ] Verify every critical TAD finding against the actual code or config before planning work.
- [ ] Inventory Java projects, line up JAXB, `DatatypeConverter`, JNA, and library updates.
- [ ] Decide which servers need to stay on Java 8, and pin them with `ibmint specify jre --version 8`.
- [ ] Back up the source node and config before anything else.
- [ ] Pick the migration style that matches your source version and your appetite for risk.
- [ ] Copy keystores, shared-classes jars, ODBC files, and environment scripts by hand. `extract` won't.
- [ ] For WS-Security, create a new policy on v13 rather than porting the old binding.
- [ ] Deploy with flows stopped, confirm the server is clean, then start flows in groups.
- [ ] Test WS-Security end-to-end, JSON parser behaviour, and TLS against real endpoints.
- [ ] Document every Java 8 holdover with a name, an owner, and a date for retiring it.

---

# References

- [Running the Transformation Advisor tool](https://www.ibm.com/docs/en/app-connect/13.0.x?topic=tasks-running-transformation-advisor-tool)
- [Migrating to IBM App Connect Enterprise 13.0](https://www.ibm.com/docs/en/app-connect/13.0.x?topic=migrating-app-connect-enterprise-130)
- [Seamlessly migrate to IBM App Connect Enterprise 13](https://www.youtube.com/watch?v=rk6vLCNraY0)
- 

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#AppConnectEnterprise(ACE)