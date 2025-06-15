
import json
import os

def add_record_to_json(file_path, new_record):
    """
    Adds a new record to a JSON file. Creates the file if it doesn't exist.

    Args:
        file_path (str): The path to the JSON file.
        new_record (dict): The new record to add.
    """
    if not os.path.exists(file_path):
        # Create a new JSON file with the new record as a list
        with open(file_path, 'w') as f:
            json.dump([new_record], f, indent=4)
    else:
        # Load the existing JSON data
        with open(file_path, 'r+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                # Handle the case where the file is empty or contains invalid JSON
                data = []

            # Append the new record
            data.append(new_record)

            # Move the file pointer to the beginning of the file
            f.seek(0)
            # Write the updated data to the file
            json.dump(data, f, indent=4)
            # Truncate the file to remove any old content after the new data
            f.truncate()

"""# Example usage
file_path = 'my_data.json'
new_record = {'name': 'Alice', 'age': 30}
add_record_to_json(file_path, new_record)

new_record = {'name': 'Bob', 'age': 25}
add_record_to_json(file_path, new_record)"""
f = open('my_data.json')
record = json.load(f)
f.close()
print(record)