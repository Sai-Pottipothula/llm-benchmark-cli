import os
import time
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from tabulate import tabulate

from cache import get_cached_response, save_cached_response

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

OPENAI_MODEL = "gpt-4.1-mini"
CLAUDE_MODEL = "claude-haiku-4-5"


def ask_gpt(prompt, system):
    cached = get_cached_response("gpt", prompt, system)

    if cached:
        cached["cached"] = True
        return cached

    start = time.time()

    response = openai_client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )

    latency = time.time() - start

    result = {
        "model": OPENAI_MODEL,
        "answer": response.output_text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "latency": round(latency, 2),
        "cached": False,
    }

    save_cached_response("gpt", prompt, system, result)

    return result


def ask_claude(prompt, system):
    cached = get_cached_response("claude", prompt, system)

    if cached:
        cached["cached"] = True
        return cached

    start = time.time()

    response = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=500,
        system=system,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    latency = time.time() - start

    result = {
        "model": CLAUDE_MODEL,
        "answer": response.content[0].text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "latency": round(latency, 2),
        "cached": False,
    }

    save_cached_response("claude", prompt, system, result)

    return result


def stream_gpt(prompt, system):
    print("\n===== GPT STREAM =====\n")

    stream = openai_client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)

    print("\n")


def stream_claude(prompt, system):
    print("\n===== CLAUDE STREAM =====\n")

    with anthropic_client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=500,
        system=system,
        messages=[
            {"role": "user", "content": prompt},
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument(
        "--system",
        default="You are a helpful assistant.",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
    )

    args = parser.parse_args()

    if args.stream:
        stream_gpt(args.prompt, args.system)
        stream_claude(args.prompt, args.system)
        return

    gpt_result = ask_gpt(args.prompt, args.system)
    claude_result = ask_claude(args.prompt, args.system)

    table = [
        [
            "GPT",
            gpt_result["answer"],
            gpt_result["input_tokens"],
            gpt_result["output_tokens"],
            gpt_result["latency"],
            gpt_result["cached"],
        ],
        [
            "Claude",
            claude_result["answer"],
            claude_result["input_tokens"],
            claude_result["output_tokens"],
            claude_result["latency"],
            claude_result["cached"],
        ],
    ]

    print(
        tabulate(
            table,
            headers=[
                "Provider",
                "Answer",
                "Input Tokens",
                "Output Tokens",
                "Latency",
                "Cached",
            ],
            tablefmt="grid",
        )
    )


if __name__ == "__main__":
    main()