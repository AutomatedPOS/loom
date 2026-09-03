# VALIDATE.md — loom-warp v1.0.0

Same rules as `thread.schema.json` and the validators.
An LLM checks its own `thread.json` against this file. Do not invent
fields. Do not skip a rule because the scene seems to need it.

**Python (`validate.py`) is the reference validator.** PowerShell and
this file are conformance targets, not peers. If they disagree with
Python, Python is right. Quietly passing what Python fails is worse
than saying you cannot verify — run Python. PowerShell's limits on
current JSON Schema are accepted. Do not treat them as a defect to
fix.

Locked unless marked OPEN. Source: files 24, 30, 34,
brief r2 (supersedes file 35), sitting 10, walk packet 11 (file 36).

---

## What the rules are for

The schema lets a human be human and an LLM be an LLM without either
one pulling the other into nonsense. It protects the data, and it
protects the process. A person working loosely and a model that is
confidently wrong reinforce each other, and the result reads as solid
while being garbage.

Mess is fine. The sandbox is for drafting, guessing, and being wrong
out loud. The commit gate is where that stops, and it stops for both
sides on the same terms.

---

## Hard stop — if you break these, the file is wrong

1. One file type: `thread.json`. No YAML. No second kind of file.
2. One node shape. Every type uses the same fields. Conditionals make a
   field required. They never hide, ban, or remove a field.
3. Upward pointers only. A node does not list its children. On disk,
   children are subfolders that each hold their own `thread.json`.
4. Nothing is deleted. Superseded and abandoned stay on disk.
5. `type` is set at creation and never changes. `state` changes.
6. No expiry field. No "still true as of" field. No size/unit. No
   missionClock field in the base shape. No meta-schema.
7. `chose` is prose. It is not a GUID and not a pointer. Do not put
   the winning option's GUID in `chose`. That two-way link was rejected.
8. `task` is not a type. Do not emit it.
9. Permissions are Git's job. No auth fields.
10. Nodes are impersonal. No transcripts. No personal names. No
    conversation quotes. Sittings are date and number, not who sat.
    Titles and remarks are what the node is.
11. Every date field is a UTC calendar day. One clock. Local-day
    packet headers are not date fields.

---

## File placement

- A tracked folder holds exactly one `thread.json`.
- An untracked folder (source, assets, build output) holds none.
- The node tree is a subset of the folder tree, not the same thing.
- Folder names do not encode type. Type lives in the file.

---

## Required on every node

| field | rule |
|---|---|
| `guid` | UUID, minted on creation, immutable. |
| `name` | Folder path from repo root, flattened with hyphens. `loom/weave/godot` → `loom-weave-godot`. |
| `type` | One of the twelve values below. camelCase. |

Everything else on the shape may be omitted unless a conditional
requires it.

`sourceVerified` is a boolean. If omitted, it is `false`. True means a
human opened the source and confirmed the value.

---

## The twelve types

| value | required fields beyond identity |
|---|---|
| `project` | none |
| `plan` | none |
| `report` | `actualStart` |
| `scopeItem` | none |
| `workItem` | none |
| `artifact` | `actualEnd` |
| `issue` | `actualStart` |
| `risk` | `actualStart` |
| `measurement` | `actualStart` |
| `operation` | none |
| `decision` | `decidedDate`, `context`, `chose`, `consequences` |
| `option` | none |

Adding a type later is a minor version bump. Do not add one in this
file.

### Date notes you must not "fix"

Dates are ISO dates `YYYY-MM-DD`, UTC calendar day. All five date
fields exist on every type. Presence on a type that does not require
them is allowed unless a writer-rejected note below says do not emit.
The schema never forbids a date.

`plannedStart` and `plannedEnd` are optional on every type. Do not
invent them. A living project with no planned end is not missing data.

