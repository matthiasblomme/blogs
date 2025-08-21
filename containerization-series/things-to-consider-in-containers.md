# My Containerizing IBM ACE: A Blog Series – Things to Consider in Containers

When people talk about running workloads in containers, it’s easy to get swept up in the hype. Containers solve a lot of problems: portability, speed, consistency. But they also reshape old challenges in new ways. This isn’t a “best practices” guide (you won’t find a silver bullet here), but rather a collection of things worth thinking about before they come back to bite you (silver bullet, biting… let’s hope it isn’t a full moon tonight).

## Persistence & State

Containers are ephemeral by nature, but ACE doesn’t always play by that rule. Some parts of the runtime *do* need persistence:

* Logs and monitoring data you don’t want to lose when a pod restarts.
* ACE dashboards, which remain persistent even if the runtime itself is disposable.
* File processing flows, which often require **network storage** so files can survive restarts and be shared between nodes.
* MQ messages, which must be persistent to prevent data loss.

The point isn’t that persistence (or the lack of it) is bad. It’s that you need to plan it explicitly rather than relying on the container itself to hold your state.

## Networking

Networking in containers looks simple until you hit production. With ACE, you’ll want to think about:

* **Internal service discovery**: how your ACE runtimes talk to other services.
* **Exposing your containers to the outside world**: think ingress, routes, or load balancers. Don’t just “expose everything and hope for the best.” Secure, controlled access matters.
* For APIs, consider an **API gateway** layered on top of your ACE flows. It adds governance and security beyond just pointing traffic straight at your pods.

## Scaling

One of the big promises of containers is easy scaling, but it’s not just a technical decision. With ACE:

* You can scale vertically (more resources for a container) or horizontally (more replicas).
* Autoscaling can help smooth workloads, but watch your licensing model. **More CPU = more PVUs = more money.** Scaling decisions directly affect your bill.

So yes, scale when you need to, but don’t ignore the financial side.

## Resource Management

ACE can be heavy at startup. If you’ve ever watched a container sit in “pending” or crashloop, you know what I mean. Setting CPU and memory requests and limits properly avoids the noisy-neighbor effect.

And since **Kubernetes 1.33**, you can define **startup resources**: a temporary boost to help pods through initialization before they settle into normal runtime limits. For ACE, that can make a real difference in startup stability.

## Configuration Management & Secrets

Baking everything into an image works for some setups, but often you’ll want to inject configs dynamically. Common approaches:

* **Environment variables**: simple, but not great for sensitive data.
* **Mounting ConfigMaps or Secrets**: inject files directly into the container filesystem.
* **External secret stores**: more advanced, but sometimes worth the setup.
* **ACE built-in vault**: can be injected via Kubernetes secrets mounted as a file, which lets you integrate ACE’s native vault with containerized deployments.

Whichever you pick, make sure it scales across dev, test, and prod without becoming a nightmare to maintain.

## Security & Monitoring

If you’re using an operator (like with CP4I), a lot of this is handled for you. If you’re not, you need to think about:

* How you’re logging and monitoring containers.
* Scanning images and keeping base images minimal.
* Securing secrets beyond just dropping them in environment variables.

These aren’t optional in production, but they also don’t have to be painful if you build them in from the start.

## But can you choose?

Chances are slim that if you are developing applications you’re also maintaining the container platform. That’s usually done by a dedicated container, cloud, or infra team. So a lot of these topics may already be solved for you. Some might even cause issues (not all solutions play nicely with ACE runtimes, dashboards, or operators). So definitely check with the responsible team and see if they’re open for a healthy discussion. And if you need to raise these questions, maybe this blog can help you frame the conversation.


## Closing Note

None of these points are meant to scare you away from containers. They’re meant to spark the right questions before something blows up in production. Containers give you speed and flexibility, but ACE still has real-world needs like persistence, security, and predictable scaling. Think of this list as a set of road signs: you don’t have to stop at all of them, but you should at least know they’re coming up.

---

For more integration tips and tricks, visit [Integration Designers](https://integrationdesigners.com/blog/) and check out our other blog posts.

---

## Other blogs from the Containerizing IBM ACE series

* Containerizing IBM ACE: A Blog Series – The Basics
* Containerizing IBM ACE: A Blog Series - Images vs Artifacts
*

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion \
\#AppConnectEnterprise(ACE)
