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

### README cards are gone

Ruled 2026-09-03 as a generated view of `justDid`, `next`,
`waitingOn`. Killed the same day: the README card confused both
seats, and once the weave is running it is unused.

Those three fields stay on the node. Close-out is still the end of a
**turn**, not the end of an operation. Operations do not end. Status
is read from the tree and the weave, not from a README block.

Do not put a Just did / Next / Waiting on heading in a README.
`card.py` is deleted. Do not bring it back.

Living repos carry a root `thread.json`. `loom-apollo-13` writes no
live status onto its finished 1970 root.

Sessions are per repo, in `sessions/`, gitignored. A chat binds to the
repo it opens in.
