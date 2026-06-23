import fs from "fs";
import { askGPT, askClaude } from "./ask.js";

const prompts = [
  "Explain APIs to a beginner.",
  "Write a professional email asking for a referral.",
  "Summarize what an LLM is in 5 bullet points.",
  "Write a Python function to reverse a string.",
  "Explain the difference between REST and GraphQL.",
  "Classify this message as billing, technical, or general: My card was charged twice.",
  "Give 3 startup ideas using AI.",
  "Explain JWT authentication.",
  "Write a SQL query to find duplicate emails.",
  "Give a simple analogy for tokenization.",
];

const system = "You are a helpful assistant.";

async function main() {
  const results = [];

  for (const prompt of prompts) {
    console.log(`Running: ${prompt.slice(0, 50)}...`);

    const gpt = await askGPT(prompt, system);
    const claude = await askClaude(prompt, system);

    results.push({ prompt, gpt, claude });
  }

  fs.writeFileSync("node/results.json", JSON.stringify(results, null, 2));
  console.log("Saved results to node/results.json");
}

main();