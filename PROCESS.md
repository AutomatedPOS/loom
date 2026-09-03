# Process

Three loops run at once. This file is where they are written down so
that "what is next" does not need a person. Text mode; no diagrams.

## Cold open — the outer loop

```
S1 -> S2 Opening -> S3 Candidate shapes -> S4 Cognitive apprenticeship -> S5 Reflect
   closed      closed        closed, locked          open, in progress              not started
```

Run 01 (status reporting) sits at S4. Loom is the thing being built
inside S4. S5 has not started.

## Plan gate — how a build starts

```
planning seat declares ready -> checking seat agrees -> owner goes -> one execution pass
|<----------- planning laps, unlimited, nothing built ----------->|   single pass
```

Three thumbs, in that order. Open questions are not guessed: if the
machine seats cannot settle one, work on that branch stops and the
question is written down for the owner to rule on.

## Product loops — locked in S3

```
schema loop (loom-warp)              render loop (loom-weave, loom-weave-<engine>)
triggered change control             continuous PDCA, loose on purpose
            \                              /
             \--- cross only on a block --/
```

The schema loop is configuration change control (NIST SP 800-128
shape): triggered, not continuous. The render loop is plan, do,
check, act: continuous, no terminal date. They cross only when one
blocks the other.

## Standing loops

### Promote to common, then comply

Ruled 2026-09-03. Recorded as `decisions/base-render-class`.

Work happens in `loom-weave-godot`. When a shape proves out there, it
is promoted up into `loom-weave` as the common contract. Godot then
conforms to the thing it promoted. Nothing is authored into the
common pack in advance.

### Card and session move together

Every repo README opens with a card: **Just did**, **Next**,
**Context**. Context is the operation being executed and where its
node sits; where the repo has a tree, it names the live node, so the
card and the tree cannot disagree.

The card changes in the same commit as the session file's `## Now`.
Sessions are per repo, in `sessions/`, gitignored. A chat binds to
the repo it opens in.
