# Bagel 2.0

An evidence-based nutrition advisor that answers your questions using the latest peer-reviewed research from PubMed.

Ask a nutrition question, and Bagel pulls real scientific studies from PubMed, reads their abstracts, and synthesizes a clear, practical answer with citations to the studies it used.

## How it works

1. You type a nutrition question (and optionally a personal goal like "lose fat while keeping muscle")
2. Bagel searches PubMed for the most recent relevant studies and fetches their abstracts
3. Claude reads the abstracts and writes a synthesized, actionable response with citations and links

The whole pipeline runs in a single Claude call, so responses come back in around 20-30 seconds.

## Setup

### Requirements

- Python 3.10 or newer
- An Anthropic API key ([get one here](https://console.anthropic.com))

### Install

```bash
git clone https://github.com/owencline1/Bagel-2.0.git
cd Bagel-2.0
pip install -r requirements.txt
```

### Add your API key

Create a file named `.env` in the project folder and paste your key into it:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

The `.env` file is gitignored so your key won't be committed.

## Run

```bash
python app.py
```

Then open your browser to **http://localhost:7860** and ask away.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Gradio web UI |
| `agent.py` | The synthesis pipeline (PubMed search → Claude) |
| `tools.py` | PubMed and web search functions |
| `.env` | Your API key (not committed) |

## Tech stack

- **[Anthropic Claude](https://www.anthropic.com)** — language model for synthesis
- **[Gradio](https://gradio.app)** — web UI
- **[PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/)** — scientific literature search

## Notes

Bagel is a research assistant, not a doctor. It cites studies and translates the science into practical advice, but it won't diagnose conditions or replace medical care.
