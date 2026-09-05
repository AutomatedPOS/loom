# Loom glyph factory

Comfy API graph, retired as the production seat 2026-09-05. Inner skins are drawn by Grok (Cursor); see `DESIGN-BIBLE.md` charter out_of_scope item 3. Clamp is `DESIGN-BIBLE.md` §4, especially 4.3. This graph draws **inner skins only**. Outer frames, fill-state, and accents are renderer work. Out-of-scope item three stays intact: the bible produces no artwork; this is a leftover handoff graph, not the artist.

On Spark:

- UI (LiteGraph, this is what the canvas loads): `user/default/workflows/loom_glyph_factory.json`
- API (prompt payload only): `user/default/workflows/api/loom_glyph_factory.api.json`

Windows copies: `loom_glyph_factory.json` (UI) and `glyph-factory.api.json` (API) in this folder; same pair under `comfy-director/workflows/`. Do not drop the API file onto the canvas — Comfy will open a blank graph. After a Comfy restart, open **loom_glyph_factory** from the workflow menu. Queue. Outputs land under `loom_glyph/`.

## What it does

Generate black-on-white (SDXL's native icon mode), two-color quantize, invert to white-on-black, hard threshold. Four 1024 masters per run, each cut to **1024 / 512 / 64 / 32**. 64 is the bible tile. 32 is the skin box.

## Clamp (locked)

Do not vary the clamp. Interpolate SUBJECT into the first clause. Prompt on node `8` is the full derived string. Generate **black on white** — the graph inverts.

```
flat minimalist pictogram of {SUBJECT}, front view, orthographic, solid black filled silhouette on plain white background, details as white negative-space cutouts, thick uniform silhouette, centered, square composition, no outline strokes, no 3d, no isometric, no shadow, no gradient, no texture, no text, no letters, single icon only, must stay legible at 64 pixels
```

Negative on node `3` is locked. Orange is out. Portal grammar, not costume. Do not ask for a sheet, a grid, or a scene.

## Subjects already drawn in the bible (4.3)

Smoke, not Valve costume.

| Skin | SUBJECT |
|---|---|
| tool | an open-end spanner |
| process | three filled circles evenly spaced on one horizontal bar through their centers |
| human | a sphere on a closed capsule, neck is the gap |
| robot | cube on cube, visor slot, stub antenna |

Default on node `8` is the tool skin. Passing Spark smoke: `loom_glyph/1024_00014_.png` (seed 2026090514, batch 1).

New skins: name the thing. Store the pick as base-64 + description + name. That accretion is the library.

## External process feeds

| Node | Class | Field | What |
|---|---|---|---|
| `8` | PrimitiveStringMultiline | `value` | Full derived prompt (SUBJECT already interpolated into the clamp) |
| `5` | KSampler | `seed` | Change per run |
| `4` | EmptyLatentImage | `batch_size` | Default 4 |

## Outputs

Comfy output dir, prefix `loom_glyph/{1024,512,64,32}`. Four files per size per run.

## Not this graph

- Outer shape (circle / flowchart rect / double bars)
- Hollow / solid / motion / subdued
- Hazard, current-task, changed-since
- Light-mode invert (renderer flips the field)
