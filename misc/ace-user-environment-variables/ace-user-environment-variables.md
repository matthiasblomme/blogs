---
date: 2026-05-06
title: 'Environment variables straight into ACE node properties'
description: A short note on the [iib.user-...] placeholder, UserVariables, and why you almost never need a Compute node for this
reading_time: 4 min
tags:
- ace
- server.conf.yaml
- user-variables
- environment-variables
- configuration
---

<!--MD_POST_META:START-->
<div class="md-post-meta">
  <div class="md-post-meta-left">2026-05-06 · ⏱ 4 min</div>
  <div class="md-post-meta-right"><span class="post-share-label">Share:</span> <a class="post-share post-share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fmatthiasblomme.github.io%2Fblogs%2Fposts%2Face-user-environment-variables%2Face-user-environment-variables%2F" target="_blank" rel="noopener" title="Share on LinkedIn">[<span class="in">in</span>]</a></div>
</div>
<hr class="md-post-divider"/>
<div class="md-post-tags"><span class="md-tag">ace</span> <span class="md-tag">server.conf.yaml</span> <span class="md-tag">user-variables</span> <span class="md-tag">environment-variables</span> <span class="md-tag">configuration</span></div>
<!--MD_POST_META:END-->

# Environment variables straight into ACE node properties

If you ask around how to get an environment variable into a node property in ACE, the usual answer is some flavour of "drop a Compute node, call `System.getenv`, push it onto LocalEnvironment". That works. It is also more flow logic than the problem actually needs.

There is a much shorter path. It is documented, it has been there for years, and almost nobody I work with seems to know it.

## The placeholder

Open `server.conf.yaml` and add:

```yaml
UserVariables:
  encodedvar: 'someValue'
```

Restart the server. From that point on, anywhere a node property accepts the placeholder, you can write:

```
[iib.user-encodedvar]
```

Square brackets, the literal `iib.user-` prefix, the variable name. That is the syntax.

Here it is dropped into the **Match correlation ID** field on an MQInput node:

![mqinput-user-variable](img.png)

Yes, the toolkit shows a red "Invalid hexadecimal number" on that field. That is because the field is design-time validated as hex and the placeholder is a string. The runtime substitutes the value before the field is used, so the deployed flow gets the real hex from your variable. The error is cosmetic. Ignore it.

## Pulling from an actual environment variable

`UserVariables` are static by default. Add one line and they resolve from the process environment:

```yaml
UserVariables:
  encodedvar: '${ENCODED_VAR}'
resolveUserVariableEnvVars: true
```

Use `${VAR}` even on Windows. `%VAR%` does not work, do not bother.

This is the part that makes the pattern usable in containers. You set `ENCODED_VAR` wherever your platform sets env vars (Helm values, the operator CR, Docker run, whatever), and the integration server expands it into the UserVariable at startup. Your node property gets the value via the placeholder. No image rebuild, no BAR override, no flow change.

Version gates worth knowing: `${VAR}` substitution is ACE 12.0.4+, and the `[iib.user-...]` placeholder in node properties is 12.0.5+. Check before committing.

## And it is still a UDP

The same UserVariable is also exposed as a regular user-defined property. From ESQL:

```esql
DECLARE encodedvar EXTERNAL CHARACTER 'default';
SET OutputRoot.JSON.Data.value = encodedvar;
```

Same value reachable from JavaCompute (`getUserDefinedAttribute`), .NETCompute (`GetUserDefinedProperty`), and Mapping (`iib:getUserDefinedProperty(...)`).

If you specifically want a raw OS env var without going through `UserVariables`, the classic ESQL trick still works:

```esql
CREATE FUNCTION javaLangSystemGetenv(IN name CHARACTER)
  RETURNS CHARACTER
  LANGUAGE JAVA
  EXTERNAL NAME "java.lang.System.getenv";
```

Declare it once, call `javaLangSystemGetenv('MY_VAR')` from anywhere in your ESQL.

## Bootstrapping from a script

`server.conf.yaml` has a `StartupScripts` stanza too. A startup script can return YAML on stdout and the integration server reads it back:

```yaml
StartupScripts:
  FetchSecrets:
    command: '/opt/scripts/fetch-secrets.sh'
    readVariablesFromOutput: 'auto'
```

Where `fetch-secrets.sh` writes something like:

```yaml
---
UserVariables:
  encodedvar: 'value-from-vault'
EnvironmentVariables:
  DB_URL: 'jdbc:db2://prod:50000/MYDB'
```

That is your hook for vaults, mounted secret files, sidecars, anything you can express as "run a script, print YAML". The flow stays the same. The value just appears.

## Why I am writing this

Most teams I see reach for BAR overrides, policies, or a Compute node every time they need a configurable value in a property field. All three are valid. None of them match the intent of "make this property pick up an environment variable" the way `UserVariables` plus `[iib.user-...]` does.

The placeholder syntax is also genuinely buried. It does not show up where you would expect, and most blog posts on this topic stop at `System.getenv`. So if you have been writing one-line Compute nodes for this for years, you can stop.

---

*Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)*
