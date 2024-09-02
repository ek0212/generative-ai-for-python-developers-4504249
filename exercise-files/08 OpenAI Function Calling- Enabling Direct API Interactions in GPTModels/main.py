# https://platform.openai.com/docs/guides/function-calling
# https://openweathermap.org/current
# https://openweathermap.org/api/geocoding-api

# Import necessary libraries
import openai  # OpenAI client library for accessing AI models
import json  # For handling JSON data
from colorama import Fore  # For colored text output in the terminal
from dotenv import load_dotenv  # For loading environment variables from a .env file
from utils import get_current_weather  # Custom utility function for getting current weather

# Load environment variables from the .env file
load_dotenv()

# Define tools configuration for function calls
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
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Unit for temperature, either Celsius or Fahrenheit.",
                    },
                },
                "required": ["location", "unit"],  # Parameters that must be provided
            },
        },
    }
]

# Constants
MODEL_ENGINE = "gpt-3.5-turbo"  # The model used for generating responses
messages = [{"role": "system", "content": "You are a helpful assistant"}]  # Initial system message

# Initialize OpenAI client
client = openai.OpenAI()

def generate_response(user_input):
    """
    Generates a response from the assistant based on user input.

    Args:
        user_input (str): The user's input message.

    Returns:
        response (str): The assistant's response message.
    """
    # Append the user's input to the message history
    messages.append({"role": "user", "content": user_input})
    
    # Create a completion with the OpenAI chat model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # Model version
        messages=messages,  # Message history
        tools=tools,  # Available tools/functions
        tool_choice="auto",  # Use automatic tool selection
    )
    
    # Append the assistant's response to the message history
    messages.append(response.choices[0].message)
    
    return response.choices[0].message

# Define available functions for function calls
available_functions = {
    "get_current_weather": get_current_weather,
}

def call_function(tool_calls):
    """
    Calls the specified function(s) based on tool calls.

    Args:
        tool_calls (list): List of tool calls from the assistant's response.

    Executes the function and adds the function response to the message history.
    """
    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name  # Get the name of the function to call
            function_to_call = available_functions[function_name]  # Retrieve the function from available functions
            function_args = json.loads(tool_call.function.arguments)  # Parse the arguments for the function
            
            # Call the function with the specified arguments
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )

            # Print the function response
            print(function_response)
            
            # Add the function response to the message history
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )

def main():
    """
    Main function to run the assistant. Handles user input and responses.

    Provides an interactive chat interface with the assistant.
    """
    print(Fore.CYAN + "Bot: Hello, I am a helpful assistant. Type 'exit' to quit." + Fore.RESET)

    while True:
        user_input = input("You: ")

        if user_input == "exit":
            print("Goodbye!")
            break

        # Generate the initial response from the assistant
        message_response = generate_response(user_input)
        print(message_response)

        # Check if the assistant wants to call a function
        if message_response.tool_calls is None:
            print("Bot: " + message_response.content)
            continue

        # Call the function based on the assistant's request
        call_function(message_response.tool_calls)

        # Generate a second response after the function call
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )
        print("Bot: " + second_response.choices[0].message.content)

# Entry point for the application
if __name__ == "__main__":
    main()