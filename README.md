# Smart Shopping Agent

A small Python shopping assistant built with Gradio and Groq. It can look up sample product prices using a model-selected tool call. The repository also includes standalone LangChain memory and website-summarization examples from an AI engineering class.

## Features

- Gradio chat interface with an optional temporary public share link.
- Groq chat completions using `openai/gpt-oss-20b`.
- A sample in-memory product catalog and price lookup tool.
- Separate LangChain examples for chat memory and website summarization.
- A simple website text scraper built with Requests and Beautiful Soup.

## Project Structure

| File | Purpose |
| --- | --- |
| `app.py` | Starts the Gradio chat interface. |
| `agent.py` | Calls Groq and provides the product-price tool. |
| `memory_demo.py` | Demonstrates manually supplied chat history. |
| `memory_chat.py` | Demonstrates a conversational loop with in-memory history. |
| `summarizer_langchain.py` | Scrapes and summarizes a website with LangChain. |
| `scraper.py` | Fetches and extracts readable website text. |
| `requirements.txt` | Python dependencies. |
| `.env.example` | Safe environment-variable template. |

## Prerequisites

- Python 3.10 or newer.
- A Groq account and API key for model-backed examples.
- Internet access for Groq requests, website scraping, and optional Gradio sharing.

## Installation

From the project directory, create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env`, then replace the placeholder with a Groq API key from [Groq Console](https://console.groq.com/keys). Keep `.env` private and do not commit it.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS or Linux:

```bash
cp .env.example .env
```

Edit `.env` locally and set `GROQ_API_KEY`. `GRADIO_SHARE` controls whether Gradio attempts to create a temporary public tunnel; it defaults to `true` in the example. Set it to `false` on hosting platforms that provide their own public URL.

If an API key was previously exposed, revoke it in the provider console and create a replacement before using or publishing the project.

## Run

Start the web application:

```powershell
python app.py
```

Open the local URL printed in the terminal. With `GRADIO_SHARE=true`, Gradio also attempts to print a temporary public URL. Share-link creation can fail when Gradio's sharing service is unavailable or a network, proxy, VPN, or firewall blocks its tunnel. Set `GRADIO_SHARE=false` to disable that attempt.

Other examples can be run independently:

```powershell
python agent.py
python memory_demo.py
python memory_chat.py
python summarizer_langchain.py
python scraper.py
```

## Example Usage

In the chat interface, ask: `What is the price of shoes?` The sample catalog contains shoes, hat, bag, shorts, and pants. The standalone agent can also be run with `python agent.py`.

## Tests

There is no automated test suite yet. Check Python syntax with:

```powershell
python -m compileall -q agent.py app.py memory_chat.py memory_demo.py scraper.py summarizer_langchain.py
```

Running `python agent.py` is a live smoke test and requires a valid `GROQ_API_KEY` and network access.

## Deployment

The app can be deployed to a Gradio-compatible host such as Hugging Face Spaces. Create a Gradio Space, add the project files and `requirements.txt`, and configure `GROQ_API_KEY` as a platform secret rather than uploading `.env`. Use the public URL supplied by the hosting platform and set `GRADIO_SHARE=false` there to avoid requesting a separate temporary tunnel. Never publish API keys or the generated `.gradio` certificate.

## Known Limitations

- Product data is a small hard-coded example, not a live inventory system.
- The model decides when to call the price tool; natural-language variants may not always map to a catalog item.
- Model output can be incorrect or answer beyond the shopping catalog; it is not a general-purpose source of verified facts.
- Website extraction is basic and does not render JavaScript pages.
- Gradio share URLs are temporary and depend on Gradio's sharing service and network access.

## License

No license has been selected for this project. Until a license is added, standard copyright applies and reuse or redistribution is not granted by this repository.
