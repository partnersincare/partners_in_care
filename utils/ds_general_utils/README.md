# DS_general_utils

This Python package (`ds_general_utils`) offers several basic python data script functionalities for use by the Horne Data Team.

## Features

- Easily load and manage Json configuration files
- Track the success and failure of individual tasks in a code
- Send regular and task alert emails
- Create and manage multithreaded logger objects

For detailed documentation on each class and method, refer to the inline docstrings in the source code.

## Package Installation

### Manual

1. In the main directory run the following command `python -m build`

2. Copy the resulting .tar or .whl file and move it the environment you with to install it on

3. Run `pip install path/to/the/version.tar.gz` or `pip install path/to/the/version.whl` command in the environment terminal

4. In your use script import the instance class of choice from `ds_general_utils` and start using its methods

### from GitHub (Recommended)

1. Using your GitHub personal access token run the command `pip install git+https://<your_access_token>@github.com/HORNEDEV/ds_general_utils.git` in the environment terminal

2. In your use script import the instance class of choice from `ds_general_utils` and start using its methods

## Examples

## Logger Example Usage

The `MultiThreadedLogger` class enables multi-threaded logging, allowing your application to log messages efficiently without blocking the main process. Here’s a step-by-step example of how to use it:

### Setting up the Logger

To get started, initialize the `MultiThreadedLogger` with the desired log file path, program name, task name, and log level. You can specify a custom format for the log messages if desired.

```python
from logging_module import MultiThreadedLogger

# Initialize the logger with the desired settings
logger_manager = MultiThreadedLogger(
    'app.log',  # Log file path
    'MyApp',    # Program name
    'TaskA',    # Task or component name
    level='INFO',
    format_string="%(asctime)s %(levelname)s %(message)s"
)

# Retrieve the logger and start logging
logger = logger_manager.logger
logger.info("Starting application...")
logger.warning("This is a warning message.")
```

### Cleaning Up Resources

To ensure that all resources are properly released, call cleanup() on the logger_manager when the application is shutting down.

```python
logger_manager.cleanup()
```

## Config Example Usage

The `ConfigTools` class provides tools for locating, loading, updating, and saving JSON configuration files. This example demonstrates how to initialize the class, access configuration values, update them, and save your changes.

### Loading a Configuration

Initialize `ConfigTools` by specifying the directory containing the configuration file. `ConfigTools` searches for a JSON file that includes the parent folder's name in its filename.

```python
from config_module import ConfigTools

# Initialize with the directory containing the configuration file
config_manager = ConfigTools('/path/to/config/directory')

# The configuration data is automatically loaded
config_data = config_manager.config_data
print("Configuration data:", config_data)
```

### Accessing Nested Configuration Values

Retrieve specific values from the loaded configuration by specifying the key path.

```python
api_key = config_manager.get_config_value('api', 'key')
    print("API Key:", api_key)
```

### Updating and Saving Configuration Values

To modify a configuration value, use update_config_value(). You can then save the changes to the original file or to a new file.

```python
# Update a nested configuration value
config_manager.update_config_value('new_value', 'api', 'key')

# Save changes back to the original file
config_manager.save_config()

# Optionally, save to a different file
config_manager.save_config('/path/to/new_config.json')
```

### Reloading Configuration Data

If the configuration file is updated externally, reload it with reload_config() to refresh the in-memory configuration data.

```python
# Reload the configuration from the file
config_manager.reload_config()
print("Reloaded configuration data:", config_manager.config_data)
```

## Email Example Usage

The `DsEmail` class allows for sending a basic email with and without attachments, using CC/BCC, and sending a task alert

### Setting up the email client

```python
from your_package_name.email_module import DsEmail  # Replace 'your_package_name' and 'email_module' accordingly

# Initialize the DsEmail instance with a directory containing the configuration file
email_client = DsEmail(search_directory='/path/to/config')

# Example 1: Basic email with a single recipient
email_client.send_email(
    subject="Project Update",
    body="Here's the latest update on the project.",
    sender="your_email@example.com",
    receiver="recipient@example.com"
)

# Example 2: Email with CC, BCC, and an attachment
email_client.send_email(
    subject="Monthly Report",
    body="Please find the attached report.",
    sender="your_email@example.com",
    receiver="recipient@example.com",
    cc="cc_recipient@example.com",
    bcc="bcc_recipient@example.com",
    attachments=["/path/to/report.pdf"]
)

# Example 3: Sending a task alert email to the data and project team
# Requires "data_team" and "project_team" emails in the configuration
email_client.send_task_alert_email(
    subject="Task Alert: Data Processing Complete",
    body="The data processing task for Project XYZ has been completed.",
    project_name="Project XYZ"
)
```

### Configuration Requirements

Ensure your JSON configuration file includes:

SMTP server settings (username, password, smtp_server, smtp_port).
Default sender email as default_sender.
Team email lists under data_team and project_team for alert emails.

## Task Manager Example Usage

This module provides tools for managing and tracking tasks within a process and generating HTML-formatted reports for email summaries. Below are examples of how to use the `Task` and `TaskManager` classes to manage tasks, check for errors, and generate an email report.

### Basic Setup

1. **Import the Classes**
   Start by importing the `Task` and `TaskManager` classes from the module.

   ```python
   from your_module_name import Task, TaskManager
   ```

2. Initialize TaskManager

    Create an instance of TaskManager with the name of the process you want to manage.

    ```python
    task_manager = TaskManager("Data Processing Workflow")
    ```

### Adding and Managing Tasks

1. Create and Add Tasks

    Define individual tasks by creating instances of Task. Each task requires a name, with optional details and success status.

    ```python
    task1 = Task(task_nm="Data Extraction", task_details="Extracted data from API", success=True)
    task2 = Task(task_nm="Data Transformation", task_details="Transformed data for analysis", success=False)
    ```

2. Add Tasks to TaskManager

    Use add_task to add tasks to the TaskManager instance. The process status will update automatically based on the success of each task.

    ```python
    task_manager.add_task(task1)
    task_manager.add_task(task2)
    ```

3. Check for Errors Call

    check_errors to verify if all tasks were successful. If any task failed, it raises PriorTasksFailedError.

    ```python
    try:
        task_manager.check_errors()
    except PriorTasksFailedError as e:
        print("One or more tasks failed:", e)
    ```
