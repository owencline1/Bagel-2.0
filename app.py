import os
from dotenv import load_dotenv

load_dotenv()

import gradio as gr
from agent import run_agent

if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "paste_your_key_here":
    raise SystemExit("No API key found. Open the .env file and paste your Anthropic API key.")


def chat(message: str, goal: str, history: list):
    if not message.strip():
        return history, ""
    response = run_agent(message, goal, history)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    return history, ""


with gr.Blocks(title="Bagel 2.0") as app:
    gr.Markdown("# Bagel 2.0\n### Evidence-based nutrition advice from the latest research")

    goal_input = gr.Textbox(
        label="Your Goal",
        placeholder="e.g. lose fat while keeping muscle, build mass, improve energy levels...",
    )

    chatbot = gr.Chatbot(height=500, label="Bagel")

    with gr.Row():
        msg_input = gr.Textbox(
            placeholder="Ask a nutrition question...",
            label="Your question",
            scale=4,
        )
        send_btn = gr.Button("Send", variant="primary", scale=1)

    send_btn.click(
        chat,
        inputs=[msg_input, goal_input, chatbot],
        outputs=[chatbot, msg_input],
    )
    msg_input.submit(
        chat,
        inputs=[msg_input, goal_input, chatbot],
        outputs=[chatbot, msg_input],
    )

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft())
