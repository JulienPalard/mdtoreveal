import re
import tarfile
import io
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
  <link rel="stylesheet" href="{{ revealjs_url }}/plugin/highlight/monokai.css" id="highlight-theme">
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
    parser.add_argument("html", help="HTML output file")
    return parser.parse_args()


REVEAL_JS_VERSION = "4.1.0"
REVEAL_ARCHIVE = (
    f"https://github.com/hakimel/reveal.js/archive/{REVEAL_JS_VERSION}.tar.gz"
)


def main():
    args = parse_args()
    tpl = jinja2.Template(TPL)

    root = Path(args.html).resolve().parent
    reveal_path = root / f"reveal.js-{REVEAL_JS_VERSION}"
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
        f.write(tpl.render(slides=sections, revealjs_url=reveal_path))


if __name__ == "__main__":
    main()
