---
title: Ignoring fields in ACE integration testing: a guide
description: Many users are well-acquainted with the basic integration testing capabilities of the ACE framework, but its features for ignoring specific fields during testin.
reading_time: 4 min
date: 2024-08-06
---

# Ignoring fields in ACE integration testing: a guide

Many users are well-acquainted with the basic integration testing capabilities of the ACE framework, but its features for ignoring specific fields during testing often go unnoticed. In this post, we'll delve into how to use these capabilities to simplify your testing process and avoid failures caused by dynamic data such as UUIDs and timestamps.

> If you don’t feel like reading the entire test setup and just want to get to the sweet part—I got you.

![img.png](img.png)

## Setting up the test environment

Let’s start with a simple setup. Our test flow receives an HTTP call, processes the data, and outputs results. It maps, transforms, and adds fields. Nothing fancy, but enough to demonstrate how this works in practice.

![img_1.png](img_1.png)

![img_2.png](img_2.png)

## Creating and running the test

Let’s create the test case:

1. Start the Flow Exerciser.

![img_3.png](img_3.png)
![img_4.png](img_4.png)


2. Send a test message through the flow.  

![img_5.png](img_5.png)

3. Check the response—make sure there’s no error, and that it looks correct.

![img_6.png](img_6.png)

4. Right-click on the node you want to test and select **Create Test Case**.

![img_7.png](img_7.png)

For this blog, we’ll only focus on the message body. Accept the defaults when creating the test case.

5. Click **Finish**, and you’ll see the newly created test case—for example, `FeedApplication_Test`.

![img_8.png](img_8.png)

6. Right-click the test application and select **Run Test Project**.

![img_9.png](img_9.png)
![img_10.png](img_10.png)
![img_11.png](img_11.png)

And we have a failure. Who would have expected that 😉

## Handling test failures

In our case, the test fails because of a **UUID field** that changes on every run. If you check the failure details, you'll see this:

![img_12.png](img_12.png)
![img_13.png](img_13.png)

Sure enough, the field `/Message/JSON/Data/requestSession` is a UUID.

![img_14.png](img_14.png)
![img_15.png](img_15.png)

## Ignoring dynamic fields

To fix this, we need to tell the test to ignore that specific field.

In your Java test code, go to the assert line (mine’s on line 88). We’ll use the `ignorePath()` method like this:

![img_16.png](img_16.png)

```java
assertThat(actualMessageAssembly.equalsMessage(expectedMessageAssembly)
  .ignorePath("/Message/JSON/Data/requestSession", false));
```

![img_17.png](img_17.png)

### `ignorePath()` takes:
- The path you want to ignore
- A boolean: `true` if you want to ignore all subpaths too

Save and rerun the test.

![img_18.png](img_18.png)

## Additional challenges: timestamps

Now that the UUID issue is handled, we hit a **TIMESTAMP** mismatch.

Again, you can either ignore this specific field or go broader.

To ignore **all** timestamps, just chain another method:

```java
assertThat(actualMessageAssembly.equalsMessage(expectedMessageAssembly)
  .ignorePath("/Message/JSON/Data/requestSession", false)
  .ignoreTimeStamps());
```

![img_19.png](img_19.png)

![img_20.png](img_20.png)

Almost like I planned it.

You can also ignore DateTime fields using `.ignoreDateTime()` the same way.

![img_21.png](img_21.png)

## Conclusion

The ACE Integration Test framework supports three useful ignore methods:

- `ignoreDateTime()`: Ignores DATE and TIME fields
- `ignoreTimeStamps()`: Ignores TIMESTAMP fields
- `ignorePath()`: Ignores specific paths (with or without subpaths)

Use them to clean up noisy test failures caused by UUIDs, timestamps, or any other runtime-generated fields.

---

## Resources

- [GitHub: ACE test cases with ignore logic](https://github.com/matthiasblomme/Ace_test_cases/tree/features/add-unit-test-test-case/UnitTestIgnoreFields)
- [IBM Docs: Developing integration tests](https://www.ibm.com/docs/en/app-connect/12.0?topic=solutions-developing-integration-tests)
- [IBM Docs: Using ACE Toolkit for tests](https://www.ibm.com/docs/en/app-connect/12.0?topic=dit-developing-integration-tests-by-using-app-connect-enterprise-toolkit)
- [IBM Docs: Creating test cases from recorded messages](https://www.ibm.com/docs/en/app-connect/12.0?topic=ditbuacet-creating-test-case-message-flow-node-using-recorded-messages)

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)
