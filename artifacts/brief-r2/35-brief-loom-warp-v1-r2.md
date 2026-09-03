# loom-warp v1 schema + validators
## Revision 2 — supersedes file 35

Source of truth: packet files 24, 30, 34, and the
sitting-10 walk (file 37). Everything below is locked unless marked
OPEN. Do not extrapolate past it.

This revision supersedes file 35 in three places: the type count, the
date conditionals, and the decided-date field. File 35's remaining
content stands unchanged.

## What to build

Repo `loom-warp`. Three things:

1. `thread.schema.json` — JSON Schema for one node type.
2. Validators in Python and PowerShell.
3. `VALIDATE.md` — the same rules written so an LLM can check its own
   output against them without running code.

Conventional Commits from commit one. SemVer.

## Hard constraints — do not violate

- **One file type. One node shape. No new file kinds, ever.**
- **JSON. Not YAML.**
- **Upward pointers only.** No node lists its children. No exceptions.
- **Nothing is ever deleted.** Superseded or abandoned, file stays.
- **Type never changes after creation. State does.**
- **Flat type hierarchy for v1.** Base node plus variants. No
  sub-variants, no interfaces, no generics.
- **No forbidden fields.** Conditionals may make a field required or
  leave it optional. They may never prohibit one. JSON Schema can
  forbid; do not use it. Forbidding is how one shape becomes twelve
  shapes wearing one name.
- No auth, no credentials, no user model. Permissions are Git's job.
- Do not build a renderer here.

## The node

One self-referential type. Every tracked folder holds exactly one
`thread.json`. Untracked folders hold none — **the node tree is a
subset of the folder tree.**

### identity

- `guid` — required, minted on creation, immutable.
- `name` — the folder path flattened with hyphens.
- `type` — one of **twelve**. See the list below. Adding a type later
  is a minor version bump.

### type — the twelve

Enum values are **camelCase**, matching the field-name convention
already in use (`isPartOf`, `plannedStart`, `sourceVerified`).
PROMCODE's PascalCase is an RDF class-name convention and does not
carry over.

| # | value | source |
|---|---|---|
| 1 | `project` | PROMCODE |
| 2 | `plan` | PROMCODE |
| 3 | `report` | PROMCODE |
| 4 | `scopeItem` | PROMCODE |
| 5 | `workItem` | PROMCODE |
| 6 | `artifact` | PROMCODE |
| 7 | `issue` | PROMCODE |
| 8 | `risk` | PROMCODE |
| 9 | `measurement` | PROMCODE |
| 10 | `operation` | sitting 8 |
| 11 | `decision` | sitting 9 |
| 12 | `option` | sitting 9 |

`task` is **not** a type. It appears in file 34 as illustration only.
Do not put it in the enum.

### dates — five fields

**Amendment to the sitting-8 lock.** Sitting 8 locked four date
fields. `decidedDate` is added as a fifth, accepted sitting 10, to fix
correction 19 — deciding and executing are two timestamps and must be
two fields.

- `plannedStart`
- `plannedEnd`
- `actualStart`
- `actualEnd`
- `decidedDate`

All five exist on the shape for every type, per the no-forbidden-fields
rule. A `workItem` that had a go/no-go may carry a `decidedDate`. That
is allowed and is a deliberate consequence of the fence.

### Conditional requirements by type

Required means the validator ERRORs without it. Everything not listed
as required is optional.

| type | required |
|---|---|
| `project` | `plannedStart`, `plannedEnd` |
| `plan` | `plannedStart`, `plannedEnd` |
| `report` | `actualStart` |
| `scopeItem` | `plannedEnd` |
| `workItem` | `plannedStart`, `plannedEnd` |
| `artifact` | `actualEnd` |
| `issue` | `actualStart` |
| `risk` | `actualStart` |
| `measurement` | `actualStart` |
| `operation` | `plannedStart` |
| `decision` | `decidedDate` |
| `option` | none |

Notes the code must not lose:

- **`operation` never requires `plannedEnd`.** Operations don't end.
  Requiring one would be a lie in the file.
- **`report` requires no planned dates.** A report covers a period.
  An open report has no `actualEnd`; whether it is open or abandoned
  is `state`'s job, not a date's.
