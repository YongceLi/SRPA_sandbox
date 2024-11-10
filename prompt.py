import pickle

def get_user_prompt(prompt, preference):
    if preference:
        new_prompt = f"{prompt}\nI want the answer to be:\n{preference}."
    else:
        new_prompt = f"{prompt}"
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