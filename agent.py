import json
from anthropic import Anthropic
from tools import web_search, pubmed_search

client = Anthropic()

TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for recent nutrition information, practical advice, and health news.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"],
        },
    },
    {
        "name": "pubmed_search",
        "description": "Search PubMed for peer-reviewed scientific research papers on nutrition, diet, and health.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The research query"}
            },
            "required": ["query"],
        },
    },
]

SYSTEM_PROMPT = """You are Bagel, an expert nutrition advisor who gives evidence-based advice grounded in the latest scientific research.

When a user asks a nutrition question:
1. Search PubMed for recent peer-reviewed research on the topic
2. Use web search for practical, up-to-date context
3. Synthesize findings into clear, actionable advice tailored to their stated goal
4. Always cite your sources with paper titles and links
5. Be honest when evidence is mixed or evolving — nutrition science changes

Keep your tone conversational and encouraging. Never diagnose medical conditions or replace a doctor."""

TOOL_DISPATCH = {
    "web_search": web_search,
    "pubmed_search": pubmed_search,
}


def run_agent(user_message: str, goal: str, history: list) -> str:
    messages = []

    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})

    full_message = (
        f"My goal: {goal}\n\nQuestion: {user_message}" if goal.strip() else user_message
    )
    messages.append({"role": "user", "content": full_message})

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return ""

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    fn = TOOL_DISPATCH.get(block.name)
                    result = fn(block.input["query"]) if fn else {"error": "Unknown tool"}
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result),
                        }
                    )

            messages.append({"role": "user", "content": tool_results})
        else:
            break

    return "Something went wrong — please try again."
