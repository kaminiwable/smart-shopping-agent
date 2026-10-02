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


def check_budget(items, budget):
    normalized_items = [item.strip().lower() for item in items]
    unknown_items = [item for item in normalized_items if item not in PRICES]
    if unknown_items:
        return f"I don't have prices for: {', '.join(unknown_items)}."

    total = sum(PRICES[item] for item in normalized_items)
    item_details = ", ".join(
        f"{item.title()} ₹{PRICES[item]:,}" for item in normalized_items)
    if total <= budget:
        return (
            f"Yes. {item_details} total ₹{total:,}. "
            f"You would have ₹{budget - total:,} left."
        )

    return (
        f"No. {item_details} total ₹{total:,}, which is "
        f"₹{total - budget:,} over your ₹{budget:,} budget."
    )


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
}, {
    "type": "function",
    "function": {
        "name": "check_budget",
        "description": "Use this for questions about whether a budget covers one or more catalog items. It calculates the exact total and amount left or over budget.",
        "parameters": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {"type": "string", "enum": list(PRICES)},
                },
                "budget": {"type": "integer"},
            },
            "required": ["items", "budget"],
        },
    },
}]

MAX_TOOL_ROUNDS = 5


# Let the model decide whether to look up a product price.
def agent(user_message):
    messages = [{"role": "user", "content": user_message}]
    tool_rounds = 0

    while tool_rounds < MAX_TOOL_ROUNDS:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b", messages=messages, tools=tools)
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "check_budget":
                return check_budget(args["items"], args["budget"])

            result = get_price(args["item"])
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })
        tool_rounds += 1

    return "I couldn't complete that request after several product lookups."


if __name__ == "__main__":
    print(agent("How much are the shoes?"))
    print(agent("Hi! What can you help with?"))
