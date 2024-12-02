from ChatBot import *
from Reflector import *
from Conversation import *
from Embedding import *
from helpers import *
from prompt import *
import json
import argparse

def load_config(json_path):
    """Load configuration from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run conversation with parameters from JSON file')
    parser.add_argument('config_path', help='Path to JSON configuration file')
    args = parser.parse_args()

    try:
        # Load configuration
        config = load_config(args.config_path)

        # Initialize required models
        chatbot = ChatBot()
        reflector = Reflector()
        embedding_model = EmbeddingModel()
        
        # Create conversation object with parameters from JSON
        conversation = Conversation(
            chatbot=chatbot,
            reflector=reflector,
            embedding_model=embedding_model,
            original_prompt=config.get('original_prompt'),
            extract_threshold=config.get('extract_threshold', 0.8),  # default value if not specified
            update_threshold=config.get('update_threshold', 0.9),    # default value if not specified
            target_preference=config.get('target_preference'),
            task_id=config.get('task_id'),
            evaluator=chatbot  # Using the same chatbot as evaluator
        )

        # Run conversation
        result = conversation.conversation()
        if result:
            print("Conversation completed successfully!")
            print(result)
        else:
            print("Conversation failed to complete.")

    except FileNotFoundError:
        print(f"Error: Could not find configuration file at {args.config_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in configuration file {args.config_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()