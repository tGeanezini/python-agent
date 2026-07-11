import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("No API key was provided")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "user", "content": args.user_prompt},
]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def generate_messages(messages, client):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if response.usage is None:
        raise RuntimeError("There was an issue processing your request")

    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\n"
            + f"Prompt tokens: {response.usage.prompt_tokens}\n"
            + f"Response tokens: {response.usage.completion_tokens}"
        )

    print(response.choices[0].message.content)


generate_messages(messages, client)
