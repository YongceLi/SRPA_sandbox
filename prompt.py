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
    new_prompt = f"""Task Description: {prompt}
User Specific Preferences: {preference}
Response to be Evaluated: {output}

Evaluate whether the task requirements and your specific preferences have been fully met in the response.

If EVERY aspect are satisfied and have nothing to improve, only output a single word "SATISFIED". 

If some aspects are not satisfied or partial aspects have room to improve, imagine you are the user and have engaged in the conversation, only provide a one sentence follow-up prompt in first person tone for potential modification. 
"""
    return new_prompt

def get_reflector_prompt(chat_history):
    new_prompt = f"""Given the conversations between the User and the Chatbot, summarize the User's preference on the current context in general into a python list of words. 

Conversation history:
{chat_history}

Only output the summarized python preference list:\n"""
    return new_prompt