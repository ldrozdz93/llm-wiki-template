# CLAUDE.md

Guidance for Claude Code (and other LLM agents) working in this repo.

## What this repo is

A **template/skeleton for a personal LLM wiki**: an empty, ready-to-fill knowledge base where
raw sources (video captions, web pages, PDFs, text, doc repos, …) are ingested, compiled into
curated Markdown articles, and read back by LLM agents. Clone it, point an ingestion skill at a
source, compile, and you have a topic wiki.

**The reader is a machine, not a human.** Content is consumed by LLM agents. Optimize every file
for agent navigation: grep-friendly text, explicit YAML frontmatter, and the per-layer
`_index.md` routers — not human prose polish.

There is **no build system, no tests, no lint of the content** — it's plain Markdown driven
entirely by the wiki skills below. The hub currently has **zero topics**; that's the point.

## Which skills to use (the important part)

This repo is driven by the **`wiki:*` plugin skills** plus **`youtube-captions`**. Do NOT
hand-roll the wiki structure — invoke the skills, which know the conventions and keep the
indexes, logs, and `wikis.json` in sync.

| You want to… | Use |
|---|---|
| Anything, via natural language (router: init/status/config + all below) | **`/wiki:wiki`** |
| Download video captions (single video / channel / playlist) as Markdown | **`/youtube-captions`** |
| Ingest a source — URL, file, PDF, freeform text, or the topic inbox | **`/wiki:ingest`** |
| Bulk-ingest a collection — git doc repo, MediaWiki, CSV/JSON archive, Wayback | **`/wiki:ingest-collection`** |
| Compile raw sources → wiki articles (synthesize, cross-reference) | **`/wiki:compile`** |
| Ask a question against the compiled wiki (with citations) | **`/wiki:query`** |
| Answer strictly from the wiki, no citations, no training knowledge (local skill) | **`wiki-answer`** |
| Generate an output artifact (summary, report, study guide, glossary, …) | **`/wiki:output`** |
| Health checks (broken links, missing indexes, stale content) | **`/wiki:lint`** |
| Article-layer maintenance (staleness, quality, coherence) | **`/wiki:librarian`** |
| Truth-seeking trust audit of a wiki + its outputs | **`/wiki:audit`** |
| Research a topic from the web into the wiki | **`/wiki:research`** |
| Archive / restore a whole topic | **`/wiki:archive`** |

When unsure which to call, start with **`/wiki:wiki`** — it understands natural language and
routes to the right subcommand. Full inventory: any skill namespaced `wiki:*`.

## Typical flow (video captions → answerable wiki)

```
/youtube-captions <youtube-url> --out wiki/topics/<slug>/inbox/   # raw captions → inbox
/wiki:ingest                                                       # process the inbox → raw/
/wiki:compile                                                      # raw/ → curated wiki/ articles
/wiki:query "your question"        (or the wiki-answer skill)      # read it back
```

Other raw sources work the same way — swap the first step for `/wiki:ingest <url|path>` or
`/wiki:ingest-collection`. Captions are just the first supported source; the structure is
source-agnostic.

## Structure

```
wiki/                         ← HUB (managed by the skills)
  _index.md                   hub index (topic table)
  wikis.json                  machine-readable topic registry
  log.md                      activity log
  topics/<slug>/              ← one directory per topic wiki
    config.md                 title, slug, answer language, scope (in/out)
    _index.md                 topic index (layer counts, recent changes)
    log.md                    per-topic activity log
    inbox/                    ingest queue (.processed/ holds consumed inputs)
    raw/                      source material, by kind
      _index.md
      articles/ data/ notes/ papers/ repos/
    wiki/                     compiled articles, by layer
      _index.md
      concepts/ topics/ references/ theses/
    output/                   generated artifacts (reports, study guides)
      _index.md
```

Three layers, in dependency order: **`raw/`** (verbatim sources) → **`wiki/`** (synthesized
articles) → **`output/`** (artifacts built from articles). The `_index.md` files are routers —
keep them accurate (the skills do this for you).

## Conventions

- **Frontmatter:** YAML with **English keys**; values in the **source's own language** (source
  material is often intentionally not translated — the original stays canonical).
- **Answer language is per-topic**, declared in `config.md` — answer in it.
- **Names use underscores, not hyphens:** `board_games/`, `04_setup_phase.md`.
- **Don't fill gaps from training knowledge** when answering — if the source is silent, say so.

## Utility

- `scripts/md_to_html.py` — convert Markdown to phone-friendly standalone HTML (inlined CSS,
  dark mode) for humans reading on a phone. `python3 scripts/md_to_html.py PATH` (file or dir;
  `-o OUTDIR` to mirror). Needs `python3 -m pip install --user markdown`. (Rendered `*.html` is
  git-ignored.)
