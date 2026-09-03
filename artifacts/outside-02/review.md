# Outside review 02 — 2026-09-03

Unassociated pass against the four tethered repos. Source below.
This file is the disposition so the next pass can tone out what
the tree already holds.

Next paste is `reports/outside/03` and `artifacts/outside-03`.

## Disposition

Already in the tree. Not re-minted.

| finding | already here |
|---|---|
| Godot is the wrong engine; web export is the product and it is parked | Ruled. `reports/outside/01/godot-vs-web`, state done. Godot first; web follows. |
| name vs folder path never checked; rename lies | Ruled. `reports/outside/01/identity-unreconciled`, state done. `isPartOf` matches folder position. Name is free text. The pass is stale: it still describes the pre-ruling name rule. |
| Referential integrity repo-scoped; dangling is ERROR; cross-repo only prose | Ruled. `reports/outside/01/cross-repo-pointers`, state done. Miss is WARNING. Form is `repo:GUID`. The pass is stale: it still describes dangling as ERROR. |
| Collapse to one repo | Locked. `four-repo`, option `four-tethered` chosen. |
| Delete PROCESS.md; ceremony vs shipping | Partly `reports/outside/01/planning-laps` (accepted: count the folders). The reward-function claim is new; minted this pass as `progress-simulator`. |
| Unlimited planning laps / spec machine | `reports/outside/01/planning-laps`. |
| No pixels yet; renderer does not exist | Live plan: `plans/render-turn-one`. The new crack is that PROCESS.md never requires the loop to finish. |
| Shuttle not minted; fifth repo referenced | `plans/shuttle`. `reports/outside/01/capture-cost` stays open, owned by shuttle. |
| Day-granularity dates | Locked. VALIDATE.md hard stop 11. UTC calendar day. Not a defect. |
| measurement close to useless at day resolution | Already OPEN in VALIDATE.md. No node minted. |
| One node shape; never forbid; props as hatch | Locked. `plans/warp-v1/one-node-shape`. The new crack is props swallowing real usage. |
| `ok` certifies little | `reports/outside/01/ok-means-little`. |
| Python is the reference validator | VALIDATE.md. Strength, not a gap. |
| Canonical key order / `--check` | VALIDATE.md. Strength, not a gap. |
| Filesystem-as-tree | By design. Strength, not a gap. |

Identified, not yet a node. Minted this pass.

| finding | node | type |
|---|---|---|
| Render loop has no completion criterion; nothing forces a renderer to exist | `reports/outside/02/render-loop-no-end` | issue |
| Cards and rulings produce motion without shipped capability | `reports/outside/02/progress-simulator` | risk |
| No user, competitor, or job to be done; demo is a museum exhibit | `reports/outside/02/no-job-to-be-done` | issue |
| Schema and first render target have not met a project the author is not running | `reports/outside/02/self-validated` | risk |
| `threads[]` and subfolders are two legal hierarchies | `reports/outside/02/threads-fork` | issue |
| Real usage routes through `props`; the strict schema becomes decorative | `reports/outside/02/props-becomes-schema` | risk |
| `state` is not required | `reports/outside/02/state-optional` | issue |
| `$id` is the relative identifier `thread.schema.json` | `reports/outside/02/schema-id-relative` | issue |

A later chat binds to one child of `reports/outside/02`.

## Source

What it is

A project-record format, plus a renderer that doesn't exist yet.

loom-warp is the only repo with working code: a JSON Schema defining a single node shape with twelve types — project, plan, report, scopeItem, workItem, artifact, issue, risk, measurement, operation, decision, option — plus a ~194-line Python validator and a PowerShell port. The README designates Python as the reference validator and the PowerShell/Markdown versions as conformance targets, not peers. Nodes live as thread.json files, one per folder, and the directory tree is the hierarchy.

loom is a signpost that holds no code — its own tree of thread.json nodes tracking the construction of Loom itself. loom-weave is a base render contract with no renderer code in the repo — .gitignore and README, two files, two commits. loom-weave-godot is the first weave, also with no renderer code yet, containing a slot spec and a list of owed artifacts.

