import csv
import json
import ast

def convert_csv_to_json(csv_file_path, json_file_path):
    data = []

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            # Read the CSV file as a dictionary
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                try:
                    # The 'options' column in your CSV is a string representation of a list 
                    # (e.g., "['A. yes', 'B. no']"). We use ast.literal_eval to convert 
                    # it back into a real Python list.
                    options_list = ast.literal_eval(row['options'])
                except (ValueError, SyntaxError):
                    # Fallback if the options string is malformed
                    options_list = row['options']

                # Create the dictionary object matching the structure of test.json
                entry = {
                    "id": int(row['id']),
                    "ground_truth": row['ground_truth'],
                    "question_type": row['question_type'],
                    "question": row['question'],
                    "video_path": row['video_file'],  # Mapping 'video_file' to 'video_path'
                    "options": options_list,
                    "mc_answer": row['answer']       # Mapping 'answer' to 'mc_answer'
                }
                
                data.append(entry)

        # Write the list of dictionaries to a JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
            
        print(f"Successfully converted {len(data)} rows to {json_file_path}")

    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
# Ensure 'annotations.csv' is in the same directory or provide the full path
convert_csv_to_json('annotations.csv', 'formatted_annotations.json')