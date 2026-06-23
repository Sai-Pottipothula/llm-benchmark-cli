import "dotenv/config";
import OpenAI from "openai";
import Anthropic from "@anthropic-ai/sdk";
import {
  getCachedResponse,
  saveCachedResponse,
} from "./cache.js";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const prompt = process.argv[2];
const isStreaming = process.argv.includes("--stream");

const system = "You are a helpful assistant.";

async function askGPT(prompt, system) {
  const cached = await getCachedResponse("gpt", prompt, system);

  if (cached) {
    console.log("Using cached GPT response");
    return cached;
  }

  const start = Date.now();

  const response = await openai.responses.create({
    model: "gpt-4.1-mini",
    input: [
      { role: "system", content: system },
      { role: "user", content: prompt },
    ],
  });

  const result = {
    provider: "GPT",
    model: "gpt-4.1-mini",
    answer: response.output_text,
    input_tokens: response.usage.input_tokens,
    output_tokens: response.usage.output_tokens,
    latency: Number(((Date.now() - start) / 1000).toFixed(2)),
  };

  await saveCachedResponse("gpt", prompt, system, result);

  return result;
}

async function askClaude(prompt, system) {
  const cached = await getCachedResponse("claude", prompt, system);

  if (cached) {
    console.log("Using cached Claude response");
    return cached;
  }

  const start = Date.now();

  const response = await anthropic.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 500,
    system: system,
    messages: [{ role: "user", content: prompt }],
  });

  const result = {
    provider: "Claude",
    model: "claude-haiku-4-5",
    answer: response.content[0].text,
    input_tokens: response.usage.input_tokens,
    output_tokens: response.usage.output_tokens,
    latency: Number(((Date.now() - start) / 1000).toFixed(2)),
  };

  await saveCachedResponse("claude", prompt, system, result);

  return result;
}

async function streamGPT() {
  console.log("\n===== GPT STREAM =====\n");

  const response = await openai.responses.create({
    model: "gpt-4.1-mini",
    input: [
      { role: "system", content: system },
      { role: "user", content: prompt },
    ],
    stream: true,
  });

  for await (const event of response) {
    if (event.type === "response.output_text.delta") {
      process.stdout.write(event.delta);
    }
  }

  console.log("\n");
}

async function streamClaude() {
  console.log("\n===== CLAUDE STREAM =====\n");

  const stream = anthropic.messages.stream({
    model: "claude-haiku-4-5",
    max_tokens: 500,
    system: system,
    messages: [{ role: "user", content: prompt }],
  });

  for await (const event of stream) {
    if (
      event.type === "content_block_delta" &&
      event.delta &&
      event.delta.text
    ) {
      process.stdout.write(event.delta.text);
    }
  }

  console.log("\n");
}

async function main() {
  try {
    if (isStreaming) {
      await streamGPT();
      await streamClaude();
      return;
    }

    const gpt = await askGPT(prompt, system);
    const claude = await askClaude(prompt, system);
    
console.log("\n================ GPT RESULT ================");
console.log(`Model: ${gpt.model}`);
console.log(`Input Tokens: ${gpt.input_tokens}`);
console.log(`Output Tokens: ${gpt.output_tokens}`);
console.log(`Latency: ${gpt.latency}s`);
console.log("\nAnswer:");
console.log(gpt.answer);

console.log("\n================ CLAUDE RESULT ================");
console.log(`Model: ${claude.model}`);
console.log(`Input Tokens: ${claude.input_tokens}`);
console.log(`Output Tokens: ${claude.output_tokens}`);
console.log(`Latency: ${claude.latency}s`);
console.log("\nAnswer:");
console.log(claude.answer);
  } catch (error) {
    console.error("Error:", error.message);
  }
}

export { askGPT, askClaude };

if (process.argv[1].endsWith("ask.js")) {
  main();
}