---
date: 2026-07-31
title: 'Retrieving IIB v10 resources when the BAR file is gone'
description: You cannot retrieve a deployed BAR file on IIB 10, BAR regeneration only
  exists in ACE. But you probably do not need it. The flow is still on the broker in a
  readable XML format, ESQL included, and there is a supported route to get it back into
  a toolkit. Tested on 10.0.0.26 and ACE 13.0.7.2.
tags:
- iib
- iib10
- ace
- migration
- bar-file
- dfmxml
- esql
- recovery
status: draft
---

# Retrieving IIB v10 resources when the BAR file is gone

This one comes up regularly. A project is deployed on IIB 10, the BAR file has been misplaced, nobody put the source in version control, and now there is a bug that needs fixing. Can you pull the deployed BAR back off the server?

You cannot retrieve the BAR file itself on IIB 10. BAR regeneration only exists in ACE, toolkit 12.0.9 and web UI 12.0.11.

The good part is that you probably do not need it. The BAR is not what you are after, the flow is, and the flow is still on the broker in a readable XML format, just not as a .msgflow.

## Where everything sits

Every deployed artifact sits in this folder structure:

```
<MQSI_WORKPATH>\components\<broker>\<egUUID>\config\<appUUID>\**
```

With the message flows here:

```
<MQSI_WORKPATH>\components\<broker>\<egUUID>\config\<appUUID>\FLOWS\<flowUUID>\dataFlowManager.xml
```

`MQSI_WORKPATH` is `C:\ProgramData\IBM\MQSI` on Windows and `/var/mqsi` on Unix.

<<insert screenshot>>

If you open that file in a text editor, you get the full message flow content. Every node, every property, every connection.

```xml
<Definition><MessageFlow uuid="2a066358-a0ce-4b33-955d-687ecf7bb6f8" label="httpTest"
 additionalInstances="0" commitCount="1" coordinatedTransaction="no"
 deployInfo="PGRlcGxveUluZm8gdmVyc2lvbj0iMSI+…">
  <ComIbmWSInputNode uuid="httpTest#FCMComposite_1_1" label="HTTP Input"
                     URLSpecifier="/test" timeoutForClient="180">
    <OutputTerminal uuid="timeout"/>
  </ComIbmWSInputNode>
  <ComIbmWSReplyNode uuid="httpTest#FCMComposite_1_2" label="HTTP Reply"
                     timeoutForReply="120"/>
  <Connection sourceNode="httpTest#FCMComposite_1_1" sourceTerminal="out"
              targetNode="httpTest#FCMComposite_1_2" targetTerminal="in"/>
</MessageFlow><Supplement deployedAsSource="true"/></Definition>
```

I checked this on 10.0.0.26 by deploying the same application twice, once as source and once with compile and in-line, and searching the whole work path. Both give the same result. There is no .cmf on the broker at all, in either case. That file only exists inside the BAR itself, the broker unpacks it on deploy.

<<insert screenshot>>

## A rename does not get you a .msgflow

You might be tempted to think that a simple rename of the file would work. It does not.

A dataFlowManager.xml is a runtime file, not a toolkit file. The root element is `Definition` and the node type is the element name itself, `ComIbmWSInputNode`. A .msgflow is Eclipse EMF, the root element is `ecore:EPackage` and nodes are generic `<nodes xmi:type="ComIbmWSInput.msgnode:FCMComposite_1">` entries.

They share no element names at all, even when they describe the same flow.

The clearest example is canvas location. A .msgflow carries `location="189,89"` on every node, because the toolkit needs to know where to draw them. The runtime has no use for that, so dataFlowManager.xml does not have it. Which is also exactly why IBM documents "node positions are regenerated" as a conversion loss. The information simply is not there.

## The ESQL

