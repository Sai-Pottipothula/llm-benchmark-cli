# LLM API Benchmark - Claude vs GPT

A CLI tool that sends prompts to both Anthropic Claude and OpenAI GPT, compares their responses side-by-side, and benchmarks them across latency, token usage, and cost. Built in both Python and Node.js.

---

## What it does

- Sends any prompt to Claude and GPT simultaneously
- Prints responses with token counts and latency
- Supports streaming (tokens print as they arrive)
- Supports custom system prompts via `--system`
- Caches responses in SQLite so repeated prompts don't cost money
- Runs a 10-prompt benchmark harness and stores results in JSON
- Calculates total cost, average latency, and token usage

---

## Results (10 prompts, mix of factual/coding/creative/reasoning)

| Model | Input Tokens | Output Tokens | Avg Latency | Estimated Cost |
|-------|-------------|---------------|-------------|----------------|
| GPT-4.1 Mini | 264 | 2,230 | 3.73s | $0.003674 |
| Claude Haiku | 233 | 3,198 | 3.36s | $0.016223 |

**Claude writes more, costs more. GPT is 4x cheaper for similar quality.**

---

## Recommendation

For a startup doing customer-support classification, **pick GPT-4.1 Mini**.

It's 4x cheaper than Claude Haiku, slightly faster on average, and handles classification tasks (billing vs technical vs general) accurately. Claude shines on longer reasoning and structured explanations — worth considering if response quality matters more than cost.

---

## Project Structure

```
llm-api-benchmark/
├── python/
│   ├── ask.py          # CLI tool — send prompt to both models
│   ├── cache.py        # SQLite caching
│   ├── harness.py      # Run 10 prompts, save to results.json
│   ├── analyze.py      # Calculate cost, latency, token totals
│   └── results.json
├── node/
│   ├── ask.js          # Same CLI tool in Node.js
│   ├── cache.js        # SQLite caching
│   ├── harness.js      # Benchmark harness
│   ├── analyze.js      # Cost analysis
│   └── results.json
├── .env                # API keys (not committed)
├── requirements.txt
└── package.json
```

---

## Setup

**Clone the repo**
```bash
git clone <your-repo-url>
cd llm-api-benchmark
```

**Add your API keys** — create a `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

**Python**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Node.js**
```bash
npm install
```

---

## Usage

**Python**
```bash
# Basic
cd python && python ask.py "what is machine learning?"

# With system prompt
python ask.py "who are you?" --system "You are a pirate"

# Streaming
python ask.py "explain transformers" --stream

# Run benchmark
python harness.py
python analyze.py
```

**Node.js**
```bash
# Basic
node node/ask.js "what is machine learning?"

# Streaming
node node/ask.js "explain transformers" --stream

# Run benchmark
node node/harness.js
node node/analyze.js
```

---

## Caching

Responses are cached in SQLite. Run the same prompt twice and the second call is instant and free. Delete `cache.db` to clear it.

---

## Tech Stack

Python · Node.js · Anthropic SDK · OpenAI SDK · SQLite · dotenv