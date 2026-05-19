# Moved to containers

## customer 1

### build environment
We chose a baked approach with our own custom build and test images, based on the ubi-minimal and we chose the operator
aproach for our actual runtimes.
see D:\Projects\Luminus\GIT\ace-docker\Dockerfile

The main reason is because this worked for us. We had some scripts that we needed at build, test and run phase, and 
instead of just creating seperate images, or not being sure what we were running, we created one image to use for our 
build, test and actual runtime. It would have been easier to setup a runner, but then you need to maintain that one as 
well, and then it could possibel be treated as a pet again, nobody wants that.

At that moment in time, we decided that maintaining this image and these scripts all together was the easiest way of
mainting quality and stability. Would I do this agian? I might. There is an argument to be made for a on-prem configured 
dedicated runner, but you need to maintain it. So i think it depend on what you feel more comfortable using. Custom images
you need to validate in docker or a dedicated runner you can login to.
Obviously a dedicated runner can be chosen if you want to start your pipeline builds quicker. But that is anoter requirement.

### runtime environment
For the runtime environment we chose the native IntegrationRuntime operator approach. Just keep it simple, supply your bar
files and your config and let the operator do the rest

### credentials
Vault, shipped as config map
Credentials for flows loaded into container environment with startup scripts (I think this was before the java compute 
dynamic credentials, or before we know about those)

### bar file storage
We used gitlab artifact storage of the pipeline, for the simple reason that it allowed for basic auth, which is what the
operator requires to fetch your bar files. It is actually a token discuised as a basic auth request. Not all artifact repos
support that and the ones that do sometimes come with an additional price tag.
Why not the dashboard? Because it automatically performs rolling updates (sometimes a good thing, sometimes not), and it
can't handle versioning. If you wanted to do that properly, you would need an external repo that syncs to the dashboard, 
that way you get the very best out of both worlds. Except that makes it difficult for rollbacks.

### Config
For config we had the typical overrides
- the runtime itself
- vault (work dir override )   
- vault key
- a config file to specify which secrets were required at container runtime level
- server.conf.yaml override per app

and some shared stuff
- secret for the package registry
- keystore and keystore pass

And obviously
- the bar file for the app
- the bar files for all the required libs
- 
### pipeline
the pipeline brought everythign together. This is the bit that can get (and should) be complex. As long as the result
is simple and usable. Developers only needed to create the code, and some of the config, the pipelien would build all the
operator required config, devs never need to know how to build those specific config files. Everything was hashed, zipped, 
created, configured, ... in the pipeline. And build, uploaded and tagged allong with the bar file for that app.
One example is that the pipline would investigate all projects, auto resolve the dependencies, auto resolve those dependcies
untill everything was found and included in the bar list.


## customer 2
licencsing is a big issue at times, we have a customer where we could not get licensign done on pvu, but we got a worker
node licenced and used labels to only spin up the ace containers on that workernode. That does give issues when doing a
bulk restart


## customer 3
Again licecnsing. We are looking into moving to containers, currently we are also implementing the adapter patterns
so we are creating a LOT of integration servers, which is fine on a node managed system, but on cloud this coms with
the extra cost of licensing, even with 0.1 vcpu, you need to have the capacity to create new containers. 

## murmerings
startup resource contention is solved (or at least mitigated) with dynamic startup scaling, btu the runtime licencsing is
still required, that is where licensing one or a ocuple of nodes becomes interesting.



