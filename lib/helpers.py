import json

def save_to_json(data, output_path):
    """
    Save the data to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)