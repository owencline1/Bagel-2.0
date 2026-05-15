# Bagel 2.0

An evidence-based nutrition advisor that answers your questions using real peer-reviewed research from PubMed.

Ask Bagel a nutrition question, and it pulls actual scientific studies, reads them, and gives you a clear, practical answer with citations to the papers it used.

## How to use Bagel (for total beginners)

Once Bagel is running, you'll see a simple page in your browser with two boxes:

**1. Your Goal (optional but helpful)**

This is where you tell Bagel a little about you and what you're trying to achieve. The more specific you are, the more tailored the advice.

Examples:
- `lose 15 pounds of fat while keeping muscle`
- `build muscle as a 25 year old vegetarian`
- `improve my energy levels — I crash every afternoon`
- `eat better for a half marathon in 3 months`

You only need to fill this out once at the start of a conversation. Bagel will remember it.

**2. Your question**

Type any nutrition question you're curious about. Don't worry about phrasing it perfectly — ask it the way you'd ask a friend.

Examples to try:
- `Is intermittent fasting actually effective for fat loss?`
- `How much protein do I really need per day?`
- `Are seed oils as bad as people on the internet say?`
- `What does the research say about creatine for women?`
- `Does eating before bed make you gain weight?`

Hit **Send** (or press Enter) and wait around 20-30 seconds. Bagel will search PubMed, read the studies, and write you an answer with the papers it referenced — you can click any citation to read the original research.

**Tips for getting good answers**

- Be specific. "Is keto good?" is vague. "Is keto effective for fat loss in someone with insulin resistance?" gets a much better answer.
- Follow up. If Bagel's answer raises new questions, just ask the next one — the conversation stays in context.
- Trust the citations. If Bagel says something interesting, click through to the study and read the source.
- Bagel won't make stuff up. If the research doesn't address your question, it'll tell you rather than guessing.

## How it works under the hood

1. You type a question
2. Bagel searches PubMed for the most recent relevant studies and downloads their abstracts
3. Claude (the AI model behind Bagel) reads those abstracts and writes a synthesized response with citations

The whole pipeline runs in a single AI call, so responses come back in around 20-30 seconds.

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

The `.env` file is gitignored so your key won't be committed to GitHub.

### Run

```bash
python app.py
```

Then open your browser to **http://localhost:7860** and start asking questions.

## Project structure

| File | Purpose |
|---|---|
| `app.py` | The Gradio web interface |
| `agent.py` | The synthesis pipeline (PubMed search → Claude) |
| `tools.py` | PubMed and web search functions |
| `.env` | Your API key (not committed) |

## Tech stack

- **[Anthropic Claude](https://www.anthropic.com)** — the language model that reads studies and writes responses
- **[Gradio](https://gradio.app)** — the web interface
- **[PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/)** — scientific literature search

## A note on what Bagel is and isn't

Bagel is a research assistant. It cites real studies and translates the science into practical advice. It is **not** a doctor and shouldn't replace medical care — if you have a real health concern, talk to a professional.
