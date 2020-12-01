import re
import tarfile
import io
import sys
from pathlib import Path
import argparse

import jinja2
import requests


TPL = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Prez</title>
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="{{ revealjs_url }}/dist/reset.css">
  <link rel="stylesheet" href="{{ revealjs_url }}/dist/reveal.css">
  <link rel="stylesheet" href="{{ revealjs_url }}/dist/theme/simple.css" id="theme">
  <style>
a.sourceLine { display: inline-block; line-height: 1.25; }
a.sourceLine { pointer-events: none; color: inherit; text-decoration: inherit; }
a.sourceLine:empty { height: 1.2em; }
.sourceCode { overflow: visible; }
code.sourceCode { white-space: pre; position: relative; }
div.sourceCode {
    margin: 1em 0;
    color: #333;
    background: #f8f8f8;
    box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.15);
}
pre.sourceCode { margin: 0; }
@media screen {
    div.sourceCode { overflow: auto; }
}
@media print {
    code.sourceCode { white-space: pre-wrap; }
    a.sourceLine { text-indent: -1em; padding-left: 1em; }
}
pre.numberSource a.sourceLine
{ position: relative; left: -4em; }
pre.numberSource a.sourceLine::before
{ content: attr(title);
  position: relative; left: -1em; text-align: right; vertical-align: baseline;
  border: none; pointer-events: all; display: inline-block;
  -webkit-touch-callout: none; -webkit-user-select: none;
  -khtml-user-select: none; -moz-user-select: none;
  -ms-user-select: none; user-select: none;
  padding: 0 4px; width: 4em;
  color: #aaaaaa;
}
pre.numberSource { margin-left: 3em; border-left: 1px solid #aaaaaa;  padding-left: 4px; }
div.sourceCode
{  }
@media screen {
    a.sourceLine::before { text-decoration: underline; }
}
code span.al { color: #ff0000; font-weight: bold; } /* Alert */
code span.an { color: #60a0b0; font-weight: bold; font-style: italic; } /* Annotation */
code span.at { color: #7d9029; } /* Attribute */
code span.bn { color: #40a070; } /* BaseN */
code span.bu { } /* BuiltIn */
code span.cf { color: #333; font-weight: bold; } /* ControlFlow */
code span.ch { color: #4070a0; } /* Char */
code span.cn { color: #880000; } /* Constant */
code span.co { color: #998; font-style: italic; } /* Comment */
code span.cv { color: #60a0b0; font-weight: bold; font-style: italic; } /* CommentVar */
code span.do { color: #ba2121; font-style: italic; } /* Documentation */
code span.dt { color: #902000; } /* DataType */
code span.dv { color: #008080; } /* DecVal */
code span.er { color: #ff0000; font-weight: bold; } /* Error */
code span.ex { } /* Extension */
code span.fl { color: #008080; } /* Float */
code span.fu { color: #06287e; } /* Function */
code span.im { } /* Import */
code span.in { color: #60a0b0; font-weight: bold; font-style: italic; } /* Information */
code span.kw { color: #333; font-weight: bold; } /* Keyword */
code span.op { color: #666666; } /* Operator */
code span.ot { color: #008080; } /* Other */
code span.pp { color: #bc7a00; } /* Preprocessor */
code span.sc { color: #4070a0; } /* SpecialChar */
code span.ss { color: #bb6688; } /* SpecialString */
code span.st { color: #d14; } /* String */
code span.va { color: #008080; } /* Variable */
code span.vs { color: #4070a0; } /* VerbatimString */
code span.wa { color: #60a0b0; font-weight: bold; font-style: italic; } /* Warning */

.hljs {
  display: block;
  overflow-x: auto;
  padding: 0.5em;
  color: #333;
  background: #f8f8f8;
}

.hljs-comment,
.hljs-quote {
  color: #998;
  font-style: italic;
}

.hljs-keyword,
.hljs-selector-tag,
.hljs-subst {
  color: #333;
  font-weight: bold;
}

.hljs-number,
.hljs-literal,
.hljs-variable,
.hljs-template-variable,
.hljs-tag .hljs-attr {
  color: #008080;
}

.hljs-string,
.hljs-doctag {
  color: #d14;
}

.hljs-title,
.hljs-section,
.hljs-selector-id {
  color: #900;
  font-weight: bold;
}

.hljs-subst {
  font-weight: normal;
}

.hljs-type,
.hljs-class .hljs-title {
  color: #458;
  font-weight: bold;
}

.hljs-tag,
.hljs-name,
.hljs-attribute {
  color: #000080;
  font-weight: normal;
}

.hljs-regexp,
.hljs-link {
  color: #009926;
}

.hljs-symbol,
.hljs-bullet {
  color: #990073;
}

.hljs-built_in,
.hljs-builtin-name {
  color: #0086b3;
}

.hljs-meta {
  color: #999;
  font-weight: bold;
}

.hljs-deletion {
  background: #fdd;
}

.hljs-addition {
  background: #dfd;
}

.hljs-emphasis {
  font-style: italic;
}

.hljs-strong {
  font-weight: bold;
}
.reveal section img { border: none; }
.reveal pre { width: 100%; font-size: .65em;}
.reveal h2  { font-family: sans-serif; }
.reveal { font-family: sans-serif; }

  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">

{% for section in slides %}
<section>
  {% for slide in section %}
  <section data-markdown>
    <textarea data-template>
{{ slide }}
    </textarea>
  </section>
  {% endfor%}
</section>
{% endfor %}
    </div>
  </div>

  <script src="{{ revealjs_url }}/dist/reveal.js"></script>
  <script src="{{ revealjs_url }}/plugin/zoom/zoom.js"></script>
  <script src="{{ revealjs_url }}/plugin/notes/notes.js"></script>
  <script src="{{ revealjs_url }}/plugin/search/search.js"></script>
  <script src="{{ revealjs_url }}/plugin/markdown/markdown.js"></script>
  <script src="{{ revealjs_url }}/plugin/highlight/highlight.js"></script>
  <script>
  Reveal.initialize({
  controls: true,
  progress: true,
  center: true,
  hash: true,
  disableLayout: false,
  plugins: [ RevealZoom, RevealNotes, RevealSearch, RevealMarkdown, RevealHighlight ]
  });
  </script>
  </body>
</html>
"""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("md", help="Markdown input file")
    parser.add_argument("-o", "--output", dest="html", help="HTML output file")
    return parser.parse_args()


REVEAL_JS_VERSION = "4.1.0"
REVEAL_ARCHIVE = (
    f"https://github.com/hakimel/reveal.js/archive/{REVEAL_JS_VERSION}.tar.gz"
)


def main():
    args = parse_args()
    if not args.html:
        args.html = args.md.replace(".md", ".html")
        if args.md == args.html:
            print(
                "You did not specified an output file, and I failed to guess it, "
                "please use the --output option"
            )
            sys.exit(1)
    tpl = jinja2.Template(TPL)

    root = Path(args.html).resolve().parent
    reveal_dir = f"reveal.js-{REVEAL_JS_VERSION}"
    reveal_path = root / reveal_dir
    if not reveal_path.exists():
        tarball = io.BytesIO(requests.get(REVEAL_ARCHIVE).content)
        tarfile.open(fileobj=tarball, mode="r:gz").extractall(root)

    with open(args.md) as f:
        md = f.read()

    sections = []
    for section in re.split("^# ", md, flags=re.M):
        if not section:
            continue
        slides = []
        for slide in re.split("^## ", section, flags=re.M):
            slide = re.sub("^::: notes$", '<aside class="notes">', slide, flags=re.M)
            slide = re.sub("^:::$", "</aside>", slide, flags=re.M)
            slides.append("## " + slide)
        sections.append(slides)

    with open(args.html, "w") as f:
        f.write(tpl.render(slides=sections, revealjs_url=reveal_dir))


if __name__ == "__main__":
    main()
