# Cover image art direction

One consistent visual system for every AI-generated cover, so the index page
reads as a designed set rather than twelve unrelated pictures. The style is
derived from the site's own identity: cool violet-tinted neutrals, a deep
teal accent, and the visual language of data — plots, fields, structures —
rather than photography.

## The style, in words

Abstract, diagrammatic, computational. Think "a figure from a beautiful
paper", not "a photo of a laptop". Generative-art texture is welcome;
skeuomorphism and stock-photo realism are not.

## Palette

| Role | Value | Use |
|---|---|---|
| Ground | deep violet-navy `#10111a` – `#1a1c2a` | dominant background |
| Primary marks | teal `#137a73` → `#45c5b6` | the main subject |
| Secondary marks | violet `#46196b` → `#8a5cc0` | supporting structure |
| Highlight | yellow `#f2d024` | one small element at most |

Dark ground is required: the site shows covers on both light and dark cards,
and dark covers with luminous marks work on both. Light/white backgrounds
blend into the light theme's cards and look broken.

## Prompt template

Fill the bracket from the post's subject, keep the rest stable:

> Abstract computational illustration of **[the post's core concept — e.g.
> "message classification: streams of particles being sorted into labeled
> channels" / "container isolation: identical geometric rooms nested inside
> each other" / "web crawling: a branching graph being traversed node by
> node"]**. Dark violet-navy background, luminous teal and violet geometric
> forms, one small yellow accent element, fine grid lines, generative art
> style, flat vector shading, no text, no letters, no people, no
> photorealism. Wide 16:9 composition with the focal element off-center.

## Rules

- **No text in the image.** Titles live in HTML; baked-in text breaks on
  crop, looks wrong at small sizes, and dates instantly.
- **One focal idea per cover**, drawn from the post's actual mechanism —
  the concept slot in the template is where each cover gets its identity.
- **Off-center composition**: the index crops covers to varying ratios, so
  keep the focal element in the middle two-thirds, not at the edges.
- **Export 1600×900**, save as `cover.jpg` (or `.png` if flat shapes) in
  the post's page bundle, set `image: cover.jpg` in front matter.
- Compress before committing — target under 300 KB.

## Checking a generated image

Reject and regenerate if: it contains any legible text or letterforms; the
background is light; it looks like a photograph; it has more than one yellow
element fighting for attention; or the focal subject is so close to an edge
that a 21:9 crop would lose it.
