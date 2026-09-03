# Outside review 01 — 2026-09-03

Unassociated pass against the four tethered repos. Source below.
This file is the disposition so the next pass can tone out what
the tree already holds.

Next paste is `reports/outside/02` and `artifacts/outside-02`.

## Disposition

Already in the tree. Not re-minted.

| finding | already here |
|---|---|
| No pixels yet; governance ahead of a renderer | `plans/render-turn-one` (open). `plans/weave` (open). README Next. |
| Validator never forbids; one node shape | Locked. `plans/warp-v1/one-node-shape`. VALIDATE.md hard stop 2. Brief r2: no forbidden fields. |
| Four tethered repos | `four-repo`, option `four-tethered` chosen. |
| Python is the reference validator | VALIDATE.md. Brief r2. |
| abandoned / superseded as first-class states | Schema. Not a gap. |
| props as OSCAL-shaped escape hatch | Schema. Not a gap. |
| sourceVerified | Schema. Not a gap. |
| NIST SP 800-128 shape on the schema loop | PROCESS.md product loops. |
| loom-weave empty; warp v1 frozen as a triggered loop | Known. Schema loop is triggered, not continuous. Weave plan is open. |
| Execution ran on thumb 1 alone | `plans/process-cards/pain-32`. |
| Ship a read-only view of this tree | Already the live plan: `plans/render-turn-one`. Vehicle (Godot vs web) is the new issue. |

Identified, not yet a node. Minted this pass so there is something to answer.

| finding | node | type |
|---|---|---|
| name / isPartOf / folder nesting never reconciled | `reports/outside/01/identity-unreconciled` | issue |
| Cross-repo pointers still OPEN; interesting links are English in cards | `reports/outside/01/cross-repo-pointers` | issue |
| Exactly-one-chosen lock cannot hold a live decision | `reports/outside/01/live-decision` | issue |
| Capture cost vs a text box | `reports/outside/01/capture-cost` | issue |
| No glossary | `reports/outside/01/glossary` | issue |
| No license | `reports/outside/01/license` | issue |
| Godot as first weave vs a Tuesday-morning web view | `reports/outside/01/godot-vs-web` | issue |
| Green validator, little meaning, GRC reader treats it as certified | `reports/outside/01/ok-means-little` | risk |
| Planning laps outrun execution | `reports/outside/01/planning-laps` | risk |

`cross-repo-pointers` was already named in `four-repo` consequences ("Cross-repo pointers remain OPEN"). It was not a node. It is now.

`live-decision` challenges a lock (VALIDATE.md ERROR 4, `plans/warp-v1/chose-is-prose`). It is not a claim that the validator is buggy.

`ok-means-little` does not reopen the never-forbid lock. It is the audience mismatch of that lock.

`planning-laps` is broader than pain-32.

A later chat binds to one child of `reports/outside/01`.

## Source

What they're building

A project-status format, not an app. The unit is thread.json — one file per folder, folder tree is the index. Twelve node types (project, plan, report, scopeItem, workItem, artifact, issue, risk, measurement, operation, decision, option), GUID identity, state machine (open/active/done/abandoned/superseded/chosen), typed cross-links (supersedes, blockedBy, realizedAs, mitigatedBy, voidedPlan), plan-vs-actual dates, and OSCAL-style props as an extension hatch.

The intent is clearly compliance/GRC. NIST SP 800-128 change control is cited by name, props is explicitly OSCAL-shaped, there's a sourceVerified boolean, and the account's other repo is STIG checklist automation in PowerShell. The pitch, unstated but obvious: your project history becomes a validated, machine-checkable artifact instead of a deck someone wrote on Thursday. loom-weave-godot is meant to render that as a spatial/cinematic view — "galaxies," a 45-second cold open, Apollo 13 and Enron as demo trees.

Where it fails

