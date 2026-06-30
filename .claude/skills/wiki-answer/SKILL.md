---
name: wiki-answer
description: >-
  Answer a question or carry out a task using ONLY this repo's local knowledge-base wiki
  (under `wiki/topics/<slug>/`), never the model's own training knowledge. Use whenever the
  user asks a practical domain question that a topic in this wiki covers. Trigger on how-to /
  advice / "what does X say about Y" questions in any covered domain even when the user never
  mentions the wiki, a slug, or a filename. Routes the question to the right topic and 1–3
  articles, then gives a concise, coherent answer grounded strictly in the source — no
  citations, no invented facts, and an explicit "the wiki doesn't cover this" when the source
  is silent. Do NOT trigger for questions outside the topics present under `wiki/topics/` —
  those have nothing to draw from here.
---

# Wiki Answer

Answer domain questions from this repo's local wiki, and **only** from it. The wiki is a
curated, source-of-truth knowledge store (compiled from primary sources). The reader trusts
that every claim in your answer traces back to the wiki text — so the value is entirely in
*not* substituting your own training knowledge.

## Prime directive

Everything you assert comes from the wiki text you read. If the wiki is silent or only
partially covers the question, say what it doesn't cover instead of filling the gap from
general knowledge. A short honest "the wiki doesn't go into X" is more useful than a confident
paragraph the source can't back.

## Routing: question → topic → articles

The wiki lives under `wiki/` at the repo root. Layout:

```
wiki/wikis.json                         ← machine-readable topic list (slug, title, description)
wiki/topics/<slug>/config.md            ← answer language + scope (in/out) for the topic
wiki/topics/<slug>/wiki/_index.md       ← router: every article with a one-line summary + link
wiki/topics/<slug>/wiki/<layer>/*.md    ← the articles (layers: concepts, topics, references, theses)
```

Steps:

1. **Pick the topic.** Read `wiki/wikis.json`; match the question to a topic by its
   `description`/`title`. No topic fits → tell the user the knowledge base doesn't cover this
   subject, and stop. Don't answer from training knowledge.
2. **Check scope + language.** Read that topic's `config.md`. It states the **answer language**
   (answer in it — much source material is intentionally not translated) and what's out of
   scope. An out-of-scope question → say so.
3. **Find the articles.** Read `wiki/topics/<slug>/wiki/_index.md` — it lists every article with
   a summary. Semantic-match the question to **1–3** articles. For a specific term the summaries
   miss, grep:
   `grep -ril "term" wiki/topics/<slug>/wiki --include='*.md' | grep -v _index`
4. **Read the full bodies** of the matched articles — not just frontmatter/summaries. Cross-topic
   questions: follow `depends_on` in frontmatter and links in the body to one or two more.

## Composing the answer

The user wants the answer, not a tour of how you found it.

- **Lead with the answer.** First sentence addresses what was asked. No "Great question",
  no "According to the wiki…", no restating the question, no preamble.
- **No citations.** Don't name files, articles, sources, or say "the wiki says". Present it as a
  single coherent voice. (You still answer *only* from the source — you just don't show the seams.)
- **Concise and on-point.** Cover what was asked and closely related must-knows the source flags
  (e.g. a safety caveat the source itself stresses). Cut tangents, padding, and disclaimers the
  source didn't make.
- **Structure to fit.** A direct question → a few sentences or a short list. A "how do I…" →
  ordered steps. Don't pad a simple answer into sections.
- **Answer in the source's language** (per `config.md`).
- **Gaps are answers too.** Partially covered → give what's there, then note the boundary in one
  line ("the source doesn't cover X").

## Style example

Terse, grounded, no seams. Real answers draw their content from the article bodies you read.

Bad: "Great question! According to `foo.md`, the source says… Generally, experts also recommend…"
Good: a direct answer in the source's own voice, only from what the matched articles state, with
one honest line on anything the source leaves out.
