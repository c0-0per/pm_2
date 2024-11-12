import os
import json

# Directory containing JSON files
JSON_DIR = 'json_files'

def replace_record_id_in_file(file_path):
    """
    Replace 'record_id' with an empty string in every JSON element of the given file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if data is a list of dictionaries
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    item['record_id'] = ""
        elif isinstance(data, dict):
            data['record_id'] = ""
        else:
            print(f"Unsupported JSON structure in {file_path}")
            return
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Updated 'record_id' in {file_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_json_files(directory):
    """
    Locate all JSON files in the specified directory and replace 'record_id' in each.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            replace_record_id_in_file(file_path)

if __name__ == "__main__":
    process_json_files(JSON_DIR)
