# llm-wiki-template

An empty, ready-to-fill **personal LLM wiki**: ingest raw sources (video captions, web pages,
PDFs, text, doc repos…), compile them into curated Markdown articles, and let LLM agents read
them back. Source-agnostic; video captions are the first supported input.

It's driven entirely by the **`wiki:*` plugin skills** and **`youtube-captions`** — not by any
build system. Start with `/wiki:wiki` (natural-language router) or follow the quick flow below.

```
/youtube-captions <youtube-url> --out wiki/topics/<slug>/inbox/
/wiki:ingest        # inbox → raw/
/wiki:compile       # raw/ → wiki/ articles
/wiki:query "..."   # read it back
```

See **`CLAUDE.md`** for the full structure, the skill map (which skill for which task), and
conventions.