- **`artifact` requires only `actualEnd`** — the date it existed. An
  artifact is a thing, not work. `plannedEnd` stays optional so a due
  date can be stated without inventing a duration.
- **`risk` requires `actualStart`, meaning identified-on.** It is the
  date someone wrote the risk down, not the date the risk started
  happening. See OPEN below — this naming is a known rot risk.
- **`decision` requires none of the planned/actual four.** Execution,
  if you want it, goes on `actualStart`. The gap between `decidedDate`
  and `actualStart` is the measurement file 26 was after.
- **`option` requires nothing.** An option may never be built; every
  date on it would be fiction. The date that matters is on the
  decision above it. Real dates land on the `workItem` beneath a
  chosen option.

### state

Shared vocabulary across every type: `open`, `active`, `done`,
`abandoned`, `superseded`. Type-specific values only where a type needs
one (`option` adds `chosen`). Same word, same meaning, everywhere.

### pointers — all hold a GUID unless noted

- `isPartOf` — the parent. Empty allowed **at repo root only**.
- `supersedes`
- `supersededBecause` — free text, deliberately uncheckable
- `abandonedScope`
- `realizedAs`
- `voidedPlan`
- `mitigatedBy`
- `blockedBy` — the waiting node points at the blocker. The blocker
  holds nothing.
- `representedBy` — **holds a path, not a GUID.**

### body

Prose. For `type: decision`, three required fields: `context`, `chose`,
`consequences`. `chose` is prose, not a pointer.

### extension block

One reserved key. Base validator never reads inside it. Model on
OSCAL's `props`: array of objects with required `name` (token) and
`value` (string), optional `ns` (URI namespace), `class`, `remarks`.
Check OSCAL's exact naming at
`https://pages.nist.gov/OSCAL/learn/tutorials/general/extension/`
before finalising. Domain clocks (Apollo GET) go here or in prose.

`sourceVerified` — boolean, default `false`.

### threads[]

Zero or more nodes. On disk this is subfolders. Expressed with
`$ref`/`$defs`.

## Type-specific rules

**`decision`** requires `context`, `chose`, `consequences`, and
`decidedDate`. Holds until superseded. **No expiry field.** Staleness
is calculated by the renderer from the date. Usage weight is derived —
count of nodes pointing at its GUID. Nothing stored.

**`option`** — alternatives are nodes, not prose. Whether one won is a
`state` value (`chosen`).

**Validator rule:** a `decision` must have exactly one `option` beneath
it in state `chosen`. The decision does **not** point down at the
winner.

## Validator — two tiers

**ERROR (blocks the commit)**
- Schema violation, including a missing conditionally-required date.
- Duplicate `guid`. Scope: files in the commit against an index of
  existing GUIDs in that repo. Not a full walk every time.
- Deleting or removing a node another node points at.
- A `decision` with zero or more than one `chosen` option beneath it.
- `isPartOf` empty anywhere but the repo root.

**WARNING (shows, does not block)**
- `representedBy` path does not resolve.
- `supersededBecause` thin or empty. **Do not enforce a minimum
  length.** Expose it, don't judge it.

## Tooling that must exist

A copy command that **mints a new GUID on the way through.**

## Deliberately excluded from v1

- `size` / `unit` — parked.
- `missionClock` — extension block or prose.
- Any field asserting "still true as of" — **locked out.**
- Meta-schema. Git branching does that job.
- Interfaces, generics, type inheritance below the first level.

## OPEN — do not decide these in code

- Where the iteration counter is recorded.
- **`measurement` has no worked definition** from this run. Its only
  appearance is the decision-gap note in file 24. `actualStart` as its
  timestamp is a recommendation, not a ruling. Do not build anything
  else onto this type until it is defined.
- **The risk identified-on naming.** `actualStart` meaning "identified"
  is semantic overload and will rot. Either it gets its own field
  (`identifiedDate`, parallel to `decidedDate`) or it stays on
  `actualStart` and `VALIDATE.md` says so in plain words. Not ruled.
- Whether `chose` should also carry a structured reference to the
  chosen option's GUID — considered, **rejected as a two-way link. Do
  not reintroduce.**

## First test after it validates

Draft Apollo 13's `thread.json` tree, then Loom's own. **If the schema
cannot describe Loom, it is too narrow.**
