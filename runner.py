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
    parser = argparse.ArgumentParser(description="Parser")

    parser = argparse.ArgumentParser(description='Run conversation')
    parser.add_argument('--data_path', type=str, help='Path to dataset')
    parser.add_argument('--extract_threshold', type=float, help='specifying the extracting threshold', default=0.85)
    parser.add_argument('--update_threshold', type=float, help='Aspecifying the updating threshold', default=0.9)
    parser.add_argument("--no_preference", action="store_true", help="do not append preference, test original prompts")
    
    args = parser.parse_args()

    no_preference = False
    if args.no_preference:
        no_preference = True

    try:
        input_data = load_jsonl(args.data_path)
        # Load configuration
        for config in tqdm(input_data):
            # Initialize required models
            chatbot = ChatBot("gpt-4o-mini")
            evaluator = ChatBot("gpt-4o-mini")
            reflector = Reflector(user_id = config.get('personal_id'))
            embedding_model = EmbeddingModel()
            
            # Create conversation object with parameters from JSON
            conversation = Conversation(
                chatbot=chatbot,
                reflector=reflector,
                embedding_model=embedding_model,
                original_prompt=config.get('original_prompt'),
                extract_threshold=args.extract_threshold,  # default value if not specified
                update_threshold=args.update_threshold,    # default value if not specified
                target_preference=config.get('target_preference'),
                task_id=config.get('task_id'),
                evaluator=evaluator,  # Using the same chatbot as evaluator
                no_preference=no_preference,
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