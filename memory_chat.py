# memory_chat.py
# Optional standalone example: a LangChain chat loop with in-memory history.
# Run: python memory_chat.py (type 'quit' to stop)
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-20b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant. Use the conversation history to stay consistent."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
chain = prompt | model

history = []

print("Chat with the bot (type 'quit' to exit).")
while True:
    question = input("You: ")
    if question.strip().lower() in {"quit", "exit"}:
        break

    answer = chain.invoke(
        {"history": history, "question": question}).content
    print("Bot:", answer)

    history.append(HumanMessage(question))
    history.append(AIMessage(answer))
    print(f"   (history now has {len(history)} messages)")
