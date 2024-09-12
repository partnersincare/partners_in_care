import os
from cryptography.fernet import Fernet


def find_key_file(search_path, key_filename):
    """
    Search for the key file in the specified directory and its subdirectories.

    Args:
        search_path (str): The directory path to start searching for the key file.
        key_filename (str): The name of the key file to search for.

    Returns:
        str: The path to the found key file.

    Raises:
        FileNotFoundError: If the key file is not found in the specified path.
    """
    # Walk through the directory to find the key file
    for root, _, files in os.walk(search_path):
        while True:
            for root, _, files in os.walk(search_path):
                if key_filename in files:
                    return os.path.join(root, key_filename)
                input(
                    "Key file could not be found. Please contact the author of this repo and place the secret.key file in the utils folder. Press Enter to check again..."
                )


def find_encrypted_file(search_path):
    """
    Search for an encrypted file (.enc) in the specified directory and its subdirectories.

    Args:
        search_path (str): The directory path to start searching for the encrypted file.

    Returns:
        str: The path to the found encrypted file.

    Raises:
        FileNotFoundError: If no encrypted file is found in the specified path.
    """
    # Walk through the directory to find the encrypted file
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(".enc"):
                return os.path.join(root, file)

    raise FileNotFoundError(f"No encrypted file found in '{search_path}'")


def decrypt_file(enc_file, key_file, dec_file):
    """
    Decrypt the encrypted file using the key from the key file and save the decrypted data to the output file.

    Args:
        enc_file (str): The path to the encrypted file to be decrypted.
        key_file (str): The path to the key file to be used for decryption.
        dec_file (str): The path where the decrypted file will be saved.

    Returns:
        None
    """
    # Load the key
    with open(key_file, "rb") as keyfile:
        key = keyfile.read()

    cipher_suite = Fernet(key)

    # Read the encrypted file
    with open(enc_file, "rb") as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Write the decrypted data
    with open(dec_file, "wb") as file:
        file.write(decrypted_data)


if __name__ == "__main__":
    search_path_key = "utils"
    key_filename = "partners_in_care_secret.key"
    search_path_json = "utils"

    # Find the key file
    key_path = find_key_file(search_path_key, key_filename)

    # Find the encrypted file
    enc_file_path = find_encrypted_file(search_path_json)
    dec_file_path = enc_file_path[:-4]  # Remove the .enc extension
    decrypt_file(enc_file_path, key_path, dec_file_path)
