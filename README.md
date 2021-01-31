# poc-bt
POC scrapy + starlette background tasks

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```
export TWISTED_REACTOR="twisted.internet.asyncioreactor.AsyncioSelectorReactor"
uvicorn poc:app
http :8000/crawl query="teste"
```

## Problem

When hit <kbd>Ctrl</kbd> + <kbd>c</kbd>, scrapy closes event loop before uvicorn, and an exception is raised.