Combined: 13 commits, 0 stars, 0 forks, 0 watchers, 0 outside contributors, all dated today. The strategic question isn't how to kill it. It's whether it survives contact with its own second week.

The core problem

The governance apparatus is an order of magnitude heavier than the product. PROCESS.md defines three concurrent loops, a five-stage outer "cold open," a plan gate with a planning seat, a checking seat, and an owner, unlimited planning laps against a single execution pass, and a rule that every README opens with a Just did / Next / Context card that must change in the same commit as the session file. That's a change-control regime for a codebase with one real script in it.

This isn't just overhead — it's a progress simulator. Maintaining cards, minting decision nodes, and recording rulings produces commits, produces a sense of motion, and produces zero shipped capability. The author has built a machine that rewards documenting work over doing it, and the repos are the evidence: the process is v1.0.0 and the product is a folder named self-render.

Where it dies

The render loop has no completion criterion, by design. The schema loop is triggered change control; the render loop is continuous PDCA with no terminal date. So the loop that's finished is the one that had a defined end, and the loop that has to produce the actual product has explicitly disclaimed having one. Nothing in the process forces a renderer to exist. That's the failure mode, and it's written into the constitution.

Godot is the wrong engine for this buyer. Anyone who wants project status wants a URL they can send to someone. Godot gets you a binary, a WASM export toolchain, no linking, no embedding in existing tooling, and a near-empty talent pool for PM software. The README already concedes the Apollo read-only web export stays owed, later. The web export is the product. It's parked.

The demo strategy is a museum exhibit. An Apollo galaxy and an Enron galaxy with RICE at the core, a seven-step intro on a 45-second budget. Famous disasters rendered as data structures gets you "cool" at a conference and zero procurement. There is no sentence anywhere in these four repos naming a user, a competitor, or a job to be done.

Everything is validated against itself. The first render target is a status view of Loom's own tree. The schema has never met a project the author isn't running. No adversarial data, no scale, no second opinion.

Concrete schema weaknesses

These are where a technical attack lands:

name is specified as the folder path from repo root, flattened with hyphens — identity duplicated between filesystem location and a field, and validate.py never checks that they agree. Rename a folder and the record silently lies.

The schema defines a threads array of child nodes while noting that on disk children are subfolders, not this array. Two legal representations of the same hierarchy on day one, and the validator's decision/option check has to handle both. That fork will never close.

Referential integrity is repo-scoped: pointers that don't resolve within the repo are errors. But the architecture is deliberately multi-repo with cross-repo references. The link graph is broken precisely at the seams the whole design rests on. Cross-repo pointers can only be prose or file paths, which means they're unvalidated.

additionalProperties: false plus a frozen 12-value type enum means every new concept needs a schema bump under triggered change control — while props sits there as an untyped name/value escape hatch. Real usage will route everything through props and the strict schema becomes decorative.

state isn't required on any node type. Optional status, in a status tool.

Dates are day-granularity format: date only. No timestamps, no ordering, no timezone. measurement as a type is close to useless at that resolution.

"$id": "thread.schema.json" is a relative identifier. For a format whose entire thesis is portability, nothing downstream can resolve it.

What's actually good

Worth knowing, because a critique that finds nothing competent is a critique you can't trust: filesystem-as-tree is a genuinely nice call for git-native records. Designating one implementation as authoritative over its ports is discipline most people skip. Canonical key ordering with a --check CI gate is real engineering. The person can build.

That's what makes this diagnosis specific rather than general: the failure isn't capability, it's that the process has become the product. Four repos, a promote-then-comply protocol, a fifth repo referenced but not created — all invented to coordinate a codebase that fits in one directory. The split created the coordination problem that the ceremony then solves.

If you're competing: ship a web view of typed project records that someone can send in Slack, and this never reaches a user. If you're advising the author: collapse to one repo, delete PROCESS.md, and render something in a browser this week.
