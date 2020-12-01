# md2reveal

It's an extremly basic
[Markdown](https://daringfireball.net/projects/markdown/) to
[reveal.js](https://revealjs.com/) conversion tool.

Yes reveal already supports Markdown, but it needs specifically
crafted Markdown with strange separators which I don't personally
like. And yes you can also do this using pandoc but it mess with
syntax highlighting by handling it.

## Usage

    md2reveal my_prez.md --output my_prez.html

It's also allowed to skip the output file, so its name is guessed, the
previous command is equivalent to the following one:

    md2reveal my_prez.md


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
	md2reveal $< -o $@
```
