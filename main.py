import textbase
import os
import pickle
from textbase.message import Message
from textbase import models
from typing import List
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# Access the variables
models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

gpt_ask = True
wrong_input = False
abs_dict = {}
# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You're chatting with an health assistant. Your name is Health-GPT You should only ask about health and fitness related stuff. No other prompts should be entertained. Please check that the prompts are related to health and fitness only."""
info_user = ""


def auth_user(counter, message_history):

    print(counter)

    if counter == 0:
        return "Please enter your email id.", False

    elif counter == 1:
        # if"yes" in message_history[-1].content.lower():
        with open("database.bin", "rb+") as f:
            info_dict = pickle.load(f)
            try:
                
                info_user = info_dict[message_history[-1].content]
                return f"Welcome back, {info_user['name']}.As per your previous records, yours height is {info_user['height']} and weight is {info_user['weight']} How may I help you today?", True
            except:
                info_dict[message_history[-1].content.strip()
                          ] = {"name": "", "height": "", "weight": ""}
                with open("database.bin", "wb+") as g:
                    pickle.dump(info_dict, g)
                print(type(message_history[-1].content), info_dict)
                return "Please enter your name", False

    elif counter == 2:
        with open("database.bin", "rb+") as f:
            info_dict = pickle.load(f)
            # print(info_dict)
            info_dict[message_history[-3].content]["name"] = message_history[-1].content
            with open("database.bin", "wb+") as g:
                pickle.dump(info_dict, g)
        return "Please enter your height in centimetres", False

    elif counter == 3:
        with open("database.bin", "rb+") as f:
            info_dict = pickle.load(f)
            info_dict[message_history[-5].content]["height"] = message_history[-1].content
            with open("database.bin", "wb+") as g:
                pickle.dump(info_dict, g)
        return "Please enter your weight in kilograms", False

    elif counter == 4:
        print(" inside count 4")
        with open("database.bin", "rb+") as f:
            info_dict = pickle.load(f)
            info_dict[message_history[-7].content]["weight"] = message_history[-1].content
            
            info_user = info_dict[message_history[-7].content]
            with open("database.bin", "wb") as g:
                pickle.dump(info_dict, g)
        return f"Hello, {info_user['name']}! How may I help you?", True
    else:
        print("Overflow")


@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    # global auth
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """
    if state is None or "counter" not in state:
        state = {"counter": 0, "auth": False}
    else:
        state["counter"] += 1

    if not state["auth"]:
        bot_response, auth = auth_user(state["counter"], message_history)
        state["auth"] = auth

    # # Generate GPT-3.5 Turbo response
    else:
        # message_history[-1].content = message_history[-1].content + 
        
        print(info_user)

        bot_response = models.OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,
            model="gpt-3.5-turbo",
        )

    return bot_response, state
