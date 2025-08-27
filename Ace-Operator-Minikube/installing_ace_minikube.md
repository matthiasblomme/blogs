# Installing ACE 13.x on Minikube: Filling in the Blanks

Even though we hardly ever see it, IBM App Connect Enterprise (ACE) is perfectly capable of running on plain Kubernetes. 
But let’s be honest, it looks much fancier on OpenShift 😉. If you're not using OpenShift or a Cloud Pak install, getting 
it all up and running becomes a much more hands-on operation.

In this blog, I’ll be deploying ACE 13.x manually on Minikube, including the Operator, Dashboard, and a runtime. Along 
the way, I’ll share the practical steps, issues I ran into, and the patches or tweaks I made to get it working. If you’re 
running outside the officially supported clusters or on NOKS (that is Non-OpenShift Kubernetes), this should help you 
dodge a few potholes.


## Assumptions

This post assumes:

* You already have Kubernetes and Helm installed
* You’re working with a functional cluster (Minikube or alternative)
* You know your way around `kubectl`, YAML, and k8s cluster basics

Getting started with Minikube? Or simply don't have Kubernetes or Helm installed, I’ve dropped a couple of reference 
links at the bottom.


## Step 0: Optimizing My Local Setup

Before touching the cluster, let’s make our shell faster to work with and create a dedicated namespace.

