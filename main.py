import json
import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from functions.call_function import available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("No API key was provided")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
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
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("There was an issue processing your request")

    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\n"
            + f"Prompt tokens: {response.usage.prompt_tokens}\n"
            + f"Response tokens: {response.usage.completion_tokens}"
        )

    message = response.choices[0].message

    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")


generate_messages(messages, client)
