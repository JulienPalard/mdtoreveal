# mdtoreveal

It's an extremly basic
[Markdown](https://daringfireball.net/projects/markdown/) to
[reveal.js](https://revealjs.com/) conversion tool.

Yes reveal already supports Markdown, but it needs specifically
crafted Markdown with strange separators which I don't personally
like. And yes you can also do this using pandoc but it mess with
syntax highlighting by handling it.

## Usage

    mdtoreveal my_prez.md --output my_prez.html

It's also allowed to skip the output file, so its name is guessed, the
previous command is equivalent to the following one:

    mdtoreveal my_prez.md

## Syntax

Let's start with pure Markdown:

    # Big titles makes reveal.js "columns"

    ## Sub titles make reveal.js "slides" inside columns.

    ```python
    print("Syntax highlighting works")
    ```

    ::: notes

    Look, this is a personal note, it's not mandatory to use them, but you still can.
    Everything betwen `::: notes` and the next slide is only visible by the presenter.

    ## 2nd slide

    Blah blah …


## Example

It converts
[this](https://framagit.org/JulienPalard/atelier-perf/-/blob/master/perf.md)
into [this](https://julienpalard.frama.io/atelier-perf/perf.html)
(this one uses a
[.gitlab-ci.yml](https://framagit.org/JulienPalard/atelier-perf/-/blob/master/.gitlab-ci.yml)
to publish on push).


## Configuration

There's not, deal with it, don't loose your time on fine-tuning, and
focus on your presentation.

Still, you prefer a dark theme? It's unreadable on video projectors,
keep this one, trust me.

You want bigger code blocks? You already have 12 lines and 61 columns,
if you stuff more, it won't be readable anyway, stick to it.

You want a bigger font for your code blocks, so it's still readable
from the end of the room? I can understand that, I used to use a
bigger one too, let's talk in the issues.


## You're using a Makefile?

Me too ♥ this should do:

```Makefile
SRCS := $(wildcard *.md)
HTML := $(SRCS:.md=.html)

.PHONY: static
static: $(HTML)

%.html: %.md
	mdtoreveal $< -o $@
```
