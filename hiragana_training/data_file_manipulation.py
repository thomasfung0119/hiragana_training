import json
from platformdirs import user_data_dir
from os import path, remove, makedirs


def init_paths():
    """
    Initializes paths for the TTF font, icon, and data directory.
    """
 
    paths = {}
    bundle_dir = path.abspath(path.dirname(__file__))
    paths["font"] = path.join(bundle_dir, r"ZenMaruGothic-Black.ttf")
    paths["icon"] = path.join(bundle_dir, r"icon.ico")
    paths["data_dir"] = user_data_dir(appname="hiragana_training", appauthor="thomaskkfung")
    makedirs(paths["data_dir"], exist_ok=True)
    paths["data_file"] = path.join(paths["data_dir"], 'training_record.dat')

    return paths


def read_from_json(filepath):
    """
    Reads a JSON file and returns its content.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        list: The content of the JSON file as a list.
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    if path.exists(data_file):
        remove(data_file)

def save_to_json(filepath, record):
        """
        Adds a new record to a JSON file. Creates the file if it doesn't exist.

        Args:
            filepath (str): The path to the JSON file.
            new_record (dict): The new record to add.
        """
        if not path.exists(filepath):
            with open(filepath, 'w') as file:
                json.dump([record], file, indent=4)
        else:
            try:
                with open(filepath, 'r+') as file:
                    file_data = json.load(file)
                    if not isinstance(file_data, list):
                        file_data = [file_data]
                    file_data.append(record)
                    file.seek(0)
                    json.dump(file_data, file, indent=4)
                    file.truncate()
            except json.JSONDecodeError:
                with open(filepath, 'w') as file:
                    json.dump([record], file, indent=4)