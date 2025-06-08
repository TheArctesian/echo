# echo

This is the llm version of me so an echo of myself, far from perfect but maybe resonante. This is pretty much I am getting way to busy, and I want an assistant or a clone of me. I figured that if I use an Ollama model I could make a digital assistant for myself or at least have fun talking to myself and gain some insight off of that.

I had a heavy internal debate as to whether or not to use go or rust for this but flipped a coin and decided to stay with python. As this took me an hour to build rather than 2 hrs with go or 3 with rust.

To run:
Import your obsidian vault into data, adjust `Dockerfile` volumes if neeeded:

`docker-compose up -d`

`cp -r /path/to/your/obsidian/vault/* ./data/obsidian_vault/`

`docker-compose exec rag-app python ingest.py`

Use the API:

- Access the API at http://localhost:8000
- Endpoints:
  - POST /query - Query your vault with natural language
  - POST /search - Direct similarity search
  - POST /ingest - Re-ingest your vault after changes
