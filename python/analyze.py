import json

# Pricing per 1M tokens
GPT_INPUT_PRICE = 0.40
GPT_OUTPUT_PRICE = 1.60

CLAUDE_INPUT_PRICE = 1.00
CLAUDE_OUTPUT_PRICE = 5.00


with open("python/results.json", "r") as f:
    results = json.load(f)


gpt_input = 0
gpt_output = 0
gpt_latency = 0

claude_input = 0
claude_output = 0
claude_latency = 0


for item in results:

    gpt = item["gpt"]
    claude = item["claude"]

    gpt_input += gpt["input_tokens"]
    gpt_output += gpt["output_tokens"]
    gpt_latency += gpt["latency"]

    claude_input += claude["input_tokens"]
    claude_output += claude["output_tokens"]
    claude_latency += claude["latency"]


# Cost calculations
gpt_cost = (
    (gpt_input / 1_000_000) * GPT_INPUT_PRICE +
    (gpt_output / 1_000_000) * GPT_OUTPUT_PRICE
)

claude_cost = (
    (claude_input / 1_000_000) * CLAUDE_INPUT_PRICE +
    (claude_output / 1_000_000) * CLAUDE_OUTPUT_PRICE
)

# Average latency
gpt_avg_latency = gpt_latency / len(results)
claude_avg_latency = claude_latency / len(results)

print("\n===== FINAL COMPARISON =====\n")

print("GPT")
print(f"Input Tokens: {gpt_input}")
print(f"Output Tokens: {gpt_output}")
print(f"Average Latency: {gpt_avg_latency:.2f} sec")
print(f"Estimated Cost: ${gpt_cost:.6f}")

print("\nClaude")
print(f"Input Tokens: {claude_input}")
print(f"Output Tokens: {claude_output}")
print(f"Average Latency: {claude_avg_latency:.2f} sec")
print(f"Estimated Cost: ${claude_cost:.6f}")