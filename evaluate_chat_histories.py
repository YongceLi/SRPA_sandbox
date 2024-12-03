import os
import json
import re

def calculate_average_turns_with_range(directory, k):
    """
    Calculate average conversation turns for files in a specified range (IDs ending with k to 9).
    
    Args:
        directory (str): Path to the directory containing JSON files.
        k (int): Starting digit (inclusive) for the ID range filter (e.g., 5 for files ending in 5-9).
        
    Returns:
        tuple: Average turns for 'no_preference' files and other files.
    """
    no_preference_turns = []
    other_turns = []

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            # Extract the ID from the filename using regex
            match = re.search(r'_(\d{4})', filename)
            if match:
                id_ = match.group(1)
                # Only include IDs ending in k to 9
                if int(id_[-1]) in range(k, 10):  # Check if the last digit is in the range
                    file_path = os.path.join(directory, filename)

                    # Open and parse the JSON file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        if 'messages' in data:
                            total_turns = len(data['messages']) // 2  # Each turn is a pair of user-chatbot
                            if '_no_preference' in filename:
                                no_preference_turns.append(total_turns)
                            else:
                                other_turns.append(total_turns)

    # Calculate averages
    no_preference_avg = sum(no_preference_turns) / len(no_preference_turns) if no_preference_turns else 0
    other_avg = sum(other_turns) / len(other_turns) if other_turns else 0

    return no_preference_avg, other_avg

def count_files_with_fewer_turns(directory):
    """
    Counts the number of JSON files where preference files have fewer turns
    than their corresponding no_preference files.

    Args:
        directory (str): Path to the directory containing JSON files.

    Returns:
        int: The count of files where preference files have fewer turns than no_preference files.
    """
    count = 0

    # Store turns for no_preference and preference files
    turns_dict = {}

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            # Extract the ID and type (preference or no_preference)
            match = re.search(r'_(\d{4})(_no_preference)?\.json', filename)
            if match:
                file_id = match.group(1)
                is_no_preference = bool(match.group(2))

                file_path = os.path.join(directory, filename)

                # Open and parse the JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if 'messages' in data:
                        total_turns = len(data['messages']) // 2  # Each turn is a pair of user-chatbot

                        # Update the dictionary with turns data
                        if file_id not in turns_dict:
                            turns_dict[file_id] = {'no_preference': None, 'preference': None}
                        
                        if is_no_preference:
                            turns_dict[file_id]['no_preference'] = total_turns
                        else:
                            turns_dict[file_id]['preference'] = total_turns

    # Compare turns and count files where preference has fewer turns
    for file_id, turns in turns_dict.items():
        if turns['preference'] is not None and turns['no_preference'] is not None:
            if turns['preference'] <= turns['no_preference']:
                count += 1

    return count / len(turns_dict.items())

if __name__ == '__main__':
    # Replace 'chat_histories' with the actual directory path
    directory = 'chat_histories'
    # Replace 5 with your desired starting digit (k)
    k = 5
    no_preference_avg, other_avg = calculate_average_turns_with_range(directory, k)

    print(f"Average number of turns for 'no_preference' files (IDs ending {k}-9): {no_preference_avg:.2f}")
    print(f"Average number of turns for other files (IDs ending {k}-9): {other_avg:.2f}")

    fewer_turns_count = count_files_with_fewer_turns(directory)
    print(f"Percentage of conversations where with preference decreases the total number turns of conversations: {fewer_turns_count}")