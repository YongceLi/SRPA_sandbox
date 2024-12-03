import numpy as np
import json
import ast

def load_jsonl(data_path):
    data_list = []
    with open(data_path, "r") as file:
        for line in file:
            data_list.append(json.loads(line))
    return data_list

def calculate_similarity(embedding1, embedding2):
    """
    Calculate cosine similarity between two embeddings using numpy.
    """
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    if norm1 == 0 or norm2 == 0:
        return 0.0    
    return dot_product / (norm1 * norm2)

def save_turn_to_json(file_path, chat_history):
    """Save current chat history to a JSON file."""
    conversation_data = {
        "messages": [
            {
                "role": role,
                "content": content,
                "turn": i // 2 + 1
            }
            for i, (role, content) in enumerate(chat_history)
        ]
    }
    
    with open(file_path, 'w') as f:
        json.dump(conversation_data, f, indent=2)

def str_to_list(preference_str):
    """
    Convert a string representation of a list into a Python list.
    """
    try:
        return ast.literal_eval(preference_str.strip("```python").strip("```"))
        
    except (ValueError, SyntaxError):
        try:
            cleaned = preference_str.strip("```python").strip("```").strip('[').strip(']').replace('"', '').replace("'", '')
            return [item.strip() for item in cleaned.split(',') if item.strip()]
        except Exception as e:
            print(f"Error converting string to list: {str(e)}")
            return []