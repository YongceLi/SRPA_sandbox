import pickle

def get_user_prompt(prompt, preference = []):
    assert isinstance(preference, list), "Preference must be a list of strings"
    preference_str = ", ".join(preference)
    if len(preference) > 0:
        new_prompt = f"""{prompt}
Based on your previous conversation history, the user has the following preferences:
- {preference_str}
Ensure your response:
- Maintains your natural conversational style
- Addresses all aspects of the original request

Please proceed with your response."""
    else:
        new_prompt = prompt
    return new_prompt

def get_evaluator_prompt(prompt, preference, output):
    new_prompt = f"""Evaluate whether the task requirements and your specific preferences have been fully met in the response.

If EVERY aspect satisfied, output "SATISFIED". If not, imagine you are the user and have engaged in the conversation, only provide a one sentence follow-up prompt for potential modification. 

Task Description: {prompt}
User Specific Preferences: {preference}
Response to be Evaluated: {output}"""
    return new_prompt

def get_reflector_prompt(chat_history):
    new_prompt = f"""Given the conversations between the User and Chatbot summarize the User's preference on this task in general into a list of words followed by "PREFERENCE". 
    
    Conversation history:
    {chat_history}
    Output the summarized preference list after "PREFERENCE:". """
    return new_prompt