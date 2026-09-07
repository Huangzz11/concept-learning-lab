# -*- coding: utf-8 -*-
"""把概念学习资料（Markdown）转换为自包含 HTML 页面。

用法:
    python md2html.py <文件.md> [<文件2.md> ...]

说明:
- 输入文件头部需有 YAML 元信息块（concept/date/review_status 等），会渲染为页面顶部信息条。
- 支持 mermaid 代码块（自动渲染）与 <details> 折叠自测题。
- 输出同名 .html 到同一目录。产物为单文件 HTML，可直接本地打开或托管到 GitHub Pages。
"""
import re, sys, pathlib
import markdown

CSS = """
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:#1f2328;font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.75}
.wrap{max-width:880px;margin:0 auto;padding:32px 24px 80px}
h1{font-size:1.9em;margin:.4em 0 .8em;border-bottom:3px solid #0969da;padding-bottom:.35em}
h2{font-size:1.35em;margin:1.8em 0 .6em;padding-bottom:.25em;border-bottom:1px solid #d0d7de}
h3{font-size:1.12em;margin:1.4em 0 .5em}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.95em}
th,td{border:1px solid #d0d7de;padding:8px 12px;text-align:left}
th{background:#f6f8fa}
tr:nth-child(even) td{background:#fafbfc}
code{background:#eff1f3;padding:2px 6px;border-radius:4px;font-size:.9em;font-family:Consolas,Menlo,monospace}
pre{background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:14px 16px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{border-left:4px solid #0969da;margin:1em 0;padding:.4em 1em;background:#f0f6ff;color:#3a4a5a}
blockquote p{margin:.4em 0}
details{border:1px solid #d0d7de;border-radius:6px;padding:10px 16px;margin:10px 0;background:#fff}
summary{cursor:pointer;font-weight:600;color:#0969da}
a{color:#0969da;text-decoration:none}
a:hover{text-decoration:underline}
.meta{background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 16px;font-size:.9em;color:#57606a;margin-bottom:2em}
.meta b{color:#24292f}
ul,ol{padding-left:1.6em}
hr{border:none;border-top:1px solid #d0d7de;margin:2em 0}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
{meta}
{content}
<hr>
<footer style="font-size:.85em;color:#6e7781">
本文档由 concept-learner Skill 生成，经作者人工核查（{review}）。
</footer>
</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true,theme:'base',themeVariables:{{fontSize:'14px'}}}});</script>
</body>
</html>
"""


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def extract_details(text):
    """把 <details> 折叠块抽出，内部内容单独交给 markdown 转换。"""
    blocks = []

    def repl(m):
        inner = m.group(1)
        summary_m = re.search(r"<summary>(.*?)</summary>", inner, re.S)
        summary = summary_m.group(1).strip() if summary_m else ""
        body = inner[summary_m.end():] if summary_m else inner
        body = body.strip()
        body_html = markdown.markdown(body, extensions=["extra", "sane_lists"]) if body else ""
        blocks.append((summary, body_html))
        return f"\x00DETAILS{len(blocks)-1}\x00"

    text = re.sub(r"<details>(.*?)</details>", repl, text, flags=re.S)
    return text, blocks


def convert_mermaid(html):
    def repl(m):
        code = m.group(1).strip()
        return f'<pre class="mermaid">\n{code}\n</pre>'
    return re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', repl, html, flags=re.S)


def convert(src: pathlib.Path):
    raw = src.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    body, details = extract_details(body)
    html = markdown.markdown(body, extensions=["extra", "sane_lists", "toc", "tables"])
    html = convert_mermaid(html)
    for i, (summary, body_html) in enumerate(details):
        html = html.replace(
            f"\x00DETAILS{i}\x00",
            f"<details>\n<summary>{summary}</summary>\n{body_html}\n</details>",
        )
    title = meta.get("concept") or meta.get("title") or src.stem
    rows = []
    for label, key in (("标题", "title"), ("学习概念", "concept"),
                       ("英文/别名", "english_alias"), ("领域", "domain")):
        if key in meta:
            rows.append(f"<b>{label}：</b>{meta[key]}")
    rows.append(f"<b>生成方式：</b>{meta.get('generated_by','concept-learner')} Skill")
    rows.append(f"<b>日期：</b>{meta.get('date','')}")
    rows.append(f"<b>核查状态：</b>{meta.get('review_status','待人工核查')}")
    meta_html = '<div class="meta">' + "<br>".join(rows) + "</div>"
    review = meta.get("review_status", "待人工核查")
    out = HTML_TEMPLATE.format(title=title, css=CSS, meta=meta_html, content=html, review=review)
    dest = src.with_suffix(".html")
    dest.write_text(out, encoding="utf-8")
    print(f"OK: {src.name} -> {dest.name} ({len(out)//1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        convert(pathlib.Path(arg))
