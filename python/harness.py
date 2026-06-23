import json
from python.ask import ask_gpt, ask_claude

prompts = [
    "Explain APIs to a beginner.",
    "Write a professional email asking for a referral.",
    "Summarize what an LLM is in 5 bullet points.",
    "Write a Python function to reverse a string.",
    "Explain the difference between REST and GraphQL.",
    "Classify this message as billing, technical, or general: My card was charged twice.",
    "Give 3 startup ideas using AI.",
    "Explain JWT authentication.",
    "Write a SQL query to find duplicate emails.",
    "Give a simple analogy for tokenization."
]

results = []

for prompt in prompts:
    print(f"Running: {prompt}")

    gpt = ask_gpt(prompt, "You are a helpful assistant.")
    claude = ask_claude(prompt, "You are a helpful assistant.")

    results.append({
        "prompt": prompt,
        "gpt": gpt,
        "claude": claude
    })

with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved results to results.json")