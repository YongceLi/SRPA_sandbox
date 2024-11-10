from prompt import *

class Conversation:

    def __init__(self, 
                 chatbot, 
                 reflector, 
                 original_prompt, 
                 update_threshold, 
                 target_preference = None, 
                 evaluator = None):
        
        self.chatbot = chatbot
        self.reflector = reflector
        self.original_prompt = original_prompt
        self.update_threshold = update_threshold
        self.target_preference = target_preference
        self.evaluator = evaluator
        self.turns_count = 1
        self.chat_history = []

    def extract_preference(original_prompt, threshold):
        """
        extract user preference from user's preference database based on context 
        embedding similarity.
        
        return: a list of str where each str is a single preference, or None.
        """
        pass

    def embed_task_context(self):
        pass

    def concat_chat_history(self):
        return "\n\n".join(f"{speaker}: {message}" for speaker, message in self.chat_history)
    
    def conversation(self):
        # input user prompt to chatbot get initial response
        preference = self.extract_preference(self.original_prompt, self.update_threshold)
        user_prompt = get_user_prompt(self.original_prompt, 
                                      preference)
        self.chat_history.append(["user", self.original_prompt])
        chatbot_response = self.chatbot.generate_response(user_prompt)
        self.chat_history.append(["chatbot", chatbot_response])
        # input chatbot response to evaluator to see if satisfied / need modification.
        user_response = self.evaluator.generate_response(get_evaluator_prompt(self.original_prompt, 
                                                                                self.target_preference, 
                                                                                chatbot_response))
        self.chat_history.append(["user", user_response])
        # continue multiturn conversation:
        while "SATISFIED" not in user_response:
            self.turns_count += 1
            user_input_with_suggestion = self.concat_chat_history()
            chatbot_response = self.chatbot.generate_response(user_input_with_suggestion)
            self.chat_history.append(["chatbot", chatbot_response])
            user_response = self.evaluator.generate_response(get_evaluator_prompt(self.original_prompt, 
                                                                                self.target_preference, 
                                                                                chatbot_response))
            self.chat_history.append(["user", user_response])
        
        reflection_prompt = get_reflector_prompt(self.concat_chat_history())
        preference_lst = self.reflector.generate_response(reflection_prompt)
        self.reflector.update_preference(self.embed_task_context(self.original_prompt), 
                                         preference_lst, 
                                         self.update_threshold)
        self.reflector.save_preference_to_jsonl()
        return self.concat_chat_history()