Set aliases for my most used commands (I'm doing this in powershell):

```powershell
# Alias for kubectl to save keystrokes
Set-Alias -Name k -Value kubectl
```
```powershell
# Alias for minikube for quick commands
Set-Alias -Name m -Value minikube
```

If you don't want to set them each time you open a new session, make them persistent. Open up the powershell profile 
file (or create it if it doesn't exist yet):

```powershell
notepad $PROFILE
```

Paste both alias lines into the file and save.

```powershell
Set-Alias -Name k -Value kubectl
```
```powershell
Set-Alias -Name m -Value minikube

```

Create a dedicated namespace, ace-demo, for our setup and make that namespace the default one (saves you from typing -n 
ace-demo each time):

```bash
k create namespace ace-demo
```
```bash
k config set-context --current --namespace=ace-demo
```


## Step 1: Add the IBM Helm Chart Repo

Before we can install the Operator, we need the source. Adding IBM’s Helm repo ensures we’re pulling the official charts 
and latest versions.

```bash
helm repo add ibm-helm  https://raw.githubusercontent.com/IBM/charts/master/repo/ibm-helm
```
```bash
helm repo update
```

Before we can install the Operator, we need the source. Adding IBM’s Helm repo ensures we’re pulling the official charts 
and latest versions.

```bash
helm repo add ibm-helm  https://raw.githubusercontent.com/IBM/charts/master/repo/ibm-helm
```
```bash
helm repo update
```


## Step 2: Install the k8s cert-manager
If you have a clean cluster without a cert-manager installed, begin by installing it, you will need it later. Check if 
they are installed (if you are not sure about your cluster setup). 

Check the the cert-manager namespace

```bash
k -n cert-manager get pods
No resources found in cert-manager namespace.
```

Or try to list all cert-manager instance pods

```bash
k get pods -A -l instance=cert-manager
No resources found
```

If these return nothing, install the official cert-manager
```bash
k apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.2/cert-manager.yaml
```

Wait for the pods to run:

```bash
k -n cert-manager get pods -w
NAME                                      READY   STATUS    RESTARTS   AGE
cert-manager-6468fc8f56-t4l8t             1/1     Running   0          2d4h
cert-manager-cainjector-7fd85dcc7-xfghw   1/1     Running   0          2d4h
cert-manager-webhook-57df45f686-8fchm     1/1     Running   0          2d4h
```

Verify the curstom resource definitions:

```bash
k get crd issuers.cert-manager.io clusterissuers.cert-manager.io certificates.cert-manager.io
NAME                             CREATED AT
issuers.cert-manager.io          2025-08-11T07:55:17Z
clusterissuers.cert-manager.io   2025-08-11T07:55:16Z
certificates.cert-manager.io     2025-08-11T07:55:16Z
```

If you don't install the cert-manger, your Operator pod fails to start with the below error:
```
no matches for kind "Issuer" in version "cert-manager.io/v1"
```

## Step 2: Install the ACE Operator

The operator is a Kubernetes controller that watches ACE custom resources (Dashboard, IntegrationRuntime/IntegrationServer, 
DesignerAuthoring, SwitchServer, Configuration, Trace) and reconciles the corresponding Deployments, Services, and PVCs.
The ace-operator-values.yaml file contains some basic values, nothing special. The most important one (for our setup), 
is the version tag.

```bash
helm install ibm-appconnect ibm-helm/ibm-appconnect-operator -f ./ace-operator-values.yaml
NAME: ibm-appconnect
LAST DEPLOYED: Fri Aug 22 14:16:35 2025
NAMESPACE: ace-demo
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The AppConnect Operator has been deployed!

To verify your install, look for:
- Operator pod:                     kubectl get pod | grep 'ibm-appconnect-ibm-appconnect-operator'
- MutatingWebhookConfigurations:    kubectl get mutatingwebhookconfigurations | grep 'ace-demo'
- ValidatingWebhookConfigurations:  kubectl get validatingwebhookconfigurations | grep 'ace-demo'
- Cluster Role:                     kubectl get clusterrole | grep 'ibm-appconnect-ace-demo-ibm-appconnect-operator'
- Cluster Role Binding:             kubectl get clusterrolebinding | grep 'ibm-appconnect-ace-demo-ibm-appconnect-operator'
- Role:                             kubectl get role | grep 'ibm-appconnect-ace-demo-ibm-appconnect-operator'
- Role Binding:                     kubectl get rolebinding | grep 'ibm-appconnect-ace-demo-ibm-appconnect-operator'
- Service Account:                  kubectl get serviceaccount | grep 'ibm-appconnect'
```

Example `ace-operator-values.yaml`:

```yaml
# ace-operator-values.yaml
namespace: "ace-demo"               # Namespace to install into
operator:
  replicas: 1                        # Single operator instance
  deployment:
    repository: icr.io/cpopen        # IBM container registry repo
    image: appconnect-operator       # Operator image name
    tag: 12.14.0                      # Version tag of operator
    pullPolicy: Always                # Always pull image of given tag
    resources:
      requests:
        cpu: "100m"                  # Minimum CPU request
        memory: 128Mi                # Minimum memory request
      limits:
        cpu: "250m"                  # Maximum CPU limit
        memory: 1Gi                   # Maximum memory limit
  installMode: OwnNamespace          # Restrict operator to its namespace
  imagePullSecrets:
    - ibm-entitlement-key            # Secret for pulling IBM entitled images
```


## Step 3: Create Persistent Volume Claim for Dashboard

The Dashboard stores configuration and runtime data in persistent storage. Without a PVC, it has nowhere to keep BAR files 
or settings. ACE can automatically create a matching PVC for your dashboard, if you have a RWX (Read Write Many) storage 
class available. My local setup did not have one that supports RWX, but if you plan to run a single instance of your 
dashboard (which I plan to do) you can get away with manually creating a RWO (Read Write Once) PVC and manually assign 
it to the dashboard.

Example `ace-dashboard-pvc.yaml`:

```yaml
# ace-dashboard-pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ace-dashboard-content        # Name referenced in Dashboard CR
  namespace: ace-demo                # Namespace for PVC
spec:
  storageClassName: your-storage-class # Must match available storage class
  accessModes:
    - ReadWriteOnce                  # Access mode (change to RWX if supported)
  resources:
    requests:
      storage: 5Gi                    # Size of the volume
```

Apply the PVC

```bash
k apply -f ./ace-dashboard-pvc.yaml
persistentvolumeclaim/ace-dashboard-content created
```

### Image pull issue: Entitlement key

From this point onwards, you need an entitlement key in place. The entitlement key is what grants you access to the IBM 
Container images. Ensure your that your entitlement includes container access. If this is not the case, request it.

Creating the k8s secret for the entitlement key (typically called ibm-entitlement-key).
```bash
k create secret docker-registry ibm-entitlement-key \
  --docker-username=cp \
  --docker-password=<your-entitlement-key> \
  --docker-server=cp.icr.io \
  --namespace=ace-demo
```

This is a manual action, not a versioned yaml. Don't put your secrets in source control ;).


## Step 4: Deploy the ACE Dashboard

The dashboard is the main UI for ACE. It can be used to store bar files you want to use in your Integration Runtimes.
Below you see a yaml file with a minimal setup. Note the version is set to '13.0', important if you want it to work with 
the operator version '14.12.0'. The licence and use will determine if you are going to pay any license costs, so choose wisely.

```yaml
# ace-dashboard.yaml
apiVersion: appconnect.ibm.com/v1beta1
kind: Dashboard
metadata:
  name: ace-dashboard
  namespace: ace-demo
spec:
  license:
    accept: true
    license: L-KPRV-AUG9NC
    use: AppConnectEnterpriseNonProductionFREE
  pod:
    containers:
      content-server:
        resources:
          limits:
            memory: 512Mi
          requests:
            cpu: 50m
            memory: 50Mi
      control-ui:
        resources:
          limits:
            memory: 512Mi
          requests:
            cpu: 50m
            memory: 125Mi
  switchServer:
    name: default
  authentication:
    integrationKeycloak:
      enabled: false
  authorization:
    integrationKeycloak:
      enabled: false
  api:
    enabled: true
  storage:
    type: persistent-claim
    claimName: ace-dashboard-content
  displayMode: IntegrationRuntimes
  replicas: 1
  version: '13.0'
```

Create the dashboard:

```bash
k apply -f ./ace-dashboard.yaml
dashboard.appconnect.ibm.com/ace-dashboard created
```

### Configuration issue: using the proper version combination
Because I was looking at v12 documentation of the dashboard (we are curently running ACE v12), I deployed the dashboard
with version 12.0, not really giving it much thought, just following the ibm documentation. This led me to the following error

```bash
k get events
LAST SEEN   TYPE      REASON               OBJECT                                     MESSAGE
12m         Warning   FailedMount          pod/ace-dashboard-dash-569fc47469-5bp56    MountVolume.SetUp failed for volume "resources" : configmap "appconnect-resources" not found
```

The dashboard was not finding a very specific configmap that it required.

After much searching around, it turned out I needed the proper version of the dashboard to go with the operator
In a more recent version of the dashboard, the original appconnect-resources configmap was replaced with 3 other configmaps:
- appconnect-resources-csv
- appconnect-resources-ir-crd
- appconnect-resources-is-crd

Combining operator version '12.14.0' with dashboard '13.0' did work. The default settings for the operator point you to 
a sha version of the image, but you can work with a tag as well (less sensitive to typo's). By adding the tag to the 
ace-operator-values.yaml file (as we did in the beginning of the blog) should prevent this error all together.


### Init Conatiner issue: content-server-init CrashLoop

IBM states:

> The App Connect Dashboard requires a file-based storage class with ReadWriteMany (RWX) capability. If using IBM Cloud, 
> use the `ibmc-file-gold-gid` storage class. The file system must not be root-owned and must allow read/write access for 
> the user that the Dashboard runs as.

If these requirements aren’t met, the init container may fail with permission denied errors and get stuk in a restart loop.
Diagnosing this problem:
```bash 
k get pods 
NAME                                     READY   STATUS      RESTARTS         AGE
ace-dashboard-dash-5b58fcc746-dtsqf      0/2     Restarting  5                10m

k ace-dashboard-dash-5b58fcc746-dtsqf -c content-server-init -f
mkdir: cannot create directory '/mnt/data/content': Permission denied
chmod: cannot access '/mnt/data/content': No such file or directory
```

This issue can be fixed by patching the underlying Deployment with the correct `runAsUser` and `fsGroup` values.

```yaml
# ace-dash-deployment-patch.yaml
spec:
  strategy:
    rollingUpdate:
      maxSurge: 0
      maxUnavailable: 1
  template:
    spec:
      securityContext:
        runAsUser: 1000
        fsGroup: 1001
```

Applying the patch, scale the deployment down first, since we are running on a RWO PVC, we can't have the dashboard spin 
up a new version first to do a rolling update. Don't forget to scale it back up after applying the patch.

```bash
kubectl scale deployment ace-dashboard-dash --replicas=0
```
```bash
kubectl patch deployment ace-dashboard-dash --type=merge --patch-file ./ace-dash-deployment-patch.yaml
```
```bash
kubectl scale deployment ace-dashboard-dash --replicas=1
```


## Step 5: Expose the Dashboard

Service vs Ingress (quick primer): the Service provides a stable, internal endpoint for pods inside the cluster; the 
Ingress (plus an ingress controller like NGINX) exposes HTTP(S) routes from outside the cluster to that Service and 
lets you use hostnames and TLS.

Upon the dashboard creation, you also get a dashboard service called ace-dashboard-dash. It exposes ports 3443 
(content server), 8300 (ui) and 8400 (api). To quickly check the dashboard status:

```bash
k get dashboards
NAME              RESOLVEDVERSION   REPLICAS   CUSTOMIMAGES   STATUS   UI URL   API URL   KEYCLOAK URL   AGE
ace-dashboard     13.0.4.1-r1       1          false          Ready                                      2d3h
```

```bash
k get svc
NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
ace-dashboard-dash                ClusterIP   10.109.39.252   <none>        3443/TCP,8300/TCP,8400/TCP   2d3h

k get svc ace-dashboard-dash
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
ace-dashboard-dash   ClusterIP   10.109.39.252   <none>        3443/TCP,8300/TCP,8400/TCP   2d3h
```

We want to expose the dashboard by creating a simple ingress on the hostname ace-dashboard.local
Example Ingress:

```yaml
# ace-dashboard-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ace-dashboard-ingress
  namespace: ace-demo
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    nginx.ingress.kubernetes.io/proxy-ssl-verify: "false"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: ace-dashboard.local
    http:
      paths:
      - path: /apiv2
        pathType: Prefix
        backend:
          service:
            name: ace-dashboard-dash
            port:
              number: 8300   # UI port; UI proxies /apiv2 to API
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ace-dashboard-dash
            port:
              number: 8300   # UI port
```

Create the ingress
```bash
k apply -f ./ace-dashboard-ingress.yaml
ingress.networking.k8s.io/ace-dashboard-ingress created
```

We want to access the dashboard by using the hostname, so we'll need to add hostname to our Windows hosts file:

```powershell
> Add-Content "$env:SystemRoot\System32\drivers\etc\hosts" "`n127.0.0.1`tace-dashboard.local"
```

Enable port forwarding from your local system to your k8s cluster ingress

```bash
k -n ingress-nginx port-forward svc/ingress-nginx-controller 12121:443
Forwarding from 127.0.0.1:12121 -> 443
Forwarding from [::1]:12121 -> 443
```

Open:

```
https://ace-dashboard.local:12121/
```
![img.png](img.png)



### Securing your Ingress
Right now, the setup just proxies traffic straight through—TLS is handled by the dashboard itself, and NGINX is acting as 
a simple passthrough. For a stronger security model, you can flip that around and let the Ingress terminate TLS. That way, 
certificate management and rotation happen at the Ingress layer instead of inside the dashboard.

Add the spec.tls section to your Dashboard Ingress

```yaml
  tls:
  - hosts:
    - ace-dashboard.local
    secretName: ace-dashboard-tls    # cert-manager creates this Secret
  rules:
```

And start by creating your own certificate first, you can't use what you don't have.

```yaml
#dashboard-pod-cert.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ace-dashboard-tls
  namespace: ace-demo
spec:
  secretName: ace-dashboard-tls
  issuerRef:
    kind: ClusterIssuer
    name: selfsigned-issuer   # or your CA
  dnsNames:
  - ace-dashboard.local
```

```bash
k apply -f .\dashboard-pod-cert.yaml
certificate.cert-manager.io/ace-dashboard-tls created
```

Check if your certificate is actually getting created

```bash
k get cert
NAME                              READY   SECRET                            AGE
ace-dashboard-tls                 False   ace-dashboard-tls                 10s
ace-dashboardui-cert              True    ace-dashboardui-cert              7d5h
ibm-appconnect-webhook-ace-demo   True    ibm-appconnect-webhook-ace-demo   10d
```

If the ready state is stuck on _False_, check to see if you actually have the self signed issuer in you cluster. If you 
are running an empty new cluster, chances are you probably won't have it available. So let's create it:

```yaml
#clusterissuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
```

```bash
k get clusterissuer selfsigned-issuer
Error from server (NotFound): clusterissuers.cert-manager.io "selfsigned-issuer" not found
k apply -f .\clusterissuer.yaml
clusterissuer.cert-manager.io/selfsigned-issuer created
```

Your fully updated ingress will ook like this

```yaml
# ace-dashboard-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ace-dashboard-ingress
  namespace: ace-demo
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    nginx.ingress.kubernetes.io/proxy-ssl-verify: "false"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
      - ace-dashboard.local
    secretName: ace-dashboard-tls    # cert-manager creates this Secret
  rules:
  - host: ace-dashboard.local
    http:
      paths:
      - path: /apiv2
        pathType: Prefix
        backend:
          service:
            name: ace-dashboard-dash
            port:
              number: 8300   # UI port; UI proxies /apiv2 to API
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ace-dashboard-dash
            port:
              number: 8300   # UI port
```

Apply it 

```bash
k apply -f .\ace-dashboard-ingress.yaml
ingress.networking.k8s.io/ace-dashboard-ingress configured
```

Add the hostname to your windows hosts file (from elevated prompt)

```powershell
> Add-Content "$env:SystemRoot\System32\drivers\etc\hosts" "`n127.0.0.1`ace-dashboard.local"
```

Let's expose the Minikube ingress (in stead of port-forwarding)

```powershell
PS C:\Users\Bmatt> minikube addons enable ingress
💡  ingress is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
❗  Executing "docker container inspect minikube --format={{.State.Status}}" took an unusually long time: 3.3220798s
💡  Restarting the docker service may improve performance.
💡  After the addon is enabled, please run "minikube tunnel" and your ingress resources would be available at "127.0.0.1"
▪ Using image registry.k8s.io/ingress-nginx/controller:v1.12.2
▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.5.3
▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.5.3
🔎  Verifying ingress addon...
🌟  The 'ingress' addon is enabled
PS C:\Users\Bmatt> minikube tunnel
✅  Tunnel successfully started

📌  NOTE: Please do not close this terminal as this process must stay alive for the tunnel to be accessible ...

❗  Access to ports below 1024 may fail on Windows with OpenSSH clients older than v8.1. For more information, see: https://minikube.sigs.k8s.io/docs/handbook/accessing/#access-to-ports-1024-on-windows-requires-root-permission
❗  Access to ports below 1024 may fail on Windows with OpenSSH clients older than v8.1. For more information, see: https://minikube.sigs.k8s.io/docs/handbook/accessing/#access-to-ports-1024-on-windows-requires-root-permission
❗  Access to ports below 1024 may fail on Windows with OpenSSH clients older than v8.1. For more information, see: https://minikube.sigs.k8s.io/docs/handbook/accessing/#access-to-ports-1024-on-windows-requires-root-permission
🏃  Starting tunnel for service ace-dashboard-ingress.
❗  Access to ports below 1024 may fail on Windows with OpenSSH clients older than v8.1. For more information, see: https://minikube.sigs.k8s.io/docs/handbook/accessing/#access-to-ports-1024-on-windows-requires-root-permission
🏃  Starting tunnel for service demo.
🏃  Starting tunnel for service ir01-ing.
🏃  Starting tunnel for service ingress-tls.
```

And then go to https://ace-dashboard.local/home

![img_15.png](img_15.png)

And have a look at the certificate, there you can clearly see the DNS Name provided by the Ingress.

![img_16.png](img_16.png)



### Ingress issue: No Ingress Controller in Minikube

If Minikube has no ingress controller, simply enable it:

```bash
> minikube addons enable ingress
> minikube addons enable ingress-dns
```


## Step 6: Uploadind a bar file
You could upload a bar file via the build in API, as described in this blog 
[Introducing the API for IBM App Connect in containers](https://community.ibm.com/community/user/blogs/matthew-bailey/2024/06/03/app-connect-containers-api) 
by [Matt Bailey](https://community.ibm.com/community/user/people/matthew-bailey), but we've been doing so much with the 
cli, that I'm going to switch it up and use the web UI.

In the dashboard, open up the left hand menu and click on _Bar files_

![img_1.png](img_1.png)

This brings you to an empty page where you import your very first BAR file 

![img_2.png](img_2.png)

Click on the big blue button _Import BAR file_. A new window slides open from the right.

![img_3.png](img_3.png)

Find the bar file you want to import, and click on _Import_ in the bottom left

![img_4.png](img_4.png)

All upload bar files will be listed on this page

![img_5.png](img_5.png)

## Step 7: Creating a runtime
Go back to the main dash
![img_6.png](img_6.png)

Click on deploy integrations
![img_7.png](img_7.png)

Select the quick start integration
![img_8.png](img_8.png)

Select the previously uploaded bar file

We don't have any pre-made configurations, so we can skip this
![img_9.png](img_9.png)

Just use the default values, those should be fine for most situations. Then hit Create
![img_10.png](img_10.png)

And your integration server is starting. If you check your minikube cluster at this point, you will see the following 
object create
- integrationruntime: ir-01-quickstart
- service: ir-01-quickstart-ir
- pod: ir-01-quickstart-ir-f5d5df68c-kpxcx (the pod name can be different, ofcourse)

```powershell
k get integrationruntime
NAME               RESOLVEDVERSION   STATUS   REPLICAS   AVAILABLEREPLICAS   URL                                                          AGE     CUSTOMIMAGES
ir-01-quickstart   13.0.4.1-r1       Ready    1          1                   http://ir-01-quickstart-ir.ace-demo.svc.cluster.local:7800   2m35s   false
```

```powershell
k get svc -l app.kubernetes.io/managed-by=ibm-appconnect
NAME                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
ace-dashboard-dash                ClusterIP   10.109.67.101   <none>        3443/TCP,8300/TCP,8400/TCP   135m
ibm-appconnect-webhook-ace-demo   ClusterIP   10.100.65.199   <none>        443/TCP                      3d1h
ir-01-quickstart-ir               ClusterIP   10.106.17.219   <none>        7800/TCP,7843/TCP,7600/TCP   4m18s
```

```powershell
k get pod -l app.kubernetes.io/managed-by=ibm-appconnect
NAME                                  READY   STATUS    RESTARTS   AGE
ace-dashboard-dash-9668bd46f-8tjfp    2/2     Running   0          136m
ir-01-quickstart-ir-f5d5df68c-kpxcx   1/1     Running   0          5m3s
```

Once everything is running, you should see the runtime inside the dashboard
![img_17.png](img_17.png)

![img_18.png](img_18.png)


### Dashboard issue: runtime not visible
If you have created the runtime, and the kubernetes artifacts are all up and running, but the dashboard is not showing you 
the runtime. But everything else looks fine.

![img_12.png](img_12.png)

The bar file shows that it's deployed

![img_13.png](img_13.png)

The runtime works and is accessible

![img_14.png](img_14.png)

First, it's always a good idea to enable some logging. You can turn up the log level to debug, by patching the dashboard.

```yaml
spec:
  logLevel: debug
```

```powershell
k patch dashboard ace-dashboard --patch-file .\ace\debug-log.yaml --type merge
dashboard.appconnect.ibm.com/ace-dashboard patched
```

Next, wait for the dashboard patch to complete the rollout
```powershell
k -n ace-demo rollout status deployment/ace-dashboard-dash
deployment "ace-dashboard-dash" successfully rolled out
```

Next check the log files for the dashboard pod, this will generate a log of logging, so it is handy to redirect the output to 
a log file
```powershell
k get pods -l release=ace-dashboard
NAME                                 READY   STATUS    RESTARTS   AGE
ace-dashboard-dash-9668bd46f-fprh9   2/2     Running   0          95m

k logs ace-dashboard-dash-5d99db548d-7sr5c -c control-ui > .\ace\dashboard-debug.log
```

If the log begins like this, then debugging has been enabled and you have a lot more information to go through
```text
2025-08-14 15:43:46.249Z: Created logger at level debug
2025-08-14 15:43:46.294Z: Using application name app
2025-08-14 15:43:46.294Z: METRICS_TRANSPORT is not set, so not sending metrics
...
```

As for the issue, 

...

## Step 8: Accessing the runtime

### Quick port forward
The deployed RESTApi is listening on port 7800 (inside the cluster), without https enabled (just to keep it simple). 
Let's start a new kubectl port forward session to make it accessible from my local host. 
```powershell
k port-forward svc/ir-01-quickstart-ir 17800:7800
Forwarding from 127.0.0.1:17800 -> 7800
Forwarding from [::1]:17800 -> 7800
```

And let's test this by calling the API via cli

```powershell
> Invoke-WebRequest "http://127.0.0.1:17800/world/hello" -UseBasicParsing


StatusCode        : 200
StatusDescription : OK
Content           : {"message":"Hello, Foo Bar!"}
RawContent        : HTTP/1.1 200 OK
X-IBM-ACE-Message-Id: (00000097-689DAF54-00000001)
Content-Length: 29
Content-Type: application/json
Date: Thu, 14 Aug 2025 09:41:40 GMT
Server: IBM App Connect Enterprise

{"me...
Forms             :
Headers           : {[X-IBM-ACE-Message-Id, (00000097-689DAF54-00000001)], [Content-Length, 29], [Content-Type, application/json], [Date, Thu, 14 Aug 2025 09:41:40 GMT]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        :
RawContentLength  : 29
```

And whaddayaknow, it works!


### API ingress
If you are not happy with calling your localhost, you can also create an extra Ingress to integration runtime

```yaml
#ir01-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ir01-ing
  namespace: ace-demo
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTP"   # use "HTTPS" if you point to 7843 instead
spec:
  ingressClassName: nginx
  rules:
  - host: ir01.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ir-01-quickstart-ir
            port:
              number: 7800            # or 7843 if you want HTTPS to the pod
```


Apply it
```powershell
k apply -f .\ace\ir01-ingress.yaml
```

Add the hostname to your windows hosts file (from elevated prompt)
```powershell
> Add-Content "$env:SystemRoot\System32\drivers\etc\hosts" "`n127.0.0.1`tir01.local"
```

Let's expose port 443 locally on 12122
```powershell
k -n ingress-nginx port-forward svc/ingress-nginx-controller 12122:443
Forwarding from 127.0.0.1:12122 -> 443
Forwarding from [::1]:12122 -> 443
```

And finally, thest the entire setup by pointing our browser to https://ir01.local:12122/world/hello

![img_11.png](img_11.png)

Success!

## Step 9: Cleanup

We'll clean everthing up in reverse order, and do a check nothing is left. You can start randomly deleting object. But deleting
pods before you delete a set or a deployment will just trigger a new one to be spun up. So let's do it proper.

### Before we begin
First let's have a look at what we do have running, so you can notice the difference after. If you don't care about a proper
cleanup, feel free to delete the entire namespace in one go, nice quick and dirty.

```bash
k delete namespace ace-demo

```


```bash
k get all,ingress,certificates,pvc
Warning: integrationserver.appconnect.ibm.com/v1beta1 is deprecated. Use IntegrationRuntimes
NAME                                      READY   STATUS    RESTARTS        AGE
pod/ace-dashboard-dash-9668bd46f-fprh9    2/2     Running   21 (174m ago)   7d20h
pod/demo-7d8f7758b-7t59j                  1/1     Running   1 (8d ago)      11d
pod/ibm-appconnect-5bc6b7f6b5-96fjb       1/1     Running   663 (8d ago)    13d
pod/ir-01-quickstart-ir-f5d5df68c-kpxcx   1/1     Running   16 (3h ago)     8d

NAME                                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/ace-dashboard-dash                ClusterIP   10.109.67.101   <none>        3443/TCP,8300/TCP,8400/TCP   8d
service/demo                              ClusterIP   10.108.185.89   <none>        80/TCP                       11d
service/ibm-appconnect-webhook-ace-demo   ClusterIP   10.100.65.199   <none>        443/TCP                      11d
service/ir-01-quickstart-ir               ClusterIP   10.106.17.219   <none>        7800/TCP,7843/TCP,7600/TCP   8d

NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ace-dashboard-dash    1/1     1            1           8d
deployment.apps/demo                  1/1     1            1           11d
deployment.apps/ibm-appconnect        1/1     1            1           13d
deployment.apps/ir-01-quickstart-ir   1/1     1            1           8d

NAME                                            DESIRED   CURRENT   READY   AGE
replicaset.apps/ace-dashboard-dash-5d99db548d   0         0         0       7d20h
replicaset.apps/ace-dashboard-dash-9668bd46f    1         1         1       8d
replicaset.apps/demo-7d8f7758b                  1         1         1       11d
replicaset.apps/ibm-appconnect-5bc6b7f6b5       1         1         1       13d
replicaset.apps/ir-01-quickstart-ir-f5d5df68c   1         1         1       8d

NAME                                                            AGE
configuration.appconnect.ibm.com/ir-01-quickstart-ir-adminssl   8d

NAME                                         RESOLVEDVERSION   REPLICAS   CUSTOMIMAGES   STATUS   UI URL   API URL   KEYCLOAK URL   AGE
dashboard.appconnect.ibm.com/ace-dashboard   13.0.4.1-r1       1          false          Ready                                      8d

NAME                                                     RESOLVEDVERSION   STATUS   REPLICAS   AVAILABLEREPLICAS   URL                                                          AGE   CUSTOMIMAGES
integrationruntime.appconnect.ibm.com/ir-01-quickstart   13.0.4.1-r1       Ready    1          1                   http://ir-01-quickstart-ir.ace-demo.svc.cluster.local:7800   8d    false

NAME                                              CLASS   HOSTS                 ADDRESS        PORTS     AGE
ingress.networking.k8s.io/ace-dashboard-ingress   nginx   ace-dashboard.local   192.168.49.2   80, 443   11d
ingress.networking.k8s.io/demo                    nginx   demo.local            192.168.49.2   80        11d
ingress.networking.k8s.io/ir01-ing                nginx   ir01.local            192.168.49.2   80        8d

NAME                                                          READY   SECRET                            AGE
certificate.cert-manager.io/ace-dashboard-tls                 True    ace-dashboard-tls                 23h
certificate.cert-manager.io/ace-dashboardui-cert              True    ace-dashboardui-cert              8d
certificate.cert-manager.io/ibm-appconnect-webhook-ace-demo   True    ibm-appconnect-webhook-ace-demo   11d

NAME                                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/ace-dashboard-content   Bound    pvc-12c7d64e-2dba-46b2-8993-f736fad99e36   5Gi        RWO            standard       <unset>                 8d
```

### Connections

If you have any port-forwarding or `minikube tunnel` running, stop those (ctrl + c).
Check your hosts file and remove the entries for the Dashboard and the Integration Runtime

```properties
# K8S ace

127.0.0.1	ace-dashboard.local

127.0.0.1	ir01.local

# End of section
```

### Ingress

We've defined 2 Ingress objects, one for the Dashboard and one for the Integration Runtime, delete those
```bash
k delete ingress ir01-ing 
ingress.networking.k8s.io "ir01-ing" deleted

k delete ingress ace-dashboard-ingress
ingress.networking.k8s.io "ace-dashboard-ingress" deleted
```

### Runtimes and Dashboard

Deleting the Integration Runtimes and Dashboard will also trigger the Operator to cleanup the related Deployment and Service.

```bash
kubectl delete integrationruntime --all --wait=true
integrationruntime.appconnect.ibm.com "ir-01-quickstart" deleted
```

```bash
kubectl delete dashboard ace-dashboard --wait=true
dashboard.appconnect.ibm.com "ace-dashboard" deleted
```

### Certificates

For a full cleanup, you might also want to delete the certificate we setup.

```bash
kubectl delete certificate --all
```

### Storage

Delete our volume claim

```bash
k delete pvc ace-dashboard-content
persistentvolumeclaim "ace-dashboard-content" deleted
```


### Operator

And finally, the only thing that's left, the Operator itself

```bash
> helm uninstall ibm-appconnect --wait
release "ibm-appconnect" uninstalled
```

Which brings the content of my namespace down to
```bash
k get all,ingress,certificates,pvc
NAME                                  READY   STATUS    RESTARTS       AGE
pod/demo-7d8f7758b-7t59j              1/1     Running   1 (8d ago)     11d

NAME                                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/demo                              ClusterIP   10.108.185.89   <none>        80/TCP    11d

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/demo             1/1     1            1           11d

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/demo-7d8f7758b              1         1         1       11d

NAME                                              CLASS   HOSTS                 ADDRESS        PORTS     AGE
ingress.networking.k8s.io/demo                    nginx   demo.local            192.168.49.2   80        11d
```
No more ACE.

---

For more integration tips and tricks, visit Integration Designers and check out our other blog posts.

---

## References

* [IBM ACE Docs](https://www.ibm.com/docs/en/app-connect/13.0.x)
* [ACE Operator on ArtifactHub](https://artifacthub.io/packages/helm/ibm-helm/ibm-appconnect-operator)
* [Getting started with Minikube](https://minikube.sigs.k8s.io/docs/start/)
* [Configuration properties in the values.yaml file for deploying the IBM App Connect Operator](https://www.ibm.com/docs/en/app-connect/13.0.x?topic=operator-configuration-properties-in-valuesyaml-file)
* [Introducing the API for IBM App Connect in containers](https://community.ibm.com/community/user/blogs/matthew-bailey/2024/06/03/app-connect-containers-api)

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)

\#IBMChampion
\#AppConnectEnterprise(ACE)
\#k8s
\#AceOperator
\#AceDashboard
\#AceRuntime
\#ACECC
