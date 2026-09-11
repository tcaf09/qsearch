# qsearch

A fast terminal tool for quick searches and AI-assisted summaries — not a full browser, just answers.

## Features

- Search the web without leaving your terminal
- `[S]` to summarize any result page, `[Q]` to quit
- `--quick` for a one-shot AI answer with no search results shown
- Filter by site with `--site`

## Install

```bash
pipx install git+https://github.com/tcaf09/qsearch.git
```

Or with plain pip (inside a virtualenv):

```bash
pip install git+https://github.com/tcaf09/qsearch.git
```

## Setup

qsearch uses the Gemini API for summarization. Set your API key as an environment variable:

```bash
export GEMINI_API_KEY="your-key-here"
```

## Usage

```bash
qsearch "your query here"
qsearch "your query" -n 10
qsearch "your query" --site reddit.com
qsearch --quick "explain how TCP handshakes work"
```

| Key | Action |
|-----|--------|
| `s` | Summarize the selected page |
| `q` | Quit |

