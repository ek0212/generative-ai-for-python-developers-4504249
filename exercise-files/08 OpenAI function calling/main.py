# https://platform.openai.com/docs/guides/function-calling
import openai
import os
import json
import requests
from colorama import Fore
from dotenv import load_dotenv


load_dotenv()
messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"
messages = [{"role": "system", "content": "You are a helpful assistant"}]

client = openai.OpenAI()


def generate_response(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools, #define the functions/toools
        tools_choice="auto",
    )
    return response.choices[0].message


def main():
    print(Fore.CYAN + "Bot: Hello, I am a helpful assistant. Type 'exit' to quit." + Fore.RESET)

    while True:
        user_input = input("You: ")

        if user_input == "exit":
            print("Goodbye!")
            break

        # Step 1: send the conversation and available functions to GPT
        response_message = generate_response(user_input)
        print(Fore.CYAN + "Bot: " + message_response.content + Fore.RESET)
        tool_calls = response_message.tool_calls

        # Step 2: check if GPT wanted to call a function and generate an extended response
        if tool_calls:
        # Step 3: call the function
            ailable_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        
        # Step 4: send the info on the function call and function response to GPT
        # extend conversation with assistant's reply
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        
if __name__ == "__main__":
    main()