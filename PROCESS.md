# Process

Three loops run at once. This file is where they are written down so
that "what is next" does not need a person. Text mode; no diagrams.

## Cold open — the outer loop

```
S1 Harold -> S2 Opening -> S3 Candidate shapes -> S4 Cognitive apprenticeship -> S5 Reflect
   closed      closed        closed, locked          open, in progress              not started
```

Run 01 (status reporting) sits at S4. Loom is the thing being built
inside S4. S5 has not started.

## Plan gate — how a build starts

The kind of change picks the ceremony. Ruled 2026-09-03.

```
path, type, state, parent   ->  three thumbs
prose                       ->  owner goes
both                        ->  three thumbs
```

Structural changes are expensive to unwind, because other work gets
written against them. Prose is cheap: rewrite it. A structural change
does not become prose because the diff is small.

Three thumbs is:

```
planning seat declares ready -> checking seat agrees -> owner goes -> one execution pass
|<----------- planning laps, unlimited, nothing built ----------->|   single pass
```

In that order. Open questions are not guessed: if the machine seats
cannot settle one, work on that branch stops and the question is
written down for the owner to rule on.

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

### The card is a view

Ruled 2026-09-03. Landed in loom-warp v1.1.0.

Every repo README opens with a card: **Just did**, **Next**, **Waiting
on**. Those are three fields on a node — `justDid`, `next`,
`waitingOn` — written by the operation at close-out. `card.py` renders
the README block between `<!-- card:start -->` and `<!-- card:end -->`.

Nobody authors a card by hand. The earlier version of this rule said
the card changes in the same commit as the session file's `## Now`,
which is a rule a person has to remember. This one is a check:
`card.py --check` fails when a README disagrees with its node.

Close-out is the end of a **turn**, not the end of an operation.
Operations do not end.

A repo that has no tree gains a standalone operation root: type
`operation`, `isPartOf` empty, same shape as `loom-weave-godot`.
`card.py` generates the README card from that node. Walkers skip
`tests/` so fixture trees are not the repo tree. Ruled 2026-09-03.
Closes the OPEN on which node carries close-out in a repo with no
tree. `loom-warp` and `loom-weave` now have one. This repo's root
is the same shape.

`loom-apollo-13` keeps a hand card on purpose: its root is a finished
1970 record, and live status does not get written onto a closed node.

Sessions are per repo, in `sessions/`, gitignored. A chat binds to the
repo it opens in.
