# summarizer_langchain.py
# Optional standalone example: summarize a website with LangChain.
# Run: python summarizer_langchain.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from scraper import fetch_website_contents   # Fetch page text for the summary.

load_dotenv()

# Prompt template for scraped website text.
prompt = ChatPromptTemplate.from_template(
    "Give a short, friendly summary of this website:\n\n{website}"
)

# Groq chat model wrapped for LangChain.
model = ChatGroq(model="openai/gpt-oss-20b", temperature=0.3)

# Convert the model response to plain text.
parser = StrOutputParser()

# Compose prompt, model, and output parser.
chain = prompt | model | parser


def summarize(url):
    return chain.invoke({"website": fetch_website_contents(url)})


if __name__ == "__main__":
    print(summarize("https://anthropic.com"))
