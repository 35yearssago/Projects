import random
import json


def get_response(user_input: str) -> str:
    with open('intents.json', 'r') as file:
        responses = json.load(file)

        for response in responses['intents']:

            if user_input.lower() in [pattern.lower() for pattern in response['patterns']]:
                return random.choice(response['responses'])
        print("Match not found!")
        return "I'm sorry, I don't understand that."
