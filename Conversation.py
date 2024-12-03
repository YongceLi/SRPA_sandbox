from prompt import *
from helpers import *
import json
import uuid
from datetime import datetime
import os

class Conversation:

    def __init__(self, 
                 chatbot, 
                 reflector, 
                 embedding_model,
                 original_prompt, 
                 extract_threshold,
                 update_threshold, 
                 target_preference = None, 
                 task_id = None,
                 evaluator = None,
                 no_preference = False):
        
        self.chatbot = chatbot
        self.reflector = reflector
        self.embedding_model = embedding_model
        self.original_prompt = original_prompt
        self.extract_threshold = extract_threshold
        self.update_threshold = update_threshold
        self.target_preference = ", ".join(target_preference)
        self.evaluator = evaluator
        self.turns_count = 1
        self.chat_history = []
        self.task_id = task_id
        self.no_preference = no_preference

    def extract_preference(self, original_prompt, threshold):
        """
        Extract user preferences from preference database based on context embedding similarity.
        
        Args:
            original_prompt (str): The user's original input prompt
            threshold (float): Minimum similarity score to consider preferences relevant
            
        Returns:
            list[str]: List of preference strings if similar context found, None otherwise
        """
        # Get embedding for current prompt
        prompt_embedding = self.embed_task_context(original_prompt)
        
        # Get preferences from reflector's database
        max_similarity = 0
        best_preferences = None
        
        for entry in self.reflector.preference:
            context_embedding = entry["context"]
            # Calculate cosine similarity between embeddings
            similarity = calculate_similarity(prompt_embedding, context_embedding)
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_preferences = entry["preference"]
        
        # Return preferences only if similarity exceeds threshold
        if max_similarity >= threshold:
            print("preference appended!")
            return best_preferences
        return []

    def embed_task_context(self, prompt):
        return self.embedding_model.embed_query(prompt)

    def concat_chat_history(self):
        return "\n\n".join(f"{speaker}: {message}" for speaker, message in self.chat_history)
    
    def conversation(self):
        """
        Manages the conversation flow between user, chatbot, and evaluator.
        Returns:
            str: Complete conversation history
        """
        try:
            history_dir = "chat_histories"
            os.makedirs(history_dir, exist_ok=True)
            if self.no_preference:
                history_file = os.path.join(history_dir, f"chat_history_{self.task_id}_no_preference.json")
            else:
                history_file = os.path.join(history_dir, f"chat_history_{self.task_id}.json")
        
            # Step 1: Extract relevant preferences and prepare initial prompt
            if self.no_preference:
                enhanced_prompt = self.original_prompt
            else:
                preferences = self.extract_preference(self.original_prompt, self.extract_threshold)
                enhanced_prompt = get_user_prompt(self.original_prompt, preferences)
            
            # Record original user prompt
            self.chat_history.append(["user", enhanced_prompt])
            
            # Step 2: Get initial chatbot response
            print("Begin Conversation, ChatBot responding ...")
            chatbot_response = self.chatbot.generate_response(enhanced_prompt)
            self.chat_history.append(["chatbot", chatbot_response])
            
            # Step 3: Get evaluator's feedback
            if self.evaluator is None:
                raise ValueError("Evaluator is required but not provided")
                
            print("Continue Conversation, evaluating response ...")
            user_response = self.evaluator.generate_response(
                get_evaluator_prompt(
                    self.original_prompt, 
                    self.target_preference, 
                    chatbot_response
                )
            )
            self.chat_history.append(["user", user_response])
            
            # Step 4: Continue conversation until satisfied
            while "SATISFIED" not in user_response and self.turns_count <= 5:
                self.turns_count += 1
                # Use full conversation history for context
                conversation_context = self.concat_chat_history()
                print("Continue Conversation, Chatbot modifying ...")
                chatbot_response = self.chatbot.generate_response(conversation_context)
                self.chat_history.append(["chatbot", chatbot_response])
                
                print("Continue Conversation, evaluating response ...")
                user_response = self.evaluator.generate_response(
                    get_evaluator_prompt(
                        self.original_prompt,
                        self.target_preference,
                        chatbot_response
                    )
                )
                self.chat_history.append(["user", user_response])
            
            print("Conversation ended!")
            # Step 5: Update preference database
            if self.reflector and not self.no_preference:
                reflection_prompt = get_reflector_prompt(self.concat_chat_history())
                print("Reflecting ...")
                new_preferences = self.reflector.generate_response(reflection_prompt)
                new_preferences_lst = str_to_list(new_preferences)
                # Update preference database
                print("Updating Preferences ...")
                self.reflector.update_preference(
                    self.embed_task_context(self.original_prompt),
                    new_preferences_lst,
                    self.update_threshold
                )
                self.reflector.save_preference_to_jsonl()
            
            print("Saving conversation history ...")
            save_turn_to_json(history_file, self.chat_history)

            print("Finished!")
            return self.concat_chat_history()
            
        except Exception as e:
            print(f"Error in conversation: {str(e)}")
            return None




