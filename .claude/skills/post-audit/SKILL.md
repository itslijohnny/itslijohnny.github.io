---
name: post-audit
description: Audit and polish a draft blog post for johnnyli.cc before publishing. Use this whenever the user shares a draft article, asks to review/polish/prepare/publish a post, creates a new post, or asks for feedback on writing for the blog — even if they don't say "audit". Also use it when the user asks for a cover image, a description, tags, or front matter for a post. It checks structure, front matter, the recruiter-reader lens, the search-reader lens, and cover image direction, then proposes concrete edits.
---

# Post Audit

Audit a draft post for this blog and make it publishable. The blog has two
jobs at once, and every check below serves one of them:

1. **The evaluator** — a recruiter or hiring manager who clicked through from
   a resume or LinkedIn. They spend under a minute, they skim, and they are
   not reading to learn the topic; they are reading to judge the author. What
   they can actually assess in that minute: does this person think clearly,
   explain decisions, and finish things? Every post is a work sample.
2. **The searcher** — a reader who arrived from Google or an AI assistant
   with a specific problem. They give the page a few seconds to prove it
   answers their question, and they leave the moment it stops being useful.
   They reward posts that state the answer early and structure the rest for
   skimming.

Both readers skim; neither rewards suspense. Front-load everything.

## Workflow

1. Read the draft in full before commenting on anything.
2. Run the audit sections below in order.
3. Deliver findings using the report format at the end — concrete rewrites,
   not abstract advice ("change X to Y", never "consider improving X").
4. Apply the edits the user approves. Never publish or push without being
   asked.

If the user is starting a post from scratch rather than auditing a draft,
use the same sections as a construction guide, and offer the front matter
skeleton first.

## 1 · Front matter

The site is Hugo + hugo-theme-stack; posts live in
`content/post/<slug>/index.md` with page-bundle images alongside.

Check:

- **title** — contains the words someone would actually search, front-loaded.
  "Automate Image Processing for My Blog" beats "My Cool New Script". Under
  ~60 characters so it doesn't truncate in search results.
- **description** — this is both the card dek on the index page and the
  search snippet, so it's the single highest-leverage line in the file. It
  must lead with the outcome, not the topic. Under ~155 characters.
  - Weak: "This is an introduction to my Python script that automates image
    processing."
  - Strong: "One command now crops, compresses, and uploads a cover image —
    a job that used to take 15 minutes per post."
- **slug** — set explicitly, short, hyphenated, keyword-bearing. The
  permalink is `/p/<slug>/`.
- **date** — real publish date, ISO format with timezone.
- **categories** — 1–2, reused from the existing set (check
  `content/post/*/index.md` for what's in use; don't mint a near-duplicate
  like "Data Analytics" when "Data Analysis" exists).
- **tags** — 3–6 that a reader might click, not an inventory of every
  library mentioned. Historical posts have 10–15 tags; don't imitate them.
- **image** — cover file name (see section 5).

## 2 · Structure

- **The first three sentences carry the whole post.** By the end of them,
  both readers must know what problem this solves and what the outcome was.
  If the draft warms up slowly, pull the conclusion up to the top and let
  the rest be the "how".
- Pick the shape that fits and check the draft against it:
  - **Project/build post**: problem → approach → result → what I'd do
    differently. The "result" needs something concrete — a number, a
    screenshot, a before/after.
  - **Decision post**: context → options considered → what I chose and why →
    how it turned out. The "why" is the whole value; tradeoffs named
    explicitly.
  - **How-to/tutorial**: what you'll have at the end → prerequisites →
    steps → verification. Each step's code block gets one line of "why"
    before it; never two code blocks back-to-back with no prose between.
- Headings must tell the story on their own — a reader who reads only the
  headings should still get the arc. Where a heading can naturally be the
  question a searcher would type, prefer that form.
- One idea per section. A section longer than ~6 paragraphs is usually two
  sections.
- End with a short takeaway or "what's next", plus links to related posts
  on this site if any genuinely relate.

## 3 · The recruiter lens

Read the draft once as a hiring manager and check:

- **Judgment is visible.** At least one place where the post says *why* —
  why this tool, why this approach, what was rejected and for what reason.
  A post that only narrates steps reads as following a recipe.
- **Impact is stated on the metric ladder.** If business numbers don't
  exist, walk down: volume (how much data/how many users), speed (time
  saved), quality (error rate, accuracy), cost. Even "cut a 15-minute chore
  to one command" counts. Estimates are fine when honestly framed
  ("roughly", "about") — invented precision is not. Never fabricate a
  number the user didn't give you; ask instead.
- **The work is verifiable.** Link the repo, the demo, the notebook. A
  claim with a link is evidence; without one it's an assertion.
- **The writing itself is clean.** This is a work sample: typos and
  grammar slips cost more here than anywhere else, because clear writing is
  one of the few things the evaluator can directly verify. Do a dedicated
  spelling/grammar pass — historical posts on this site shipped with typos
  ("Scrayp", "wiht", "Washginton"), so assume the draft has some too.

## 4 · The searcher lens

- **Answer-first.** The searcher's question should be answered in the
  opening, with the rest as depth. If the answer only appears after 800
  words of setup, restructure.
- **Skimmability.** Short paragraphs (2–4 sentences), meaningful headings,
  code blocks that are copy-paste runnable, lists where the content is
  actually a list.
- **Every image has alt text** that describes what the image shows —
  screenshots included. This is accessibility and image-search traffic at
  once.
- **Internal links** to related posts where they genuinely help; external
  links to primary sources (docs, papers) rather than aggregators.
- **One post, one query.** If the draft answers two unrelated questions,
  it will rank for neither — suggest splitting.
- Machine readers matter too: AI assistants quote pages the way search
  engines used to link them. Clear structure, early answers, and honest
  headings serve both.

## 5 · Cover image

Covers are AI-generated. The failure modes to prevent: covers that look
like stock photos, covers that differ so much post-to-post that the index
looks incoherent, and light-background images that blend invisibly into
the site's cards (several historical posts have this problem).

Read `references/cover-image-style.md` for the shared art direction and the
prompt template, then generate or request the cover from it. Non-negotiables
regardless of style: no text in the image (it never survives cropping or
translation), no fake photography of people or offices, mid-tone or darker
background, 1600×900, saved into the post's page bundle.

## Report format

Deliver the audit as:

```
## Post audit: <title>

**Verdict**: ready / ready after edits / needs restructuring

**The one thing**: <the single change that matters most>

### Front matter
<field-by-field: current → proposed, with reasoning>

### Structure
<findings, each with a concrete fix>

### Recruiter lens
<findings>

### Searcher lens
<findings>

### Cover image
<proposed prompt from the template, or approval of existing cover>

### Line edits
<typos/grammar as a list: "line N: 'wiht' → 'with'">
```

Keep findings that pass to one line ("Front matter: complete, description
already outcome-led"). Spend the space on what needs to change.
