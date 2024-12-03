from together import Together
from openai import OpenAI

class ChatBot:

    def __init__(self, model_code = "meta-llama/Llama-3.2-3B-Instruct-Turbo"):
        if "Llama" in model_code:
            self.client = Together()
        elif "gpt" in model_code:
            self.client = OpenAI()
        self.model_code = model_code

    def generate_response(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.model_code,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    
#prompt = """Hi ChatGPT! I'm visiting my grandmother for her birthday, and she only speaks Spanish. Can you help me with phrases to talk about my school, hobbies, and some funny things that happened last week? I also need to learn specific words like 'grades,' 'projects,' and 'friends' so I can talk to her better. Thanks! Could you add phonetic pronunciation for each phrase to make it easier for me to practice?"""
#chatBot = ChatBot("meta-llama/Llama-3.2-3B-Instruct-Turbo")
#print(chatBot.generate_response(prompt))

