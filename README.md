# First API Calls: Claude vs GPT

## Goal

The goal of this project is to make working API calls to both OpenAI GPT and Anthropic Claude using Python and Node.js. The project compares both models across multiple prompts using latency, token usage, response quality, streaming performance, caching, and estimated API cost.

This project demonstrates:

- API integration
- Environment variable management
- CLI development
- Streaming responses
- SQLite caching
- JSON result storage
- Model benchmarking
- Cost analysis

---

# Features

- Sends prompts to both GPT and Claude
- Python and Node.js implementations
- Supports streaming responses
- Supports custom system prompts
- Measures latency for each response
- Tracks input and output tokens
- Stores benchmark results in JSON format
- Calculates estimated API cost
- Implements SQLite caching for repeated prompts
- Compares both models on factual, reasoning, creative, and coding prompts

---

# Technologies Used

## Python

- Python 3
- OpenAI SDK
- Anthropic SDK
- dotenv
- sqlite3
- tabulate

## Node.js

- Node.js
- openai
- @anthropic-ai/sdk
- sqlite3
- dotenv

## Other

- JSON
- Command Line Interface (CLI)

---

# Project Setup

## 1. Clone the Repository

```bash
git clone <your-github-repo-link>
cd first-api-calls
```

---

# Python Setup

## 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# Node.js Setup

## 4. Install Node.js Dependencies

```bash
npm install
```

---

# Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

API keys are securely stored using environment variables and are never hardcoded into source code.

---

# Running the Project

# Python Version

## Run Single Prompt Comparison

```bash
python ask.py "Explain APIs in simple terms"
```

## Run with System Prompt

```bash
python ask.py "Explain APIs" --system "You are a beginner-friendly software tutor."
```

## Run Streaming Mode

```bash
python ask.py "Explain transformers in deep learning" --stream
```

---

# Node.js Version

## Run Single Prompt Comparison

```bash
node ask.js "Explain APIs in simple terms"
```

## Run Streaming Mode

```bash
node ask.js "Explain transformers in deep learning" --stream
```

---

# Streaming Support

Streaming mode prints tokens in real time as the models generate responses.

## GPT Streaming

Uses:

```javascript
stream: true
```

## Claude Streaming

Uses:

```javascript
anthropic.messages.stream()
```

Streaming was implemented successfully for both Python and Node.js versions.

---

# SQLite Caching

The project includes SQLite-based response caching.

Repeated prompts with the same provider and system prompt are loaded from the local cache instead of making additional paid API calls.

Benefits:

- Reduces API cost
- Speeds up repeated testing
- Useful during benchmarking and development

Cache database:

```text
cache.db
```

The cache database is excluded from GitHub using `.gitignore`.

---

# Benchmark Harness

The benchmark harness runs multiple prompts against both models and stores the results in `results.json`.

Run:

```bash
python harness.py
```

Example prompt categories:

- Factual questions
- Coding questions
- Reasoning tasks
- Creative writing
- Classification prompts

---

# Analyze Results

Run:

```bash
python analyze.py
```

This calculates:

- Total input tokens
- Total output tokens
- Average latency
- Estimated API cost

---

# Comparison Summary

| Model | Total Input Tokens | Total Output Tokens | Average Latency | Estimated Cost |
|---|---:|---:|---:|---:|
| GPT | Add your values here | Add your values here | Add your values here | Add your values here |
| Claude | Add your values here | Add your values here | Add your values here | Add your values here |

---

# Quality Observations

| Prompt Type | GPT | Claude |
|---|---|---|
| Factual Questions | Fast and concise | Detailed and structured |
| Coding Tasks | Practical code generation | Better explanations |
| Reasoning Tasks | Efficient and direct | Strong step-by-step reasoning |
| Creative Writing | Short and clean responses | More polished writing style |
| Classification Tasks | Very cost-effective | Accurate but higher cost |

---

# Recommendation

For a startup that needs the cheapest accurate model for customer-support classification, GPT-4.1 Mini is the better initial choice.

GPT-4.1 Mini provides strong classification quality while maintaining significantly lower token costs compared to Claude Haiku. This makes it more suitable for high-volume workflows such as:

- Support ticket classification
- Intent detection
- Request routing
- Sentiment tagging
- Automated customer workflows

Claude performs very well for detailed reasoning and long-form explanation tasks, but GPT offers a better balance between cost, speed, and accuracy for lightweight production classification systems.

---

# Project Structure

```text
first-api-calls/
├── ask.py
├── ask.js
├── cache.py
├── cache.js
├── harness.py
├── analyze.py
├── cache.db
├── results.json
├── requirements.txt
├── package.json
├── package-lock.json
├── README.md
├── .gitignore
└── .env
```

---

# Security Notes

- API keys are stored using environment variables
- `.env` is excluded using `.gitignore`
- No secrets are committed to GitHub

---

# Future Improvements

Potential future enhancements:

- Add Gemini or Llama integration
- Add response quality scoring
- Build a simple web dashboard
- Add parallel request execution
- Add retry and rate-limit handling
- Export benchmark results to CSV

---

# Learning Outcomes

This project helped build understanding of:

- LLM APIs
- Prompt engineering
- Streaming inference
- SQLite caching
- Token accounting
- AI model benchmarking
- Cost estimation
- Python CLI development
- Node.js SDK usage
- JSON processing
- API latency analysis

---