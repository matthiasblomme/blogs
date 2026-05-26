---
date: 2026-05-21
title: 'Dynamic startup resources: faster ACE startup without paying for the CPU'
image: cover.png
description: ACE 13.0.6 (operator 12.17.0+) introduces spec.startupResources on the
  IntegrationRuntime CR. The container can request a big CPU burst at startup to
  shorten boot time, then in-place-resize down to the steady-state request for the
  rest of its life. Licensing only counts the steady-state CPU. Cool feature with
  one big compatibility footnote.
tags:
- ace
- kubernetes
- startup-resources
- in-place-pod-resize
- 13.0.6
- operator-12.21
status: draft
---

# Dynamic startup resources

> _Draft. Compatibility note captured; full walkthrough pending a working cgroup-v2 test
> cluster._

(Intro — what the feature is, why you'd want it. Link to Rob Convery's IBM Community
post: <https://community.ibm.com/community/user/blogs/rob-convery1/2025/10/16/dynamic-cpu-allocation-for-faster-startup>.
TL;DR: ask for a big CPU burst at container start to shave seconds off ACE boot, then
have Kubernetes resize the running container down to a small steady-state request.
Licensing only counts the steady-state CPU, so this is essentially free startup speed.)


## Compatibility footnote: this needs cgroup v2

Two requirements get billed up front, and there's a quieter third one that bit me when
I first tried this.

Up-front requirements (from IBM's docs / Rob's post):

- App Connect Operator **≥ 12.17.0**
- Kubernetes **≥ 1.33** (in-place pod resize is BETA in 1.33, GA in 1.35) or
  OpenShift **≥ 4.20** (RC in 4.20, available 4.22+)

Unwritten third requirement that you find out the hard way:

- **The host's cgroup hierarchy must be v2.**

ACE's container startup script verifies the in-place resize completed by reading
`/sys/fs/cgroup/cpu.max`. That path only exists on cgroup v2. On cgroup v1 the
equivalent files live elsewhere (`/sys/fs/cgroup/cpu/cpu.cfs_quota_us`,
`cpu.cfs_period_us`) and the ACE script doesn't have a fallback for them. It errors,
the container exits 1, Kubernetes restarts it. Forever.

Confirmed on a vanilla `minikube` install (which defaults to cgroup v1 unless you go
out of your way to flip it):

```text
2026-05-21 19:55:56  Integration server is ready
2026-05-21 19:55:56  Resize: RUNNING_CPU_LIMITS env var set to 300m so checking container has been resized
2026-05-21 19:55:56  Resize: File /sys/fs/cgroup/cpu.max does not exist
2026-05-21 19:55:56  Resize: Error: Hit error looping waiting for the pod resize to complete - err:stat /sys/fs/cgroup/cpu.max: no such file or directory
```

Notice the timing: ACE itself starts cleanly. `BIP1991I: Integration server has
finished initialization` fires. The crash is **purely in the post-startup
resize-verification step**, after the runtime is up. Kubernetes never sees the
container reach `Ready`, restarts it, the same script runs again, fails again,
72-restarts-and-counting before I gave up.

### Where you'll hit this in practice

- **Managed Kubernetes (IKS, EKS, GKE, AKS, OpenShift 4.13+)** — all run cgroup v2 by
  default. Most production paths are fine; the feature just works.
- **Vanilla minikube on Docker Desktop / WSL2** — defaults to legacy cgroup v1 hybrid
  unless explicitly configured. To get cgroup v2 you typically need a fresh profile
  started against a `containerd` runtime on a host whose Docker is already on
  unified-hierarchy cgroups. Easier said than done; depends on your Docker / WSL /
  host kernel.
- **kind, k3d, k3s** — usually cgroup v2 on recent versions, but verify.

### How to tell which cgroup version you're on

From any pod:

```bash
kubectl exec -n <ns> <pod> -- sh -c 'cat /sys/fs/cgroup/cgroup.controllers 2>/dev/null && echo "v2" || echo "v1"'
```

`cgroup.controllers` only exists on v2 — if it returns content, you're on v2; if it
errors out, you're on v1.

### No cgroup v1 fallback as of 13.0.7.0

The ACE container shipped with operand `13.0.6.2-r1` and the 12.21.0 operator does not
have a cgroup v1 path in its resize-verification script. Worth raising with IBM
Support if you have a customer environment pinned to v1; the answer is going to be
"upgrade your host."


## What the feature does

(TODO — write up after testing on the cgroup-v2 cluster.)


## Setting it up

(TODO — `spec.startupResources` shape, `template.spec.containers[].resources` shape,
the QoS-stability constraint Rob's post calls out.)


## Watching the resize happen

(TODO — `kubectl get pod -o jsonpath` of `spec.containers[].resources` vs
`status.containerStatuses[].resources`, the `CPUResizeComplete` pod condition,
operator log lines.)


## Caveats

(TODO — what we found doesn't work / surprises during testing.)


---

## References

* [Rob Convery — Dynamic CPU Allocation for Faster Startup](https://community.ibm.com/community/user/blogs/rob-convery1/2025/10/16/dynamic-cpu-allocation-for-faster-startup)
* [Kubernetes Enhancement Proposal 1287 — In-place Update of Pod Resources](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1287-in-place-update-pod-resources)
* TODO — IBM docs link for `spec.startupResources` once located

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)
