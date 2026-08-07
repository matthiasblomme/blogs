# Short discussion post / thread reply

---

Short answer: you cannot retrieve the BAR file itself on IIB 10. BAR regeneration only exists in ACE, Toolkit 12.0.9 and web UI 12.0.11, and it does not backport.

The good part is that you probably do not need it. The BAR is not what you are after, the flow is, and the flow is still on the broker in readable XML.

Every deployed flow lives here, regardless of how the BAR was built:

```
<MQSI_WORKPATH>\components\<broker>\<egUUID>\config\<appUUID>\FLOWS\<flowUUID>\dataFlowManager.xml
```

Open it in a text editor and you get the full flow: every node, every property, every connection. There is no `.cmf` on the broker at all, that only exists inside the BAR file itself. I checked this on 10.0.0.26 by deploying the same application twice, once as source and once with compile and in-line, and searching the whole work path. No `.cmf` either time.

ESQL comes back too. Deployed as source it sits in `config\<appUUID>\ESQL\` as a plain `.esql`. Built with compile and in-line it is inside the flow, in the `computeExpression` attribute of the compute node, verbatim, comments included.

Tyron is right that you should start with `mqsibackupbroker` and work from the backup rather than poking at the running node. IBM documents that backup as including the deployed resources, so nothing is lost by doing it that way.

Two things that will cost you time if nobody warns you:

- `ExecGroupLabel` in `brokeraaeg.dat` is base64. `SVMx` is not an EG called SVMx, it decodes to `IS1`.
- Do not load `dataFlowManager.xml` with an XML parser to pull the ESQL out. Attribute-value normalisation turns the newlines into spaces, and then every `--` comment silently comments out the rest of the module.

To get from there to an editable `.msgflow` you do need an ACE 12.0.9 or later Toolkit: rename the file to `<flowname>.msgflow.dfmxml` and use Retrieve source artefacts. Worth knowing that `mqsiextractcomponents` produces a file byte for byte identical to `dataFlowManager.xml`, so for recovery you can skip the migration and just copy the file across.

One thing genuinely does not come back: Java. Only the compiled jar ever reaches the broker, so if there is a JavaCompute node in there, set expectations early.

I wrote the full procedure up with the details and the gotchas here: [link]
