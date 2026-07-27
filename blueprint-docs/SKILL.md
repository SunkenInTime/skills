---
name: blueprint-docs
description: House style for standalone HTML documents — plans, investigations, reports, proposals, specs, RFCs, postmortems, design docs, briefs. Use whenever writing or restyling a single-file HTML document, or when the user says "plan doc", "make it match my usual style", or "the blueprint style".
---

Every HTML document is a **blueprint**: a technical drawing, not a web page. Hairline rules, hatched separators, monospace annotation, nothing rounded, nothing glowing. The page looks measured — like it was drafted, not designed.

Do not improvise the visual system. Inline [`assets/blueprint.css`](assets/blueprint.css) verbatim into a `<style>` block and build on [`assets/skeleton.html`](assets/skeleton.html). Output is always **one self-contained `.html` file** — no build step, no external CSS/JS, fonts via the single Google Fonts `@import` already in the sheet.

## Invariants

Break one and the document stops reading as a blueprint.

- **Mono carries structure, sans carries prose.** JetBrains Mono for every heading, label, table header, metric, caption, diagram string, and button. Inter for paragraphs and list items only. This split is the single loudest signal of the style.
- **Hairlines, never boxes.** Every division is `1px solid var(--line)`. No `border-radius` beyond the 1–2px on inline `code` and legend chips. No `box-shadow`, ever. No gradient except `--hatch`.
- **One accent.** `--accent` for emphasis, links, active states, the dominant bar in a chart. Semantics ride `--ok` / `--warn` / `--danger` only where a value is genuinely good or bad. Nothing else gets a color.
- **Never hardcode a hex outside the palette block** — inline SVG included. Every fill, stroke, and text color is a token, or the document breaks the moment it re-themes.
- **Full-bleed blocks.** Prose sits inside `--pad`; every block element — `pre`, `.table-wrap`, `.diagram`, `.metric-line`, `h1`, `h2` — escapes it with `margin-inline: calc(-1 * var(--pad))` and rules itself with `border-block`. The eye should see block edges touching the ruled column lines.
- **Hatch marks the seam.** The `-45°` hatch band appears under the topbar and, via `h2::before`, above every section but the first. It is the document's punctuation.
- **Ruled columns.** The 4-column `.page-grid` draws vertical hairlines down the whole page. Topbar, hatch cell, and content all carry `border-inline` so the rules run unbroken from header to footer.
- **Uppercase mono micro-labels** with `letter-spacing: .16em`–`.18em` for kickers, rail labels, metric labels, and top actions.

## Theming

Both palettes ship in the sheet and both are load-bearing — the document is not a dark document that tolerates light.

- Dark is the CSS default. The inline `<head>` script resolves `localStorage` → system preference → dark and sets `data-theme` on `<html>` **before first paint**; keep it in `<head>` or the theme flashes. `:root[data-theme="light"]` is the only override block.
- Light is warm paper (`#faf9f6`), not white, mirroring the warm-neutral grays of the dark palette. The accent darkens to `#3f52c9` and the verdict colors deepen — the dark values fail contrast on paper.
- The topbar carries a `LIGHT`/`DARK` toggle that reads out the theme you'd switch *to*, and persists the choice.
- Both palettes are contrast-validated: every text token clears WCAG AA against its background, and every diagram label clears 3:1 against its bar.
- Adding a color means adding it to **both** blocks. A token defined in only one is a bug.

## Voice

The prose is as much of the style as the CSS.

- Lead with the number. "12.478 s — 82.9% of that path — was the eager module graph," not "module loading was slow."
- `<strong>` is for load-bearing figures and verdicts, not for enthusiasm.
- Every document opens: `.kicker` (3 dot-separated status words) → `h1` (a full clause, not a noun phrase) → `.lede` (the whole finding in 3–5 sentences, numbers included).
- State confidence and non-goals explicitly. Say what was not measured.
- No exclamation marks, no emoji, no "we're excited to."

## Composition

Reach for these in roughly this order; a document need not use all of them.

- `.metric-line` — 2–4 headline figures, flush, directly under the first `h2`. Values get `.good`/`.bad` when the number carries a verdict.
- `blockquote.callout` — one per document at most, for the recommended decision.
- `.table-wrap > table` — the workhorse. Milestones, findings-with-confidence, before/after. Right-hand columns take `.good`/`.warn`/`.bad`.
- `pre` — commands and config, with a leading `#` comment line naming what it is.
- `.diagram` — see below.
- `.caption` — environment, method, or caveat under a `pre` or diagram.

## Diagrams

Hand-author inline `<svg>`. Never a chart library, never a raster image.

- `viewBox="0 0 760 H"`, height to fit. Plot area x≈16–718.
- Wrap in `.diagram` with a `.diagram-title` above and, when the encoding needs decoding, a `.legend` below. `role="img"` + `aria-label` on the wrapper; `aria-hidden="true"` on the `<svg>`.
- **Tokens only, no hex.** `fill="var(--series-2)"`, `stroke="var(--line-strong)"`. Axis text `var(--fg-muted)`, data labels `var(--fg)`, labels sitting on a series bar `var(--on-fill)`, on the accent bar `var(--on-accent)`. Legend chips take `style="--legend:var(--series-2)"`.
- Series ramp toward the accent: `--series-1` → `--series-4`, with `--ok` / `--warn` / `--danger` reserved for verdicts.
- Annotate directly on the mark — a dashed accent line labelled `median 2.091 s` beats a legend entry.
- Bars are plain `<rect>`: no rounding, no stroke, no opacity.

## Checklist

- [ ] Single file, no external assets beyond the font `@import`.
- [ ] Every `h2`/`h3` has an `id` — the rail outline and reading progress are generated from them by the skeleton's script.
- [ ] `<title>` set; `.kicker` present; rail auto-fills.
- [ ] Zero `border-radius` on blocks, zero `box-shadow`, zero non-hatch gradients.
- [ ] Every block element bleeds to the column rules.
- [ ] **No hex outside the two palette blocks** — grep the file for `#` in `fill=`, `stroke=`, and `style=`.
- [ ] **Read the document in both themes.** Toggle, reload, confirm the choice persisted and nothing flashed.
- [ ] Narrow viewport: rail collapses, `border-inline` drops, nothing overflows.
