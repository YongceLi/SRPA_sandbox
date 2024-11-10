from together import Together

class ChatBot:

    def __init__(self, modelCode):
        self.client = Together()
        self.modelCode = modelCode

    def generate_response(self, prompt):
        completion = self.client.chat.completions.create(
            model=self.modelCode,
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content
    
# chatBot = ChatBot("meta-llama/Llama-3.2-3B-Instruct-Turbo")
# print(chatBot.generate_response("Hello, how are you?"))

