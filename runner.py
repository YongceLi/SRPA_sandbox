from ChatBot import *
from Reflector import *
from Conversation import *
from Embedding import *
from helpers import *
from prompt import *
import json
import argparse
from tqdm import tqdm

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run conversation with parameters from JSON file')
    parser.add_argument('data_path', help='Path to JSON configuration file')
    args = parser.parse_args()

    try:
        input_data = load_jsonl(args.data_path)
        # Load configuration
        for config in tqdm(input_data):
            # Initialize required models
            chatbot = ChatBot()
            evaluator = ChatBot("gpt-4o-mini")
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
                evaluator=evaluator  # Using the same chatbot as evaluator
            )

            # Run conversation
            result = conversation.conversation()
            if result:
                print("Conversation completed successfully!")
                #print(result)
            else:
                print("Conversation failed to complete.")

    except FileNotFoundError:
        print(f"Error: Could not find configuration file at {args.data_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in configuration file {args.data_path}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()