ESQL files are plain readable as well, in `..\config\<appUUID>\ESQL\`, if you deployed without compile-and-inline.

If you deployed with compile-and-inline, the ESQL becomes part of the dataFlowManager.xml, in the `computeExpression` attribute of the compute node. You can recover it from there, it is readable text, comments and indentation included, but that is an extra step for you to do.

<<insert screenshot>>

I tested that by putting a unique string in an ESQL comment and grepping the whole work path for it after deploying the compiled BAR. It was there.

## Two things to watch out for

1. The execution group labels are recorded as `ExecGroupLabel` in `<MQSI_WORKPATH>\components\<broker>\repository\brokeraaeg.dat`, but encoded in base64. Example: `SVMx` is not an EG called SVMx, it decodes to `IS1`.
2. An XML parser cannot help you pulling ESQL out of a compiled dataFlowManager.xml. Attribute-value normalisation replaces the newlines with spaces, and then every `--` comment silently comments out the rest of your module. Use a normal text editor, like Notepad++.

## Do not do this on a running node

All of the above is poking around in your runtime, which is not always a good idea. Especially not if you are not familiar with it.

The better route is to start with `mqsibackupbroker` and work from the backup rather than from the running node. IBM documents that a backup includes your deployed resources, so nothing is lost by doing it that way.

On v10:

```
mqsibackupbroker TESTNODE_Matthias -d c:\temp\ -a backupBroker.zip
BIP1252I: Creating backup file 'c:\temp\backupBroker.zip' for integration node 'TESTNODE_Matthias'.
BIP8071I: Successful command completion.
```

Then on v13, `ibmint extract node` reads that v10 backup directly:

```
ibmint extract node --backup-file c:\temp\backupBroker.zip --input-integration-node TESTNODE_Matthias --output-integration-node TESTNODE_13_Matthias
BIP8469I: Version '10.0' backup file supplied.
BIP8471I: Loading configuration for source integration node 'TESTNODE_Matthias'.
BIP8389W: Property 'sslProtocol' for the node wide httplistener 'HTTPSConnector' is no longer available. The property was configured with value 'TLS', which was not the default.
BIP8470I: Loading configuration for integration server 'EG_CMF'.
BIP8470I: Loading configuration for integration server 'EG_SRC'.
BIP8470I: Loading configuration for integration server 'default'.
BIP8473I: Creating target integration node 'TESTNODE_13_Matthias'.
BIP15288W: Component 'JVM' is not required by the current contents of this integration server;  therefore the Java specification will have no effect.
```

This will start your applications, unless there are unsupported features in your flows.

<<insert screenshot>>

In my case the flows did not start, but that was because they use HTTP ports that were already in use by the v10 node still running next to it. Worth checking that before you conclude something is unsupported.

One thing to know about this command: it will not overwrite an existing target node. It fails with `BIP8087E: <node> already exists and cannot be created`, and it does that *after* printing all the "Loading configuration for integration server" lines. So a failed run looks a lot like a successful one if you only read the top half. Drop or rename the target node before you re-run.

## Retrieving the resources in the toolkit

The next step is retrieving the resources via the toolkit. Right click the integration server or the application in the Integration Explorer view and pick retrieve source artefacts.

<<insert screenshot>>

This should give you your entire flow, with the ESQL separated back out into modules. The generated flow even tells you where it came from, there is a note on the canvas saying it was generated from the .dfmxml.

You need 12.0.9 or later for this. There is no v10 equivalent, and this is the one step you cannot work around, because something has to translate the runtime format into the toolkit format.

## What about overridden properties

This is the part I was least sure about, so I tested it.

BAR overrides do reach the runtime. `mqsiapplybaroverride` writes into `<app>.appzip/META-INF/broker.xml` inside the BAR, the broker applies it during deploy, and then drops it. There is no broker.xml anywhere in the v10 work path. What lands on disk in dataFlowManager.xml is the effective value, after the override.

I checked it by overriding a URLSpecifier and deploying to a separate integration server:

```
flow=recoveryTest   URLSpecifier=/OVERRIDDEN_VALUE     <- EG_OVR
flow=recoveryTest   URLSpecifier=/recoverytest         <- EG_SRC
flow=recoveryTest   URLSpecifier=/recoverytest         <- EG_CMF
```

So you do not need the BAR's broker.xml to recover your properties. What you cannot get out of it is which values were overridden and which were original, you only see the merged result. If you need that split, for example to rebuild an override file for another environment, get it from the v10 web UI or `mqsireportproperties`.

The broker.xml you do see in a v13 extract is a different file. It holds `deployBarfile`, `deployTimestamp` and `migratedDeployTimestamp`, so migration provenance, not property overrides.

What I have not confirmed is whether an override survives the last hop, the toolkit converting the .dfmxml into a .msgflow. That conversion is a real transformation, so it could drop things. If you want to test that yourself, pick a property on a less obvious tab, something like maximum client wait time on the error handling tab, rather than one on the basic tab.

## Java does not come back

Only the compiled jar ever reaches the broker. Java source never leaves the build machine, IBM even tracked .java files leaking into BAR files as a defect at some point. ACE re-imports the jar so the project builds, but if there is a JavaCompute node in that flow, you are out of luck.

Worth saying that out loud early, before someone assumes it is included in the good news.

## And skip cmf2msgflow

It comes up every time this question is asked on the forums. It is an abandoned community tool, people report the executable does not even run, and IBM pushed back on distributing unverifiable binaries at the time.

The retrieve source artefacts feature is the supported version of that idea, and for this kind of recovery you do not need either.

So no, you cannot get your BAR file back. But between the runtime XML, the backup, and one toolkit that is a few versions newer than the one you lost the source on, you can get pretty much everything that was in it.
