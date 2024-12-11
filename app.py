import gradio as gr
from ChatBot import *
import json
from datetime import datetime
from Reflector import *
from prompt import *
from Conversation import *
from Embedding import * 

def ensure_file_exists(filename):
    """
    Ensures that the specified file exists. If not, creates an empty file.
    """
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            pass  # Create an empty file

def extract_preference(reflector, openai_token, original_prompt, threshold):
        """
        Extract user preferences from preference database based on context embedding similarity.
        
        Args:
            original_prompt (str): The user's original input prompt
            threshold (float): Minimum similarity score to consider preferences relevant
            
        Returns:
            list[str]: List of preference strings if similar context found, None otherwise
        """
        # Get embedding for current prompt
        embedding_model = EmbeddingModel(api_key=openai_token)
        prompt_embedding = embedding_model.embed_query(original_prompt)
        
        # Get preferences from reflector's database
        max_similarity = 0
        best_preferences = None
        
        for entry in reflector.preference:
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

# Function to process inputs during conversation
def process_inputs(user_id, openai_token, prompt, chat_history):
    if not all([user_id, openai_token, prompt]):
        return chat_history, "Error: Missing input data"

    # Initialize chatbot with openAI token
    chatbot = ChatBot(api_key=openai_token, model_code="gpt-4o-mini")

    # Combine conversation history with the new prompt
    conversation_context = []
    for turn in chat_history:
        conversation_context.append({"role": "user", "content": turn[0]})
        conversation_context.append({"role": "assistant", "content": turn[1]})
    if len(conversation_context) == 0:
        filename = f"preference/preference_database_{user_id}.jsonl"
        ensure_file_exists(filename)
        reflector = Reflector(api_key=openai_token, preference_path=filename)
        preferences = extract_preference(reflector, openai_token, prompt, 0.85)
        enhanced_prompt = get_user_prompt(prompt, preferences)
        conversation_context.append({"role": "user", "content": enhanced_prompt})
    else:
        conversation_context.append({"role": "user", "content": prompt})

    # Generate response
    response = chatbot.multi_turn_generate_respose(conversation_context)

    # Update the chat history
    chat_history.append((prompt, response))
    return chat_history, response

# Function to mark the conversation as satisfied
def mark_satisfied(user_id, openai_token, chat_history):
    if not user_id:
        return "Error: User ID is required", []
    
    conversation_context = []
    for turn in chat_history:
        conversation_context.append({"role": "user", "content": turn[0]})
        conversation_context.append({"role": "assistant", "content": turn[1]})
    # Save the conversation to a file
    filename = f"preference/preference_database_{user_id}.jsonl"
    ensure_file_exists(filename)
    reflector = Reflector(api_key=openai_token, preference_path=filename)
    reflection_prompt = get_reflector_prompt(conversation_context)
    embedding_model = EmbeddingModel(api_key=openai_token)
    
    chatbot = ChatBot(api_key=openai_token, model_code="gpt-4o-mini")
    new_preferences = chatbot.generate_response(reflection_prompt)
    new_preferences_lst = str_to_list(new_preferences)
    original_prompt = chat_history[0][0]
    reflector.update_preference(
        embedding_model.embed_query(original_prompt),
        new_preferences_lst,
        update_threshold=0.85
    )
    reflector.save_preference_to_jsonl()
    
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"history/chat_history_{user_id}_{timestamp}.json"
    with open(filename, 'w') as file:
        json.dump({"user_id": user_id, "message": conversation_context}, file)

    # Clear the chat history for a new conversation
    return f"Conversation saved to {filename}. Starting a new session.", []

# Function to retrieve preferences for the given user
def show_preferences(user_id):
    if not user_id:
        return "Error: User ID is required"
    
    # Load preferences from the preference database
    filename = f"preference/preference_database_{user_id}.jsonl"
    if not os.path.exists(filename):
        return "No preference database found for this user."
    
    with open(filename, 'r') as file:
        preferences = [json.loads(line) for line in file]
    
    # Extract and display stored preferences
    preference_list = [entry["preference"] for entry in preferences]
    return preference_list if preference_list else "No preferences found."

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## Multi-Turn Chat with the Model")

    user_id = gr.Textbox(label="Your Name / ID", placeholder="Enter Name / ID")
    openai_token = gr.Textbox(label="OpenAI Token", placeholder="Enter OpenAI Token")
    prompt = gr.Textbox(label="Prompt", placeholder="Enter your prompt", lines=3)

    chat_history_display = gr.TextArea(label="Conversation History", interactive=False, placeholder="Conversation will appear here...", lines=5)
    response_box = gr.Textbox(label="Latest Response", placeholder="Waiting for input...", interactive=False)
    preference_display = gr.TextArea(label="Stored Preferences", interactive=False, placeholder="Preferences will appear here...", lines=2)
    
    # State variables to store chat history
    chat_history_state = gr.State([])

    submit_button = gr.Button("Submit")
    satisfied_button = gr.Button("Mark as Satisfied")
    show_preferences_button = gr.Button("Show Preferences")
    
    # Process inputs and update chat history
    submit_button.click(process_inputs, 
                        inputs=[user_id, openai_token, prompt, chat_history_state], 
                        outputs=[chat_history_state, response_box])

    # Display updated chat history
    submit_button.click(lambda history: "\n".join([f"User: {turn[0]}\nModel: {turn[1]}" for turn in history]), 
                        inputs=chat_history_state, 
                        outputs=chat_history_display)
    
    # Clear the prompt box after submission
    submit_button.click(lambda _: "", inputs=None, outputs=prompt)

    # Handle conversation satisfaction
    satisfied_button.click(mark_satisfied, 
                           inputs=[user_id, openai_token, chat_history_state], 
                           outputs=[response_box, chat_history_state])

    # Clear the chat history display after marking satisfied
    satisfied_button.click(lambda _: "", inputs=None, outputs=chat_history_display)

    # Show preferences
    show_preferences_button.click(show_preferences, 
                                  inputs=[user_id], 
                                  outputs=preference_display)

# Launch the Gradio App
demo.launch(share=True)
