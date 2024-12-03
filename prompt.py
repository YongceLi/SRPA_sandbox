import pickle

def get_user_prompt(prompt, preference = []):
    assert isinstance(preference, list), "Preference must be a list of strings"
    preference_str = ", ".join(preference)
    if len(preference) > 0:
        new_prompt = f"""{prompt}
Please make sure your response satisfies the following preference:
- {preference_str}
"""
    else:
        new_prompt = prompt
    return new_prompt

def get_evaluator_prompt(prompt, preference, output):
    new_prompt = f"""Task Description: {prompt}
User Specific Preferences: {preference}
Response to be Evaluated: {output}

Evaluate whether the task requirements and your specific preferences have been fully met in the response.

If EVERY aspect are satisfied, only output a single word "SATISFIED". 

If some aspects are not satisfied or partial aspects have room to improve, imagine you are the user and have engaged in the conversation, only provide a one sentence follow-up prompt in first person tone for potential modification and ask the model to regenerate the whole response with the suggestion. 
"""
    return new_prompt

def get_reflector_prompt(chat_history):
    new_prompt = f"""Please read the following conversation between a user and a chatbot. Analyze the dialogue to infer the user's implicit preferences, even if they are not explicitly stated. Based on the conversation, generate a list of the user's preferences, formatting each as a single phrase in a clear and concise manner.

Conversation History:

{chat_history}

Task:

Extract the user's implicit preferences from the conversation.
Present the preferences as a list of strings.
Ensure each preference is formatted as a single, standalone phrase.
Only output the extracted preferences as a python list enclosed by brackets. 
Output:
"""
    return new_prompt