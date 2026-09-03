import os
import json
from typing import Dict, Any, Optional
import configparser


class ConfigTools:
    """
    A utility class for locating, loading, modifying, and saving JSON configuration files.
    """

    def __init__(self, search_directory: str) -> None:
        """
        Initializes the ConfigTools class.
        """
        self.config_filename = None
        self.config_data = self.load_config(search_directory)

    def find_config_file(self, search_directory: str) -> str:
        """
        Searches for a JSON configuration file in the specified directory that matches the parent
        folder's name as part of the filename.

        Args:
            search_directory (str): The directory path to search for the JSON configuration file.

        Returns:
            str: The full file path of the JSON configuration file if found.

        Raises:
            FileNotFoundError: If no matching JSON file is found in the directory.
        """
        parent_folder_name = os.path.basename(os.path.abspath(search_directory))

        # Walk through the directory to find the file
        for root, _, files in os.walk(search_directory):
            for file in files:
                if file.endswith(".json") and parent_folder_name in file:
                    return os.path.join(root, file)

        raise FileNotFoundError(
            f"No JSON configuration file containing '{parent_folder_name}' found in {search_directory}"
        )

    def load_config(self, search_directory: str) -> Dict[str, Any]:
        """
        Loads the JSON configuration file located within the specified directory.
        Stores the loaded configuration data in `self.config_data`.

        Args:
            search_directory (str): The directory path to search for the JSON configuration file.

        Returns:
            Dict[str, Any]: The contents of the JSON configuration file as a dictionary.

        Raises:
            FileNotFoundError: If no matching JSON file is found in the directory.
            json.JSONDecodeError: If the file is not a valid JSON format.
        """
        self.config_filename = self.find_config_file(search_directory)
        with open(self.config_filename, "r", encoding="utf-8") as file:
            self.config_data = json.load(file)
        return self.config_data

    def get_config_value(self, *keys: str) -> Any:
        """
        Retrieves a specific nested value from the loaded configuration data based on a sequence of keys.

        Args:
            *keys (str): The sequence of keys representing the path to the nested value.

        Returns:
            Any: The value associated with the specified nested keys.

        Raises:
            ValueError: If configuration data has not been loaded.
            KeyError: If any of the keys in the sequence do not exist in the configuration data.
        """
        current_value = self.config_data

        # Start with the top-level config data and drill down using each key
        for key in keys:
            if key not in current_value:
                raise KeyError(
                    f"Key '{key}' not found in configuration data at specified location."
                )
            current_value = current_value[key]

        return current_value

    def save_config(self, file_path: Optional[str] = None) -> None:
        """
        Saves the config data back to a JSON configuration file.

        Args:
            file_path (str, optional): The file path to save the configuration data. If not provided,
                                       the original file path from initialization is used.
        """

        file_path = file_path or self.config_filename

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.config_data, file, ensure_ascii=False, indent=4)

    def reload_config(self) -> Dict[str, Any]:
        """
        Reloads the JSON configuration file, refreshing `self.config_data` with the latest data from the file.

        Raises:
            FileNotFoundError: If the config file path has not been set by `load_config`.
            json.JSONDecodeError: If the file is not a valid JSON format.
        """

        with open(self.config_filename, "r", encoding="utf-8") as file:
            self.config_data = json.load(file)

    def update_config_value(self, value: Any, *keys: str) -> None:
        """
        Updates a specific nested value in the loaded configuration data based on a sequence of keys.

        Args:
            value (Any): The new value to set at the specified nested location.
            *keys (str): The sequence of keys representing the path to the nested value.

        Raises:
            ValueError: If configuration data has not been loaded.
            KeyError: If any of the keys in the sequence do not exist in the configuration data.
        """

        # Start from the top-level config data
        current_level = self.config_data

        # Traverse through each key except the last
        for key in keys[:-1]:
            if key not in current_level:
                # If the key doesn't exist, create a new dictionary for it
                current_level[key] = {}
            elif not isinstance(current_level[key], dict):
                raise TypeError(
                    f"Expected a dictionary at '{key}', but found a non-dictionary value."
                )
            current_level = current_level[key]

        # Set the final key to the new value
        final_key = keys[-1]
        current_level[final_key] = value

    def convert_ini_to_json(self, search_directory):
        """
        Converts all .ini files in the specified directory and its subdirectories to .json files.

        Args:
            search_directory (str): The path of the directory to search for .ini files.

        Returns:
            None
        """
        # Traverse the directory
        for root, _, files in os.walk(search_directory):
            for file in files:
                if file.endswith(".ini"):
                    ini_path = os.path.join(root, file)

                    # Read .ini file
                    config = configparser.ConfigParser()
                    config.read(ini_path)

                    # Convert to dictionary
                    config_dict = {
                        section: dict(config.items(section))
                        for section in config.sections()
                    }

                    # Write to .json file
                    json_path = os.path.join(root, file.rsplit(".", 1)[0] + ".json")
                    with open(json_path, "w", encoding="utf-8") as json_file:
                        json.dump(config_dict, json_file, indent=4)