The product doesn't exist. Thirteen commits across four repos. loom-weave is a README and a .gitignore. loom-weave-godot contains no Godot code and says so twice. The only running code is ~400 lines of validator in loom-warp. Everything else is process about the process — PROCESS.md, README "cards," a formal decision node about where the base render class should live. They've built governance for a thing that has never rendered a pixel.

The validator is weaker than it looks. The schema is conditional-required-only — it never forbids. additionalProperties: false blocks typos, but every known field is legal on every type. You can put decidedDate, chose, and consequences on a workItem and it passes green. For a compliance-adjacent tool, a validator that says "ok" while meaning very little is the worst possible failure mode, and that's what this is today.

Three identities per node, zero reconciliation. name is defined as the folder path flattened with hyphens. isPartOf is a GUID. Actual parentage is folder nesting. Nothing checks that any of the three agree. Rename a folder and name silently lies. Point isPartOf at a node in a different branch and the build stays green.

This is the big one — integrity stops at the repo boundary. validate.py hard-errors when any pointer names a GUID outside the current repo. But the architecture is deliberately multi-repo, versioned independently. So every cross-repo relationship — the interesting ones — is expressed as English prose in a README card: "Node: plans/warp-v1 in loom." Unvalidated, un-GUID'd, un-linkable. The one thing the format exists to do fails at exactly the seam the architecture creates.

The decision rule can't represent a live decision. "Exactly one chosen option beneath it" means a decision with three candidates and nothing settled yet is a validation error. The format punishes you for writing a decision down while it's still a decision. That's precisely when you'd want to.

Capture cost is the whole game and they lose it. To log one thing: make a folder, mint a GUID, choose among 12 types, satisfy conditional requireds, run format_thread.py --write to pass the CI gate. Compare to typing a line in a text box. Status reporting lives or dies on friction at entry, and this is worse than a Jira ticket.

Godot is a bad bet for this audience. It buys spatial rendering and costs you web export (already deferred, "owed, later"), embeddability, text selection, accessibility, and any contributor pool that overlaps with GRC people. The 45-second cold open tells you what it's really optimized for: impressing a room. The cinematic version and the Tuesday-morning-useful version are different products, and the cinematic one usually eats the other.

Process weight vs. team size. "Planning seat declares ready → checking seat agrees → owner goes → one execution pass," with unlimited planning laps and a single execution pass. One person plus LLM agents running a three-approval gate on themselves. It is a spec-generating machine. The evidence: four artifacts owed, one delivered, one already parked because the plan moved underneath it.

Also: no license, no glossary, zero stars/forks. Warp, weave, shuttle, thread, card, seat, lap, minted, galaxy, probe, cold open — every term is a metaphor with no definition anywhere. That's a moat around the author, not around competitors.

What's actually strong — don't underestimate these

Be honest about this or you'll misjudge the fight:

The compliance angle is real. OSCAL props + 800-128 + sourceVerified is a genuine niche where a validated project history has regulatory value, not just aesthetic value. Nobody serious owns that space.
abandoned / superseded / supersededBecause as first-class states. Someone who has actually done program reporting wrote that. The valuable information in a project is what got dropped and why, and every mainstream PM tool deletes it.
props as an escape hatch is the right call — domains extend without schema churn.
"Python wins" as a conflict rule for multiple validator implementations is correct discipline.
Where I'd hit it

They have deferred the entire user-visible value to a renderer that doesn't exist, behind a process that generates plans faster than passes. So:

Ship a read-only web view of a validated tree in a weekend. That's their deferred value, and it's a weekend of work in plain HTML.
One-command capture. x add issue "thing" — folder, GUID, requireds, formatting, all of it.
Make cross-project links first-class and validated. That's their structural hole and it's load-bearing.
Use boring words. Issue, decision, plan.

The realistic outcome for them without a course correction: loom-warp v1 stays frozen and correct, loom-weave stays empty, and the render loop keeps producing specs. The compliance niche is the only place they're dangerous, and they're not currently aimed at it — they're aimed at a demo.
