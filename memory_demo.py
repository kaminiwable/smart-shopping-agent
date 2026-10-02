# memory_demo.py
# Optional standalone example: manually supplied chat history with LangChain.
# Run: python memory_demo.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-20b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly tutor."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])
chain = prompt | model

# Sample conversation history supplied to the model.
history = [HumanMessage("My name is Aarav."), AIMessage("Hi Aarav!")]

answer = chain.invoke({"history": history, "question": "What's my name?"})
print(answer.content)
