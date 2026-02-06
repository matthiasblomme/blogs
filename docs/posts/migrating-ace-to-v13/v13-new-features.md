---
date: 2026-01-16
title: ACE v13 new features (when coming from v12)
image: cover.png
description: A summary of all the new features for ACE v13 up to 13.0.6.0

---

![cover](cover.png){ .md-banner }

# ACE v13 new features (when coming from v12)

> **DISCLAIMER:**
> All the information below is provided by IBM and digested/interpreted by me. It's meant to help and inform but should
> in no way be interpreted as ...

## Why I'm doing this

[Ben Thompson](https://community.ibm.com/community/user/people/ben-thompson1) does a splendid job in clearly and cleanly
explaining all the new ACE features for each release. However, sometimes it's handy to have them all in one overview, 
grouped by main product features.

That is exactly what I'm going to do here: list all changes (and group similar ones) for anyone looking to migrate from
v12 and in need of a simple overview. I was looking into everything that changed regarding ACE v12, so it's 2 birds with one stone.

I'll try not to go into too much detail on all the topics, the main focus is to give you a straight overview. So make sure
to have a look at the referenced material as well. I'll put all of Ben's posts in there, along with some other ones that I
found interesting and that are relevant, in one way or another

With each new release, I'll try to keep this page up to date, but no promises on the time line. Feel free to reach out if
it takes too long ;)

It's sometimes difficult to place certain topics in one category as they span multiple product features, but I just choose
what felt right to me. Feel free to disagree, as long as you continue reading this blog.

## The features

### Release cycle

This is not really a feature, but since I'm bundling information, I might tackle this one as well.

General availability: 27 September 2024
Support cycle: 5+1+3
- 5 years of standard support
- 1 year of extended support for new defects
- 3 years of extended support for usage and known defects
  End of support: 2029
  End of extended support: 2033

### Product editions

There is a slight change in the name of the product versions. The below table gives a clear overview.
![img.png](img.png)

If you haven't used ACE before and/or if you have no paid entitlements, you can start with the free [Developer edition](https://www.ibm.com/resources/mrs/assets?source=swg-wmbfd).
(You will need to register for an IBM account).

| Tool            | Where it lives             | Context awareness                | Primary strength                        | Key limitation in enterprise setups |
|-----------------|----------------------------|----------------------------------|-----------------------------------------|-------------------------------------|
| Claude Code     | External chat / web / IDE  | Limited to provided context      | Strong reasoning and explanations       | No native repo or IDE grounding     |
| GitHub Copilot  | IDE (VS Code, JetBrains)   | File-level and limited repo view | Fast code completion and suggestions    | Weak at cross-cutting reasoning     |
| Antigravity     | Separate tool/environment  | Depends on ingestion setup       | Deep analysis and transformations       | Steep learning curve, context shift |
| IBM Project BOB | VS Code                    | Repo, code, config, intent       | Context-aware collaboration in-place    | Early-stage, access still gated     |

### Designer

The APP Connect Enterprise Designer is a new, low threshold, alternative tool for flow authoring.  It's not as feature
rich as the toolkit (still the strategic IDE for ACE), but it aligns more with Cloud Development Platforms. I was already
a part of the iPaaS offering of ACE, but with v13, it has been added to your local installation as well.

The most common use case is to start a Connector development project in the Designer and switch over to the toolkit for
the more detailed work.

#### Templates

The Designer also comes with its own set of templates.

![img_6.png](img_6.png)

#### Kafka nodes

Kafka input and output nodes can be used directly from the Designer.

#### Patterns

Aside from the well-known Tutorials Gallery that has been around for many years, ACE v13 comes with a new restyled
Patterns Gallery. Patterns are helpful because they:

- Generate customized solutions to a recurring integration problem in an efficient way
- Encourage adoption of preferred techniques in message flow design
- Help guide developers who are new to the product
- Provide consistency in the generated resources

They offer you a quick start based on a couple of choices, without the fixed set of resources and instructions that a
tutorial offers.

Currently, there are roughly 100 available patterns (and no, I did not count them by hand) categorized in 6 topics:
- Protocol Transformation Patterns
- Format Transformation Patterns
- AI Patterns
- Enterprise Integration Patterns
- Scatter-Gather Patterns
- Messaging Patterns

Some patterns (about 17) are marked "coming soon!" (in 13.0.6.0), so keep your eyes peeled.

##### RAG Pattern

