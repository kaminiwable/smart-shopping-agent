# app.py
# Gradio chat interface for the shopping assistant.
# Run: python app.py
import os

import gradio as gr
from dotenv import load_dotenv
from agent import agent          # the function from agent.py

load_dotenv()
share_enabled = os.getenv("GRADIO_SHARE", "true").strip().lower() == "true"


def chat(message, history):
    return agent(message)


_, local_url, share_url = gr.ChatInterface(
    fn=chat,
    title="🛍️ Smart Shop Assistant",
    description="Ask me the price of shoes, hat, bag, shorts or pants — I'll look it up.",
).launch(share=share_enabled)

print(f"Local URL: {local_url}")
print(f"Public URL: {share_url or 'Unavailable'}")
