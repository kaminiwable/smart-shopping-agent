# agent.py
# Groq-backed shopping agent with a tool for looking up product prices.
# Run: python agent.py
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq()

# Sample product catalog.
PRICES = {"shoes": 799, "hat": 399, "bag": 1420, "shorts": 1299, "pants": 1699}


# Price lookup exposed to the model as a tool.
def get_price(item):
    print(f"🔧 tool called: get_price({item})")        # so you SEE it happen
    return f"₹{PRICES.get(item.lower(), 'unknown')}"    # .get -> no crash if missing


# Tool schema sent with each model request.
tools = [{
    "type": "function",
    "function": {
        "name": "get_price",
        "description": "Get the price of a shop item the user asks about.",
        "parameters": {
            "type": "object",
            "properties": {"item": {"type": "string", "description": "the item name"}},
            "required": ["item"],
        },
    },
}]


# Let the model decide whether to look up a product price.
def agent(user_message):
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b", messages=messages, tools=tools)
    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = get_price(args["item"])
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b", messages=messages)
        msg = response.choices[0].message

    return msg.content


if __name__ == "__main__":
    print(agent("How much are the shoes?"))
    print(agent("Hi! What can you help with?"))
