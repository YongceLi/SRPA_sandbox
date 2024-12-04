from openai import OpenAI
from helpers import *
import json
import os 

class Reflector:

    def __init__(self, model_code = "gpt-4o-mini", user_id = "01"):
        preference_path = f"./preference_database_{user_id}.jsonl"
        if not os.path.isfile(preference_path):
            with open(preference_path, 'w', encoding='utf-8') as file:
                pass 
        self.client = OpenAI()
        self.modelCode = model_code
        self.preference_path = preference_path
        self.preference = load_jsonl(preference_path)

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
        
    def update_preference(self, context_embedding, preference_lst, update_threshold):
        """
        Updates the preference database by either replacing existing preferences 
        or creating a new entry based on context similarity.
        
        Args:
            context_embedding (list): Vector embedding of current context
            preference_lst (list): New preferences to add/update
            update_threshold (float): Similarity threshold for merging preferences
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            # Find most similar existing context
            max_similarity = 0
            similar_entry_idx = -1
            
            for idx, entry in enumerate(self.preference):
                similarity = calculate_similarity(context_embedding, entry["context"])
                if similarity > max_similarity:
                    max_similarity = similarity
                    similar_entry_idx = idx
            
            # If similar context found, replace preferences
            if max_similarity >= update_threshold and similar_entry_idx != -1:
                self.preference[similar_entry_idx]["preference"] = preference_lst
            else:
                # Create new entry
                new_entry = {
                    "context": context_embedding,
                    "preference": preference_lst
                }
                self.preference.append(new_entry)
            # Save updates to file
            self.save_preference_to_jsonl()
            return True
            
        except Exception as e:
            print(f"Error updating preferences: {str(e)}")
            return False

