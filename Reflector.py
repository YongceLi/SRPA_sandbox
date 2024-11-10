from openai import OpenAI
import json
import os 

class Reflector:

    def __init__(self, modelCode, preference_path):
        if not os.path.isfile(preference_path):
            raise FileNotFoundError(f"The file at path '{preference_path}' does not exist or is not a valid file.")
        self.client = OpenAI()
        self.modelCode = modelCode
        self.preference_path = preference_path
        self.preference = self.load_preferences(preference_path)

    def load_preferences(self, preference_path):
        preferences_lst = []
        with open(preference_path, "r") as file:
            for line in file:
                preferences_lst.append(json.loads(line))
        
        return preferences_lst

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

    def save_preference_to_jsonl(self):
        with open(self.preference_path, "w") as file:
            for item in self.preference:
                file.write(json.dumps(item) + "\n")
        

