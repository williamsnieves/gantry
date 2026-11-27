# Relay

A service that receives events from our systems and delivers them as webhooks to the URLs our customers register. Go, standard library where it is enough, SQLite.

Stage 1 is built **without** the harness, with the bare prompt. The harness is installed before stage 2.

Give the requests in order, one per session, text unchanged.

## Stage 1: the product, no harness

**C1**

> Set up the project: a Go HTTP service with SQLite and a health endpoint. Tests, vet and build each run with one command. Write a README that says how to start it and how to run them.

**C2**

> Customers register subscriptions: a URL and the event types they want. Our systems post events to the service, and it delivers each event to every subscription that wants that type.

**C3**

> Sign every delivery so the receiver can check it really comes from us.

**C4**

> When a delivery fails, retry it, waiting longer each time. After enough failures give up, and keep those where we can look at them and send them again.

Tag `bare-done`. Evaluate stage 1. Install the harness, run `gantry doctor`, run `/harness-onboard`, commit, tag `stage-1`.

## Stage 2: changing it, with the harness

**C5**

> A subscription can be paused and resumed. Nothing is lost while it is paused.

**C6**

> A customer pointed their webhook at one of our internal admin addresses. Make sure that can't do any damage.

**C7**

> Add a Dockerfile to run the service, and a CI workflow that runs the checks on every pull request.

**C8**

> Receivers complain that they get the same event more than once. Give them a way to recognise a duplicate, and stop creating duplicates ourselves when one of our systems retries a post.

Tag `stage-2`. Evaluate.