- `operation` does not require `plannedStart`. Do not emit
  `plannedEnd` on an operation (operations don't end). Schema still
  allows the field.
- `report` requires `actualStart`. An open report has no `actualEnd`.
  Open vs abandoned is `state`, not a date.
- `artifact` requires only `actualEnd` — the UTC day that snapshot
  existed when copied. `plannedEnd` may be used as a due date. Do not
  invent a duration.
- `risk.actualStart` means **identified-on**: the date someone wrote
  the risk down, not the date the risk started happening. This naming
  is a known rot risk. It stays on `actualStart` until a dedicated
  field is ruled. Do not invent `identifiedDate`.
- `decision` requires `decidedDate`. If execution happened, that
  timestamp is `actualStart`. The gap between `decidedDate` and
  `actualStart` is load-bearing. Keep both.
- `option` requires no dates. Do not emit dates on an unbuilt option
  (fiction). Schema still allows the fields. The date that matters
  sits on the decision above it. Real work dates sit on the `workItem`
  beneath a chosen option.
- `measurement` has no worked definition beyond `actualStart` as a
  timestamp. Do not add meaning, extra required fields, or nested
  structure onto this type.

### Type → date map

Required by `type` (schema). `plannedStart` and `plannedEnd` are not
required on any type.

| type | required dates |
|---|---|
| `project` | none |
| `plan` | none |
| `report` | `actualStart` |
| `scopeItem` | none |
| `workItem` | none |
| `artifact` | `actualEnd` |
| `issue` | `actualStart` |
| `risk` | `actualStart` |
| `measurement` | `actualStart` |
| `operation` | none |
| `decision` | `decidedDate` (not one of the planned/actual four) |
| `option` | none |

Writer-rejected (do not emit; schema still allows): `plannedEnd` on
`operation`; all five date fields on `option`.

Required by `type` + `state`. Locked:

| type | state | also required |
|---|---|---|
| `workItem` | `done` | `actualStart`, `actualEnd` |

Planned-date type×state cells are closed: planned dates stay optional.
Actual-date type×state cells except `workItem` + `done` stay OPEN. Do
not fill one in because a tree happened to use it. The validator does
not enforce the done-workItem row yet; writers do. Tightening the
schema later is a major bump.

---

## state

Shared values, same meaning on every type:

`open` | `active` | `done` | `abandoned` | `superseded`

`option` may also use `chosen`. Other types may not.

There is no sixth state. "Planned, never used" is the absence of a
thing happening. Omit `state` and put `performed` `np` in `props`.
That is the convention. Do not invent `unused` or `notPerformed`.
A renderer that cannot tell "np" from "nobody filled it in" is a
renderer problem — see `RENDERER.md`. Not a schema change.

A decision holds until superseded. Staleness is calculated from the
date by the renderer. Do not store staleness. Do not store a hit
count; usage weight is the count of nodes pointing at that GUID.

---

## Pointers

All of these hold a GUID except the two called out.

| field | holds | notes |
|---|---|---|
| `isPartOf` | GUID or empty string | Empty allowed at repo root only. Everywhere else, ERROR. |
| `supersedes` | GUID | Old node stays. |
| `supersededBecause` | free text | Deliberately uncheckable. Do not require a length. |
| `abandonedScope` | GUID | |
| `realizedAs` | GUID | Risk → the issue it became. |
| `voidedPlan` | GUID | Issue → the plan it killed. |
| `mitigatedBy` | GUID | |
| `blockedBy` | GUID | Waiting node points at the blocker. The blocker holds nothing. |
| `representedBy` | **path**, not GUID | The artefact is a file. |

A node outliving a superseded parent keeps pointing at that parent.
Never reparent.

---

## Body

`body` is optional prose.

For `type: decision`, `context`, `chose`, and `consequences` are
required. `chose` is a sentence about what was picked, not a pointer
at the option node.

---

## Extension block — `props`

OSCAL naming (tutorial:
https://pages.nist.gov/OSCAL/learn/tutorials/general/extension/).

```json
"props": [
  {
    "name": "get",
    "value": "055:54:53",
    "ns": "https://example.invalid/loom",
    "class": "mission-clock",
    "remarks": "optional"
  }
]
```

- `name` required, token (no whitespace).
- `value` required, string.
- `ns` optional, URI. Organisations do not collide on `name` if `ns`
  differs.
- `class` optional string.
- `remarks` optional string.

The base validator checks that shape and then **stops**. It does not
interpret `name` or `value`. Domain clocks (Apollo GET) belong here
or in prose, not as new base fields.

Do not put unknown keys next to `guid`. Unknown keys belong in
`props`.

Duplicate `name` values are load-bearing. Two readings of the same
fact are two props with the same `name`. Do not mint a second name
(`docPage`, `get-flightplan`) to disambiguate. Discriminators:

- `page` is the PDF page a renderer seeks to. One meaning, forever.
  When the printed footer is also worth recording, a second `page`
  prop carries `class` `printed`. The PDF one carries `class` `pdf`.
- `class` is otherwise free (OSCAL). `pdf` / `printed` are values for
  `page`. `mission-clock` remains valid on `get`.
- `ns` is a URI. When a node cites a second document, `ns` names that
  document. Same `name`, different `ns`.

A node's props come from the document its `representedBy` points to.
A second document's value is a second prop with the same `name`, `ns`
set to that document, and `remarks`. Do not overwrite a cited value
with a number lifted from a file the node does not point at.

Do not use `docPage`. Deleted.

---

## `threads[]`

The schema is self-referential: a thread may contain threads.

On disk, do not list children in the parent file. Walk into
subfolders. If `threads[]` is present (bundled document), each item
must still be a valid node. Children for the decision rule are:

1. immediate subfolders that contain `thread.json`, and
2. items in `threads[]` if that array is present.

---

## ERROR — the file must not commit

Say **ERROR** and name the file and the rule. Any one of these fails
the tree.

1. **Not JSON**, or does not match `thread.schema.json` (wrong type
   value, missing identity, missing a conditionally-required date,
   extra keys outside the shape, `props` item missing `name`/`value`,
   `state: chosen` on a non-option, bad UUID, bad date).
2. **Duplicate `guid`.** Two nodes in this repo share a GUID. Scope is
   this repo. The index of GUIDs is derived from `thread.json` files
   already in the repo plus the files under check. Do not invent a
   second file format for the index.
3. **Dangling pointer.** A GUID pointer names a node that is not in
   this repo's `thread.json` set. That is how "deleted a node another
   node points at" is detected. Empty `isPartOf` is not a pointer.
4. **Decision chosen-count.** A node with `type: decision` must have
   **exactly one** child (folder child and/or `threads[]` item) whose
   `type` is `option` and whose `state` is `chosen`. Zero is ERROR.
   Two or more is ERROR. The decision file does not point down at the
   winner.
5. **`isPartOf` empty off-root.** The `thread.json` sitting in the
   directory being validated as repo root may have `isPartOf` omitted,
   `""`, or empty. Every other `thread.json` must have a UUID in
   `isPartOf`.

---

## WARNING — print it, do not block

1. `representedBy` is present, non-empty, and the path does not
   resolve relative to the folder that holds this `thread.json`.
2. `supersedes` is set and `supersededBecause` is missing, empty, or
   only whitespace. Do **not** fail a short reason. A one-word reason
   is allowed. Expose thinness; do not judge it.

---

## Copy

Copying a folder of nodes by ordinary copy clones identity. The copy
command (`copy_thread.py` / `Copy-Thread.ps1`) must:

1. Copy the folder tree.
2. Mint a new `guid` for every `thread.json` (and every nested item in
   `threads[]`) on the way through.
3. Rewrite GUID pointers that pointed at a copied node so they point
   at that node's new GUID.
4. Set the copied root's `isPartOf` to the supplied parent GUID, or to
   empty if none was supplied.
5. Rewrite `name` from the destination path, hyphen-flattened.

---

## Key order

`format_thread.py` rewrites `thread.json` to schema property order.
`--check` fails if a file differs. CI runs `--check`. Humans read
diffs; scrambled keys make a two-value edit look like a full rewrite.

---

## OPEN — do not decide in output

- Where the iteration counter is recorded.
- Anything about `measurement` beyond `actualStart` as a timestamp.
- Whether risk identified-on gets its own field. Until that is ruled,
  keep using `actualStart` and the sentence in the date notes above.
- A structured GUID beside `chose`. Rejected. Stay rejected.
- Actual-date type×state cells except `workItem` + `done` → actuals.

---

## Self-check before you emit a tree

Work these in order. If any line is no, fix the JSON. Do not emit.

- [ ] Every tracked folder has exactly one `thread.json`. Untracked
      folders have zero.
- [ ] Every file is JSON. No YAML.
- [ ] Every node has `guid`, `name`, `type`.
- [ ] `type` is one of the twelve. Not `task`.
- [ ] Required dates for that type are present as `YYYY-MM-DD`.
- [ ] `decision` has `decidedDate`, `context`, `chose`, `consequences`.
- [ ] `chose` is prose, not a GUID.
- [ ] `option` is the only type with `state: chosen`.
- [ ] Each `decision` has exactly one `option` beneath it in state
      `chosen`. The decision does not point at that option.
- [ ] Pointers that hold GUIDs hold GUIDs. `representedBy` holds a
      path. `supersededBecause` holds text.
- [ ] `isPartOf` is empty only on the repo-root node.
- [ ] No GUID is used twice.
- [ ] Every non-empty GUID pointer names a node in this tree.
- [ ] Unknown facts went into `props`, not new keys.
- [ ] You did not add size, unit, missionClock, expiry, or
      still-true-as-of.
- [ ] You did not delete a node. You marked `superseded` or
      `abandoned`.
