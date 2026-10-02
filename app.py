# app.py
# Block 12 — the PROJECT: give your agent a chat UI with Gradio.
# Run:  python app.py     then open the local link it prints.
import os

import gradio as gr
from dotenv import load_dotenv
from agent import agent          # the function from agent.py

load_dotenv()
share_enabled = os.getenv("GRADIO_SHARE", "true").strip().lower() == "true"


def chat(message, history):
    # Gradio fills in `message` (newest) and `history` (past turns) for you.
    # Homework hint: pass `history` into your agent to give it memory!
    return agent(message)


_, local_url, share_url = gr.ChatInterface(
    fn=chat,
    title="🛍️ Smart Shop Assistant",
    description="Ask me the price of shoes, hat, bag, shorts or pants — I'll look it up.",
).launch(share=share_enabled)

print(f"Local URL: {local_url}")
print(f"Public URL: {share_url or 'Unavailable'}")
