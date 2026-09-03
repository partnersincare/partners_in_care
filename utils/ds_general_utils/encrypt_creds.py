import os
from cryptography.fernet import Fernet


def find_or_create_key_file(search_path, key_filename):
    """
    Search for the key file in the specified directory and its subdirectories.
    If the key file is not found, create a new key file in the root of the search path.

    Args:
        search_path (str): The directory path to start searching for the key file.
        key_filename (str): The name of the key file to search for.

    Returns:
        str: The path to the found or created key file.
    """
    # Walk through the directory to find the key file
    for root, _, files in os.walk(search_path):
        if key_filename in files:
            return os.path.join(root, key_filename)

    # If key file is not found, create it in the root of the search path
    key_file_path = os.path.join(search_path, key_filename)
    key = Fernet.generate_key()
    with open(key_file_path, "wb") as keyfile:
        keyfile.write(key)

    return key_file_path


def find_json_file(search_path):
    """
    Search for a .json file in the specified directory and its subdirectories.

    Args:
        search_path (str): The directory path to start searching for the .json file.

    Returns:
        str: The path to the found .json file.

    Raises:
        FileNotFoundError: If no .json file is found in the specified path.
    """
    # Walk through the directory to find the .json file
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(".json"):
                return os.path.join(root, file)

    raise FileNotFoundError(f"No .json file found in '{search_path}'")


def encrypt_file(input_file, output_file, key_file):
    """
    Encrypt the input file using the key from the key file and save the encrypted data to the output file.

    Args:
        input_file (str): The path to the file to be encrypted.
        output_file (str): The path where the encrypted file will be saved.
        key_file (str): The path to the key file to be used for encryption.

    Returns:
        None
    """
    # Load the key
    with open(key_file, "rb") as keyfile:
        key = keyfile.read()

    cipher_suite = Fernet(key)

    # Read and encrypt the input file
    with open(input_file, "rb") as file:
        file_data = file.read()
        encrypted_data = cipher_suite.encrypt(file_data)

    # Save the encrypted data
    with open(output_file, "wb") as file:
        file.write(encrypted_data)


if __name__ == "__main__":
    search_path_key = "utils"
    key_filename = "zoom_secret.key"
    search_path_json = os.path.dirname(__file__)

    # Find or create the key file
    key_path = find_or_create_key_file(search_path_key, key_filename)

    # Find the .json file
    json_file_path = find_json_file(search_path_json)
    output_file_path = json_file_path + ".enc"

    encrypt_file(json_file_path, output_file_path, key_path)
