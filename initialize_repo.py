import os
import stat
import subprocess
import sys


def run_decrypt_creds(venv_dir):
    """
    Executes the 'decrypt_creds.py' script within the virtual environment.
    """
    if os.name == "nt":
        # Windows
        activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")
        python_executable = os.path.join(venv_dir, "Scripts", "python")
    else:
        # Unix or MacOS
        activate_script = os.path.join(venv_dir, "bin", "activate")
        python_executable = os.path.join(venv_dir, "bin", "python")

    try:
        if os.name == "nt":
            subprocess.check_call(
                f"{activate_script} && {python_executable} decrypt_creds.py", shell=True
            )
        else:
            subprocess.check_call(
                f"source {activate_script} && {python_executable} decrypt_creds.py",
                shell=True,
            )
        print("decrypt_creds.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run decrypt_creds.py: {e}")


def create_file(file_path, content):
    """
    The generic function to create the .bat and hook files to update the creds periodically.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    # Make the file executable
    if os.name == "nt":  # On Windows
        pass  # No need to change permissions for Windows
    else:  # On Unix-like systems
        st = os.stat(file_path)
        os.chmod(file_path, st.st_mode | stat.S_IEXEC)


def is_venv_dir(directory):
    """
    Check if a directory is a virtual environment.

    A directory is considered a virtual environment if it contains a 'pyvenv.cfg' file
    and either a 'bin' directory (on Unix-like systems) or a 'Scripts' directory (on Windows).

    Args:
        directory (str): The directory to check.

    Returns:
        bool: True if the directory is a virtual environment, False otherwise.
    """
    return os.path.isfile(os.path.join(directory, "pyvenv.cfg")) and (
        os.path.isdir(os.path.join(directory, "bin"))
        or os.path.isdir(os.path.join(directory, "Scripts"))
    )


def find_venv():
    """
    Find a virtual environment in the current directory.

    Scans the current directory for any directories that contain markers indicating
    a virtual environment.

    Returns:
        str or None: The name of the virtual environment directory if found, None otherwise.
    """
    for entry in os.listdir("."):
        if os.path.isdir(entry) and is_venv_dir(entry):
            return entry
    return None


def create_venv(venv_dir):
    """
    Create a virtual environment.

    Uses the 'venv' module to create a virtual environment in the specified directory.

    Args:
        venv_dir (str): The directory to create the virtual environment in.
    """
    subprocess.check_call([sys.executable, "-m", "venv", venv_dir])


def install_requirements(venv_dir, requirements_file):
    """
    Install packages from a requirements file into the virtual environment.

    Uses the pip executable from the virtual environment to install packages listed
    in the requirements file.

    Args:
        venv_dir (str): The virtual environment directory.
        requirements_file (str): The path to the requirements.txt file.
    """
    pip_executable = os.path.join(venv_dir, "bin", "pip")
    if not os.path.isfile(pip_executable):
        pip_executable = os.path.join(venv_dir, "Scripts", "pip")  # for Windows
    subprocess.check_call([pip_executable, "install", "-r", requirements_file])


if __name__ == "__main__":
    hooks_dir = ".git/hooks"
    post_checkout_hook = os.path.join(hooks_dir, "post-checkout")
    post_merge_hook = os.path.join(hooks_dir, "post-merge")
    bat_file_path = "decrypt_creds.bat"
    python_script_path = "decrypt_creds.py"

    # Ensure the hooks directory exists
    os.makedirs(hooks_dir, exist_ok=True)

    # Content for the batch file
    bat_file_content = f"""@echo off
python "{python_script_path}"
    """

    # Content for the post-checkout hook
    post_checkout_content = f"""@echo off
call "{bat_file_path}"
    """

    # Content for the post-merge hook
    post_merge_content = f"""@echo off
call "{bat_file_path}"
    """
    create_file(bat_file_path, bat_file_content)
    print(f"Created {bat_file_path}")

    # Create the post-checkout hook
    create_file(post_checkout_hook, post_checkout_content)
    print(f"Created {post_checkout_hook}")

    # Create the post-merge hook
    create_file(post_merge_hook, post_merge_content)
    print(f"Created {post_merge_hook}")

    requirements_file = "requirements.txt"

    venv_dir = find_venv()
    if venv_dir:
        print(f"Virtual environment found in directory: {venv_dir}")
    else:
        venv_dir = "venv"  # Directory name for the virtual environment
        print("Creating virtual environment...")
        create_venv(venv_dir)

    if os.path.isfile(requirements_file):
        print("Installing packages from requirements.txt...")
        install_requirements(venv_dir, requirements_file)
    else:
        print("requirements.txt not found.")

    run_decrypt_creds(venv_dir)

