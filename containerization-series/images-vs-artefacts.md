## Containerizing IBM ACE: A Blog Series - Images vs Artifacts

When people start talking about container images for IBM ACE, you’ll often hear the phrase *“bake vs fry”*. Or at least you should. It sounds a bit like we’re cooking eggs, but it’s actually a handy way to describe two different approaches to building (and shipping) your runtimes.

### Bake

The **bake** approach is about building a custom image that already has your BAR files and everything else you need, baked in (hence the name). The runtime and the applications are packaged together into a self-contained image, ready to deploy.

* The upside:

    * fast startup times and consistency
    * the exact same image runs in dev, test, and production
    * 100% tailored to your needs
    * tests are run on the actual production image (if you use a proper CI/CD pipeline)
* The downside:

    * you need to rebuild and retest the image every time something changes (runtime or applications)
    * a lot of possible variance on your runtimes, some containers run with version a.b.c, and others with x.y.z
    * big artifacts (docker images) to ship and store

Baking is putting everything together, mixing it well and throwing it into the oven. Once done, you can enjoy it immediately or save it for later.

### Fry

The **fry** method is the opposite. Here you start with a clean ACE runtime image (possibly supplied by IBM), and only add your BAR files and configurations at deployment time.

* The upside:

    * one standard runtime image you can reuse everywhere, maintained by the vendor
    * small artifacts (bar files)
    * more consistent runtime versions
    * the exact same artifact runs in all pillars
* The downside:

    * your build/test and runtime environments might vary.
    * your CI/CD pipeline tests your artifact, not your runtime
    * there can be runtime differences between pillars
    * less control over the runtime

Frying is adding salt, pepper, and all your dependencies last minute into your pan, and eating it right there and then.

### What to choose

With the definitions out of the way, let's look at what it means.

Straight off the bat, baking is more initial work.

* You need to choose a base image
* Maybe install ACE and/or MQ
* Maybe install some testing tools like Bruno
* Build and compile your code
* Deploy it inside the newly created image
* Package the entire thing up
* Ship it out

Whereas frying is limited to a subset of these actions. Just build and package your code and you’re done.

Now is it always that simple or straightforward? No, it’s not.

I actually like both. I like the all-in-one package that a bake offers and I like the small footprint of frying a simple artifact. Both have a use, depending on your needs.

For instance, I like baking a test image to use in your pipeline. An image that contains all testing tools and dependencies I could possibly need, very handy to validate whatever type of integration you are building. But for the actual deliverables, I prefer ad-hoc frying. Shipping small artifacts is a lot simpler, and the artifacts are what it’s all about, right?

Again, no ready-made solutions here, just reflections on the trade-offs.

### Considerations while baking

When baking, you need to choose what base image you are going to be using. Will it be a vendor-supplied one, like ACE Certified Containers? Or are you starting with a minimal Linux flavor and taking even more control over your runtime? The world (of containers) is your oyster, choose wisely.

Whatever you decide to do, IBM supports ACE both in ACEcc and in custom installed containers, so at least that won’t be a deciding factor.


### Pets and Cattle

Even here, the comparison between pets and cattle feels appropriate. Not only can that term be used to describe how you manages your runtimes, but it also fits (in my opinion) with how you build your runtime.
Think about it. If you build larger images, you are basically building small servers. You choose a base image, you install some software and you put your code in. That sounds an awfull lot like managing a server, pets.
Now, if you only build small artefacts, that can be set loose in the open pasture that is your runtime, then it feels more like you aren't mirco managing it, so cattle (and not only because of my aptly chosen metaphors).

### Some Takeaways

Here's what I've learned so far

* When baking, start with IBM’s pre-built ACE images so you know you’re on solid ground.
* Use *fry* when you want a bit more flexibility
* Use *bake* when you need more predictability or special setups.
* Always keep security in mind: smaller base images, multi-stage builds, and regular scanning are your friends.

### Quick Comparison

| Aspect             | Bake                               | Fry                                      |
| ------------------ | ---------------------------------- | ---------------------------------------- |
| What it contains   | Runtime + BARs bundled together    | Bars and Config as separate deliverables |
| Startup time       | Fast, self-contained image         | Slower (needs BAR injection)             |
| Flexibility        | Low – changes require rebuild      | High – one runtime reused with many BARs |
| Artifact size      | Large (Docker images)              | Small (BAR files and/or config)          |
| Consistency        | Same image across all environments | Same artifact across environments        |
| Maintenance effort | Higher (rebuild for every change)  | Lower (fewer image rebuilds)             |

## Conclusion

This is a highly debatable topic, and everyone has their own view of what the best approach is. Moral of the story: there is no single right answer. It depends on what you are comfortable with, the experience you have available in your organization, and the CI/CD options you have in place.

Both approaches can work and work well. The important thing is to pick the one that fits your context best.

Personally, I keep switching between the two depending on what I’m building and who I’m building it for — and that’s fine. Hopefully this gives you some ideas to chew on for your own setup.
****