The RAG pattern is the first addition to the AI Patterns category.

![img_33.png](img_33.png)


#### AI Mapping

The Designer contains Mapping Assist and Data Assist features. Both are based on AI algorithms to help you with mapping.
suggestions.

Mapping Assist runs locally, together with the designer, so you don't need any cloud connections or subscriptions to use
it. You will need to download and run a single IBM-provided container which hosts the LLM, this can be done with Podman,
Docker, or any other container orchestrator. Just configure the endpoint in the `designer.conf.yaml`

![img_21.png](img_21.png)

The Data Assist uses the same technology and setup, but it helps users construct JSONata expressions that can be used within
a graphical mapping (if that's your thing, not a fan myself).

#### Designer Account Managing

The Designer allows you to (since 13.0.5.0) choose an alternative name for the account information name you use during
the discovery process.

### Toolkit Enhancements

#### New Nodes (and updates)

##### Discovery Request Nodes

Each new release brings new Discovery Request Nodes along. There are so many by now, that I'll just limit myself to
list them all out

| 13.0.1.0                       | 13.0.3.0                           | 13.0.4.0                             | 13.0.5.0                   | 13.0.6.0      |
|--------------------------------|------------------------------------|--------------------------------------|----------------------------|---------------|
| Businessmap Request node       | Azure Cosmos DB Request node       | Azure Service Bus Request node       | Microsoft Azure Event Hubs | Apache Pulsar |
| ClickSend Request node         | Milvus Request node                | IBM Planning Analytics Request node  | Google Gemini              | AstraDB       |
| Crystal Ball Request node      | Pinecone Vector Database Request   |                                      | IBM Aspera                 | Databricks    |
| Factorial HR Request node      | Workday Request                    |                                      | Redis                      |               |
| Front Request node             |                                    |                                      | Splunk                     |               |
| Hunter Request node            |                                    |                                      | Vespa                      |               |
| IBM Targetprocess Request node |                                    |                                      |                            |               |
| IBM watsonx.ai Request node    |                                    |                                      |                            |               |
| Infobip Request node           |                                    |                                      |                            |               |
| Toggl Track Request node       |                                    |                                      |                            |               |
| Wrike Request node             |                                    |                                      |                            |               |
| Zoho Books Request node        |                                    |                                      |                            |               |
| Zoho CRM Request node          |                                    |                                      |                            |               |
| Zoho Inventory Request node    |                                    |                                      |                            |               |
| Zoho Recruit Request node      |                                    |                                      |                            |               |



##### Discovery Input Nodes

Each new release brings new Discovery Input Nodes along. There are so many by now, that I'll just limit myself to
list them all out

| 13.0.1.0                     | 13.0.4.0                       | 13.0.5.0                   | 13.0.6.0            |
|------------------------------|--------------------------------|----------------------------|---------------------|
| Businessmap Input node       | Amazon Event Bridge Input node | Microsoft Azure Event Hubs | Apache Pulsar,      |
| ClickSend Input node         | Azure Service Bus Input node   |                            | AstraDB             |
| Eventbrite Input node        |                                |                            | Databricks          |
| Front Input node             |                                |                            | SAP SuccessFactors  |
| Greenhouse Input node        |                                |                            |                     |
| IBM Maximo Input node        |                                |                            |                     |
| IBM Targetprocess Input node |                                |                            |                     |
| Magento Input node           |                                |                            |                     |
| Marketo Input node           |                                |                            |                     |
| Slack Input node             |                                |                            |                     |
| Toggl Track Input node       |                                |                            |                     |
| Wrike Input node             |                                |                            |                     |
| Zoho Books Input node        |                                |                            |                     |
| Zoho CRM Input node          |                                |                            |                     |
| Zoho Recruit Input node      |                                |                            |                     |

##### JSONata Mapping Node

![img_1.png](img_1.png)

JSONata is a lightweight query and transformation language specifically designed for interacting with JSON data. You can
compare it to XSLT for XML.

##### Kafka Nodes

The KafkaProducer, KafkaConsumer and KafkaRead nodes support Avro and Schema Registries.

![img_4.png](img_4.png)

It does require you to use a Schema Registry Policy.

![img_5.png](img_5.png)

The KafkaProducer and KafkaConsumer nodes now support transactionality in writing and reading messages. This can be
configured via a set of new properties.

![img_27.png](img_27.png)

![img_28.png](img_28.png)

Kafka nodes support scaling via
- setting additional instances (process messages in parallel)
- deploying multiple message flows with the same consumer group ID and subscribed to the same Topic name
- enabling multiple kafka connections (pull more messages concurrently)

![img_29.png](img_29.png)

##### TCPIP Nodes

![img_7.png](img_7.png)

TCPIP nodes now support timeout values expressed as fractions of a second, up to 3 decimal places, expressed as `0.250`.
`0.100` is the shortest supported timeout.

##### Couchbase Request Node

![img_8.png](img_8.png)

You can use the Couchbase Request node to connect to Couchbase and issue requests to perform actions on objects such as
buckets, collections, custom SQL, documents, and scopes. It comes with a matching policy as well.


##### Salesforce Nodes

Salesforce nodes now can be configured to use an HTTP proxy by setting a policy with the proxy details

![img_14.png](img_14.png)

![img_15.png](img_15.png)


##### HTTPRequest Node

The HTTPRequest node support Retry capability directly from the node config.

- Retry Mechanism: no or short
- Retry Threshold: number of retries
- Short Retry Interval: time interval between retries in seconds
- Retry Condition: the errors on which to retry

![img_18.png](img_18.png)

![img_19.png](img_19.png)

Oauth2.0 support has also been made available in the HTTP Request nodes. The HTTP Request node is associated with
credentials of type `http`.

Supported Authentication types and options:
- apiKey
- basic
- basicApiKey
- bearerToken
- client
- oauth
- oauthPassword

To communicate with HTTP endpoints that are secured using OAuth 2.0, there are 6 new properties to the HTTP policy
which are shown in the picture below:

![img_24.png](img_24.png)

##### RestRequest Node

Oauth2.0 support has also been made available in the REST Request nodes. The REST Request node is associated with
credentials of type `rest`.

Supported Authentication types and options:
- apiKey
- basic
- basicApiKey
- bearerToken
- client
- oauth
- oauthPassword
  The security scheme configuration can be provided by the Open API document associated with the node

##### Callable Flow Nodes

Has been enhanced with Supported Domains. These are new properties on the CallableInput and CallableReply nodes. It shows
the supported message domains and models and can be configured to check the messages against the domains.

##### Salesforce Input Node

The Salesforce input node supports a state presitence policy to enable robust data handling and minimize downtime. This
helps processing messages even if the flow is not running but Salesforce events are still being generated.
This does require an external persitence provider, which can be either FILE or REDIS.

![img_22.png](img_22.png)

![img_23.png](img_23.png)

##### MQTT Nodes

MQTT version 5 is supported. This is reflected in the MQTT policies

![img_25.png](img_25.png)

##### Microsoft Azure Blob Storage Request node

The Microsoft Azure Blob Storage Request node support directly pushing Blob data without having to convert to JSON first.

![img_32.png](img_32.png)



#### Build in console
The toolkit allows you to run ACE commands straight from within the toolkit.

![img_10.png](img_10.png)

#### External Directory Vault explorer

Managing an external directory vault is now possible from within the toolkit: create, connect and manage credentials.

![img_2.png](img_2.png)

#### Container Explorer view

You can now add and manage ACE CC containers deployed on a k8s platform directly from within the toolkit. Just add the
dashboard link to the toolkit.

![img_16.png](img_16.png)

![img_17.png](img_17.png)

#### Context Trees

I might be biased (it's my blog, so I'm allowed to be), but Context Trees is a big one. If I'm allowed to steal a description
from another one of my blogs (again, my blog, so I am allowed):

_It was originally designed to support discovery connectors, but it also gives you a sharp way to handle message data in
classic ACE flows. Let's give you some context (pun intended) first. The Context tree is a read-only logical structure
that grows as your message passes through the flow. At the start it only knows about the input node, but each node adds
its own payload and metadata. By the end you have a complete picture, parser context included. The important bit for us:
the original payload is always available. In practice, you don’t need to configure or enable anything special. As soon
s you reference the Context tree in ESQL, ACE populates it at runtime._

Couldn't have said it better myself (hm, maybe I need to stop writing in the evenings).

Context trees are also visible in the Debugger and Flow Exercisers (since 13.0.5.0).

![img_30.png](img_30.png)

![img_31.png](img_31.png)

There are also new ESQL and Java methods to support interacting with the Context Trees

ESQL:

- CONTEXTINVOCATIONNODE
- CONTEXTREFERENCE

Java:

- MbContextTreeNode
- MbContextTreeNodePayload

### CLI Enhancements

#### ibmint

##### ibmint deploy
ibmint deploy supports additional ssl options
- `--output-uri URI` URI for a remote integration server in the form tcp://[user[:password]@]host:port or in the form ssl://[user[:password]@]host:port.
- `--https` specifies that HTTPS will be used for the connection to the integration node or server.
- `--no-https` specifies that HTTPS will not be used for the connection to the integration node or server.
- `--cacert cacertFile` specifies the path to the certificate file (in either PEM, P12, or JKS format)
- `--cacert-password cacertPassword` the password for password-protected cacert files.
- `--insecure` Specifies that the certificate that is returned by the integration node or server will not be verified.

#### Auto-complete

ibmint commands on Linux and Unix support auto-complete.

#### ibmint remote connections

Add ssl connections settings for (see ibmint deploy for the params)

- ibmint create server command
- ibmint delete server command
- ibmint start server command
- ibmint stop server command
- ibmint display credentials command
- ibmint set credential command
- ibmint unset credential command


### Runtime Enhancements

#### Open Telemetry
OTel suppoert a basic auth security identity in the header of the OTel message taht is propagated to an extern OTel
collector.

These are available in the `server.conf.yaml`

![img_9.png](img_9.png)

#### IPv6

The HTTPConnect supports IPv6, but IPv4 remains the default

```yaml
HTTPConnector:
    #ListenerPort: 0              # Set non-zero to set a specific port, defaults to 7800
    #ListenerAddress: '0.0.0.0'      # Set the IP address for the listener to listen on all IPv4 addresses (Default)
    #ListenerAddress: '::'           # Set the IP address for the listener to listen on all IPv6 and all IPv4 addresses
    #ListenerAddress: 'ipv6:::'      # Set the IP address for the listener to listen on all IPv6 and all IPv4 addresses
    #ListenerAddress: '127.0.0.1'    # Set the IP address for the listener to listen on to the localhost IPv4 address
    #ListenerAddress: '::1'          # Set the IP address for the listener to listen on to the localhost IPv6 address
    #ListenerAddress: '2001:DB8::1'  # Set the IP address for the listener to listen on a specific IPv6 address
    #ListenerAddress: '192.168.0.1'  # Set the IP address for the listener to listen on a specific IPv4 address
```

#### Embedded Global Cache

The In-memory Embedded Global Cache allows for caching data between separate ACE integration servers. Each server
involved in  replication both reads and writes to the cache has to be explicitly nominated via the `server.conf.yaml`

Upsert is availabe for use within the JavaCompute nodes

![img_26.png](img_26.png)

![img_11.png](img_11.png)

#### External Redis Global Cache

If you want to use an external cache that you can share with other applications or want to replace a WXS grid solution,
Redis global cache is availble. ACE offers limited support for correct usage of the Redis API. A Redis Connection policy
and crendential type are available:

![img_12.png](img_12.png)

![img_13.png](img_13.png)

#### Open Telemetry

The current nodes that can send OTel traces
- MQInput, MQOutput, MQReply, MQGet, MQPublication
- HTTPInput, HTTPReply, HTTPRequest, HTTPAsyncRequest, HTTPAsyncResponse
- RESTRequest, RESTAsyncRequest, RESTAsyncResponse
- SOAPInput, SOAPReply, SOAPRequest, SOAPAsyncRequest, SOAPAsyncResponse
- CallableInput, CallableReply, CallableFlowInvoke, CallableFlowAsyncInvoke, CallableFlowAsyncResponse
- KafkaConsumer, Kafka Read, KakfaProducer

### Java

You might think that this should be part of a runtime or the Toolkit chapter, but seeing as the java upgrade is a pretty
big deal, it gets its own chapter.

IBM Semeru Java 17 is now the default for both the Toolkit and the ACE Runtimes. Java 1.8 is still shipped, and you can
select it if you need it. Initially some features were not supported under Java 17, but each consecutive release brought
more support.

Currently the follow restrictions are in place
- Nodes only enabled under Java 17: CDC Node
- Nodes not supported under Java 17:
  - CORBARequest
  - WRR
  - WXS
  - WS-Security
  - WS-ReliableMessaging
  - TFIM
- Environment variables
  - TMPDIR is not observered under Java 17, use _JAVA_OPTIONS or jvmSystemProperty in the *.conf.yaml files

```java
_JAVA_OPTIONS="-Djava.io.tmpdir=/apps/mqsi/javacache"
```

```java
ResourceManagers:
  JVM:
    jvmSystemProperty:
```

If you have a JavaCompute node and/or custom Java Input or Compute nodes, make sure to test each of them.

### Credentials

With ace choosing for the vault and credentials over mqsisetdbparms (don't worry, it stil works), there are also some
aadditions and improvements in the way ACE interacts with credentials.
One of these is dynamic credentials. These are credentials that can be changed and updated without having to restart the
server.

A list of dynamic credentials (in short, most of them)

| Connector                     | Connector                   | Connector                     | Connector                    |
|-------------------------------|-----------------------------|-------------------------------|------------------------------|
| amazoncloudwatch (dynamic)    | amazondynamodb (dynamic)    | amazonec2 (dynamic)           | amazoneventbridge (dynamic)  |
| amazonkinesis (dynamic)       | amazonlambda (dynamic)      | amazonrds (dynamic)           | amazonredshift (dynamic)     |
| amazons3 (dynamic)            | amazonses (dynamic)         | amazonsns (dynamic)           | amazonsqs (dynamic)          |
| anaplan (dynamic)             | apachepulsar (dynamic)      | apptiotargetprocess (dynamic) | asana (dynamic)              |
| astradb (dynamic)             | azuread (dynamic)           | azureblobstorage (dynamic)    | azurecosmosdb (dynamic)      |
| azureeventhub (dynamic)       | azureservicebus (dynamic)   | bamboohr (dynamic)            | box (dynamic)                |
| businessmap (dynamic)         | calendly (dynamic)          | cd (static)                   | cdc (dynamic)                |
| cics (static)                 | clicksend (dynamic)         | cloudantdb (dynamic)          | cmis (dynamic)               |
| confluence (dynamic)          | couchbase (dynamic)         | coupa (dynamic)               | crystalball (dynamic)        |
| databricks (dynamic)          | db2 (dynamic)               | docusign (dynamic)            | dropbox (dynamic)            |
| eis (dynamic)                 | elk (static)                | email (static)                | eventbrite (dynamic)         |
| expensify (dynamic)           | factorialhr (dynamic)       | filenet (dynamic)             | front (dynamic)              |
| ftp (dynamic)                 | github (dynamic)            | gitlab (dynamic)              | gmail (dynamic)              |
| googleanalytics (dynamic)     | googlebigquery (dynamic)    | googlecalendar (dynamic)      | googlechat (dynamic)         |
| googlecloudstorage (dynamic)  | googlecontacts (dynamic)    | googledrive (dynamic)         | googlegemini (dynamic)       |
| googlegroups (dynamic)        | googlepubsub (dynamic)      | googlesheet (dynamic)         | googletasks (dynamic)        |
| googletranslate (dynamic)     | greenhouse (dynamic)        | http (dynamic)                | httpproxy (static)           |
| hubspotcrm (dynamic)          | hubspotmarketing (dynamic)  | hunter (dynamic)              | ibmaspera (dynamic)          |
| ibmcoss3 (dynamic)            | ibmewm (dynamic)            | ibmopenpages (dynamic)        | ibmsterlingiv (dynamic)      |
| ibmtwc (dynamic)              | ibmwatsonxai (dynamic)      | ift (dynamic)                 | ims (static)                 |
| infobip (dynamic)             | insightly (dynamic)         | jdbc (static)                 | jenkins (dynamic)            |
| jira (dynamic)                | jms (static)                | jndi (static)                 | kafka (static)               |
| kerberos (static)             | keystore (static)           | keystorekey (static)          | kronos (dynamic)             |
| ldap (dynamic)                | local (dynamic)             | loopback (static)             | magento (dynamic)            |
| mailchimp (dynamic)           | marketo (dynamic)           | maximo (dynamic)              | mcp (dynamic)                |
| milvus (dynamic)              | mondaydotcom (dynamic)      | mq (dynamic)                  | mqtt (static)                |
| msad (dynamic)                | msdynamicscrmrest (dynamic) | msdynamicsfando (dynamic)     | msexcel (dynamic)            |
| msexchange (dynamic)          | msonedrive (dynamic)        | msonenote (dynamic)           | mspowerbi (dynamic)          |
| mssharepoint (dynamic)        | mssql (dynamic)             | msteams (dynamic)             | mstodo (dynamic)             |
| mysql (dynamic)               | odbc (dynamic)              | odm (static)                  | opentelemetry (dynamic)      |
| oracle (dynamic)              | oracleebs (dynamic)         | oraclehcm (dynamic)           | pineconedb (dynamic)         |
| planninganalytics (dynamic)   | postgres (dynamic)          | redis (dynamic)               | rest (dynamic)               |
| salesforce (dynamic)          | salesforceae (dynamic)      | salesforcemc (dynamic)        | sapariba (dynamic)           |
| sapodata (dynamic)            | sapsuccessfactors (dynamic) | schemaregistry (static)       | servicenow (dynamic)         |
| sfcommerceclouddata (dynamic) | sftp (dynamic)              | shopify (dynamic)             | slack (dynamic)              |
| smtp (dynamic)                | snowflake (dynamic)         | soap (dynamic)                | splunk (dynamic)             |
| square (dynamic)              | surveymonkey (dynamic)      | toggltrack (dynamic)          | trello (dynamic)             |
| truststore (static)           | truststorekey (static)      | twilio (dynamic)              | userdefined (dynamic)        |
| vespa (dynamic)               | watsondiscovery (dynamic)   | wordpress (dynamic)           | workday (dynamic)            |
| wrike (dynamic)               | wsrr (static)               | wufoo (dynamic)               | wxs (static)                 |
| yammer (dynamic)              | yapily (dynamic)            | zendeskservice (dynamic)      | zohobooks (dynamic)          |
| zohocrm (dynamic)             | zohoinventory (dynamic)     | zohorecruit (dynamic)         | zosconnect (dynamic)         |


### Business Transaction Monitoring

BTM extends the set of supported databases to include MS SQL Server and PostgreSQL, alongside DB2 and Oracle which were
previously already supported. ACE makes connections to the database using ODBC.

- On Windows, the ODBC driver for MS SQL Server is provided by the operating system.
- On the other ACE platforms, ACE provides a DataDirect ODBC driver for connecting to MS SQL Server.
- On Windows and xLinux, ACE provides a DataDirect ODBC driver for connecting to PostgreSQL.

### Database

#### PostgreSQL

Since 13.0.2.0, PostgreSQL is extended to support stored procedures that return dynamic result sets. You may notice a
slight difference in the syntax we are promoting for PostgreSQL. For PostgreSQL, a dummy cursor value must be supplied
in the ESQL CALL statement for each intended results set.

### AI

Watsonx Code Assistant chat is embedded in the ACE Toolkit. You do need an additional subscription to use this feature.
It is designed for

- Asking generalized questions
- Providing explanations for existing code
- Generating instance data to match a schema
- Generating a schema by providing example instance data
- Generating Java code snippets through natural language
- Generating ESQL code snippets through natural language
- Generation of Unit tests
-
![img_20.png](img_20.png)

## Migration

I will talk about migration, but that is another article all together.

## Closing

Hopefully this has been of some value to some of you. Feel free to make positive suggestions or just let me know if you
found it usefull.

# References

- [IBM App Connect Enterprise_13.0.x - Product lifecycle](https://www.ibm.com/support/pages/ibm-app-connect-enterprise130x)
- [New function added in IBM App Connect Enterprise 13.0 modification packs](https://www.ibm.com/docs/en/app-connect/13.0.x?topic=wniv1-new-function-added-in-app-connect-enterprise-130-modification-packs)
- [Explore the new features in App Connect Enterprise 13.0.1.0](https://community.ibm.com/community/user/blogs/ben-thompson1/2024/09/27/ace-13-0-1-0)
- [Explore the new features in App Connect Enterprise 13.0.2.0](https://community.ibm.com/community/user/blogs/ben-thompson1/2024/12/06/ace-13-0-2-0)
- [Explore the new features in App Connect Enterprise 13.0.3.0](https://community.ibm.com/community/user/blogs/ben-thompson1/2025/03/30/ace-13-0-3-0)
- [Explore the new features in App Connect Enterprise 13.0.4.0](https://community.ibm.com/community/user/blogs/ben-thompson1/2025/06/18/ace-13-0-4-0)
- [Explore the new features in App Connect Enterprise 13.0.5.0](https://community.ibm.com/community/user/blogs/ben-thompson1/2025/09/25/ace-13-0-5-0)
- [Explore the new features in App Connect Enterprise 13.0.6.0](https://community.ibm.com/community/user/blogs/ben-thompson1/2025/12/11/ace-13-0-6-0)