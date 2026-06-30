#!/usr/bin/env python3
"""Convert Markdown to phone-friendly standalone HTML.

Usage:
    python3 scripts/md_to_html.py PATH [PATH ...] [-o OUTDIR]
    python3 scripts/md_to_html.py --selftest

PATH is a .md file or a directory (searched recursively for *.md). By default
each <name>.md is written beside it as <name>.html; with -o the directory tree
is mirrored into OUTDIR. Output is one self-contained HTML file (CSS inlined),
so it opens offline on a phone with sane wrapping, large text and dark mode.

Requires the `markdown` package:  python3 -m pip install --user markdown
(use `python3 -m pip`, not bare `pip`, so it installs for the same interpreter.)
"""
import argparse
import html
import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency: python3 -m pip install --user markdown")

_FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
_TITLE = re.compile(r'^title:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)
_H1 = re.compile(r"^#\s+(.+)$", re.MULTILINE)

CSS = """
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#fff;color:#1a1a1a;
 font:1.08rem/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:42rem;margin:0 auto;padding:1.5rem 1.15rem 4rem}
h1,h2,h3{line-height:1.25;margin:1.8em 0 .55em;font-weight:650}
h1{font-size:1.7rem;margin-top:.2em}
h2{font-size:1.34rem;border-bottom:1px solid #e6e6e6;padding-bottom:.2em}
h3{font-size:1.12rem}
p,li{overflow-wrap:break-word}
ul,ol{padding-left:1.3em}
li{margin:.3em 0}
a{color:#0b62d6}
blockquote{margin:1em 0;padding:.4em 1em;border-left:4px solid #d3d3d3;
 background:#fafafa;color:#555}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em;
 background:#f2f2f2;padding:.1em .3em;border-radius:4px}
pre{background:#f6f8fa;padding:1em;border-radius:8px;overflow-x:auto}
pre code{background:none;padding:0}
img{max-width:100%;height:auto}
table{display:block;overflow-x:auto;border-collapse:collapse}
th,td{border:1px solid #ddd;padding:.45em .6em;text-align:left}
hr{border:0;border-top:1px solid #e6e6e6;margin:2em 0}
@media (prefers-color-scheme:dark){
 body{background:#16181c;color:#d9dde1}
 h2,hr{border-color:#2c2f36}
 a{color:#6cb0ff}
 blockquote{background:#1c1f24;border-color:#3a3f47;color:#a8aeb6}
 code,pre{background:#1c1f24}
 th,td{border-color:#2c2f36}
}
"""

_PAGE = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n"
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    "<title>{title}</title>\n<style>{css}</style>\n"
    "</head>\n<body>\n<main>\n{body}\n</main>\n</body>\n</html>\n"
)


def split_frontmatter(text):
    """Return (title_or_None, body_without_frontmatter)."""
    m = _FRONTMATTER.match(text)
    if not m:
        return None, text
    t = _TITLE.search(m.group(0))
    return (t.group(1).strip() if t else None), text[m.end():]


def convert(text, fallback_title):
    title, body_md = split_frontmatter(text)
    if not title:
        h = _H1.search(body_md)
        title = h.group(1).strip() if h else fallback_title
    body = markdown.markdown(body_md, extensions=["extra", "sane_lists"])
    return _PAGE.format(title=html.escape(title), css=CSS, body=body)


def iter_md(paths):
    """Yield (base_dir, md_path); base_dir anchors relative paths for -o."""
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for f in sorted(p.rglob("*.md")):
                yield p, f
        elif p.suffix.lower() == ".md":
            yield p.parent, p
        else:
            print(f"skip (not .md or dir): {p}", file=sys.stderr)


def dest(base, f, outdir):
    if outdir is None:
        return f.with_suffix(".html")
    return Path(outdir) / f.relative_to(base).with_suffix(".html")


def selftest():
    t, b = split_frontmatter('---\ntitle: "Hi"\nx: 1\n---\n# Body\ntext')
    assert t == "Hi" and b.startswith("# Body"), (t, b)
    t, b = split_frontmatter("# No FM\nhi")
    assert t is None and b.startswith("# No FM"), (t, b)
    out = convert('---\ntitle: "T & co"\n---\n# H\n\n- a\n- b\n', "fb")
    assert "<title>T &amp; co</title>" in out, out
    assert "<li>a</li>" in out and "<li>b</li>" in out, out
    assert "max-width:42rem" in out and "width=device-width" in out
    print("selftest ok")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Markdown -> phone-friendly HTML")
    ap.add_argument("paths", nargs="*", help=".md files or directories")
    ap.add_argument("-o", "--outdir", help="mirror output tree here instead of beside source")
    ap.add_argument("--selftest", action="store_true", help="run internal checks and exit")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return
    if not args.paths:
        ap.error("give at least one .md file or directory (or --selftest)")
    n = 0
    for base, f in iter_md(args.paths):
        out = dest(base, f, args.outdir)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(convert(f.read_text(encoding="utf-8"), f.stem.replace("_", " ")),
                       encoding="utf-8")
        print(out)
        n += 1
    print(f"{n} file(s) converted", file=sys.stderr)


if __name__ == "__main__":
    main()
