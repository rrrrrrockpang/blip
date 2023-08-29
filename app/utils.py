import openai 
import json

def connect_to_openai(token_keys_path):
    with open(token_keys_path, "r") as f:
        token_keys = json.load(f)
    openai.api_key = token_keys['OPENAI_API_KEY']


def complete(prompt):
    completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=70,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            n=1
        )
    return completion.choices[0].text.strip()
