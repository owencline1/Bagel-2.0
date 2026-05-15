import json
from anthropic import Anthropic
from tools import pubmed_search

client = Anthropic()

SYSTEM_PROMPT = """You are Bagel, an expert nutrition advisor who gives evidence-based advice grounded in the latest peer-reviewed science.

You will be given the user's question along with a set of recent PubMed studies (titles, journals, authors, and abstracts) that were retrieved for that question. Your job is to read those studies carefully and synthesize a thorough, actionable response.

Rules:
- Ground your answer in the studies provided — cite them by title and include their PubMed URLs
- Go deep: explain mechanisms, dosages, effect sizes, and the context behind the findings — not just surface-level takeaways
- Translate scientific language into clear, practical advice the user can act on
- Be honest when evidence is mixed, limited, or evolving — nutrition science changes
- If none of the retrieved studies actually address the question, say so plainly rather than padding the response
- Keep your tone conversational and encouraging
- Never diagnose medical conditions or replace a doctor"""


def run_agent(user_message: str, goal: str, history: list) -> str:
    pubmed_results = pubmed_search(user_message)

    if not pubmed_results:
        return "I couldn't find any studies on this topic in the scientific literature. Try rephrasing or asking about a related topic."

    messages = []
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})

    research_block = json.dumps(pubmed_results, indent=2)
    goal_line = f"My goal: {goal}\n\n" if goal.strip() else ""
    full_message = (
        f"{goal_line}Question: {user_message}\n\n"
        f"Retrieved PubMed studies:\n{research_block}"
    )
    messages.append({"role": "user", "content": full_message})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=messages,
        timeout=90.0,
    )

    for block in response.content:
        if hasattr(block, "text"):
            return block.text

    return "Something went wrong — please try again."
