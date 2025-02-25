# DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY process documentation

## DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.ipynb

### Initialization

#### Cell 1

- This cell sets up the environment for the notebook.
- Functionality:
  - Imports necessary libraries such as `pandas`, `os`, `json`, `datetime`, `numpy`, `pytz`, `StringIO`, and `looker_sdk`.

**Cell 1 Expected Fail Cases and Fixes:**

1. **Library Import Failure:**
    - **Likely Cause:** Missing library or incorrect installation.
    - **Fix:** Ensure all required libraries are installed using `pip install <library_name>`.

#### Cell 2

- This cell imports utility modules and database connection classes.
- Functionality:
  - Imports `DsEmail`, `ConfigTools`, `Task`, `TaskManager`, and `MultiThreadedLogger` from `ds_general_utils`.
  - Imports `PicHorneDashesConnection` from `utils.sql_connection`.

**Cell 2 Expected Fail Cases and Fixes:**

1. **Import Failure:**
    - **Likely Cause:** Missing or incorrect module installation.
    - **Fix:** Ensure the `ds_general_utils` and `utils.sql_connection` modules are installed and accessible.

#### Cell 3

- This cell initializes the task manager with the overall name of the task.
- Functionality:
  - Initializes the `TaskManager` with the name "partners in care daily activity data ingestion".

**Cell 3 Expected Fail Cases and Fixes:**

1. **Task Manager Initialization Failure:**
    - **Likely Cause:** Issues with the `TaskManager` class or incorrect initialization parameters.
    - **Fix:** Verify the `TaskManager` class implementation and ensure the initialization parameters are correct.

#### Cell 4

- This cell initializes the log file for the data ingestion process.
- Functionality:
  - Creates a timestamp for the log file name.
  - Sets up the logging directory and file path.
  - Initializes the `MultiThreadedLogger` with the specified log file path and configuration.
  - Logs the start of the data ingestion process.
  - Updates the task tracker with the status of the log file initialization.

**Cell 4 Expected Fail Cases and Fixes:**

1. **Directory Creation Failure:**
    - **Likely Cause:** Insufficient permissions or invalid directory path.
    - **Fix:** Ensure the script has the necessary permissions and the directory path is valid.

2. **Logger Initialization Failure:**
    - **Likely Cause:** Incorrect logger configuration or issues with the `MultiThreadedLogger` class.
    - **Fix:** Verify the logger configuration and ensure the `MultiThreadedLogger` class is correctly implemented and accessible.

3. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

#### Cell 5

- This cell initializes the starting global variables for the data ingestion process.
- Functionality:
  - Checks for any errors in the task manager.
  - Sets up the main directory path and configuration manager.
  - Loads configuration data from the `looker.ini` file.
  - Defines variables for pulling records from Looker, including model, view, and limit.
  - Retrieves SQL credentials from the configuration object.
  - Sets up date and time variables in different formats.

**Cell 5 Expected Fail Cases and Fixes:**

1. **Configuration Load Failure:**
    - **Likely Cause:** Incorrect file path or missing configuration file.
    - **Fix:** Ensure the `looker.ini` file exists at the specified path and is accessible.

2. **Variable Initialization Failure:**
    - **Likely Cause:** Incorrect configuration data or missing keys.
    - **Fix:** Verify the configuration data and ensure all required keys are present.

3. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

### Ingestion

#### Cell 6

- This cell connects to the Looker API and ingests program-level data.
- Functionality:
  - Initializes the Looker SDK using the configuration file.
  - Defines the fields to be retrieved from the Looker API.
  - Sets up filters for the query.
  - Generates the query body.
  - Runs the query to retrieve data.
  - Processes the results by loading them into a pandas DataFrame.
  - Collects all DataFrames and concatenates them into one DataFrame (`client_level_df`).
  - Updates the task tracker with the status of the data ingestion process.

**Cell 6 Expected Fail Cases and Fixes:**

1. **SDK Initialization Failure:**
    - **Likely Cause:** Incorrect configuration file path or missing configuration file.
    - **Fix:** Ensure the `looker.ini` file exists at the specified path and is accessible.

2. **Query Execution Failure:**
    - **Likely Cause:** Incorrect query parameters or API endpoint issues.
    - **Fix:** Verify the query parameters and ensure the API endpoint is correct and accessible.

3. **Data Processing Failure:**
    - **Likely Cause:** Issues with the data format returned by the API.
    - **Fix:** Verify the data format and ensure it is compatible with pandas DataFrame.

4. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

#### Cell 7

- This cell connects to the Looker API and ingests program-level data for various time periods.
- Functionality:
  - Initializes the Looker SDK using the configuration file.
  - Defines the fields to be retrieved from the Looker API.
  - Sets up filters for the query.
  - Generates the query body.
  - Runs the query to retrieve data.
  - Processes the results by loading them into a pandas DataFrame.
  - Collects all DataFrames and concatenates them into one DataFrame (`referrals_df`).
  - Updates the task tracker with the status of the data ingestion process.

**Cell 7 Expected Fail Cases and Fixes:**

1. **SDK Initialization Failure:**
    - **Likely Cause:** Incorrect configuration file path or missing configuration file.
    - **Fix:** Ensure the `looker.ini` file exists at the specified path and is accessible.

2. **Query Execution Failure:**
    - **Likely Cause:** Incorrect query parameters or API endpoint issues.
    - **Fix:** Verify the query parameters and ensure the API endpoint is correct and accessible.

3. **Data Processing Failure:**
    - **Likely Cause:** Issues with the data format returned by the API.
    - **Fix:** Verify the data format and ensure it is compatible with pandas DataFrame.

4. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

### Uploading

#### Cell 8

- This cell uploads the client-level data to the database.
- Functionality:
  - Checks for any errors in the task manager.
  - Establishes a connection to the database using `PicHorneDashesConnection`.
  - Adds update timestamps in HST, CST, and UTC to the client-level DataFrame.
  - Inserts the client-level DataFrame into the specified database table with progress tracking.
  - Updates the task tracker with the status of the data upload.

**Cell 8 Expected Fail Cases and Fixes:**

1. **Database Connection Failure:**
    - **Likely Cause:** Incorrect connection parameters or database server issues.
    - **Fix:** Verify the connection parameters and ensure the database server is accessible.

2. **Data Insertion Failure:**
    - **Likely Cause:** Data type mismatches or schema issues.
    - **Fix:** Verify the data types and ensure the schema matches the DataFrame structure.

3. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

#### Cell 9

- This cell uploads the referral-level data to the database.
- Functionality:
  - Checks for any errors in the task manager.
  - Adds update timestamps in HST, CST, and UTC to the referral-level DataFrame.
  - Establishes a connection to the database using `PicHorneDashesConnection`.
  - Inserts the referral-level DataFrame into the specified database table with progress tracking.
  - Updates the task tracker with the status of the data upload.

**Cell 9 Expected Fail Cases and Fixes:**

1. **Database Connection Failure:**
    - **Likely Cause:** Incorrect connection parameters or database server issues.
    - **Fix:** Verify the connection parameters and ensure the database server is accessible.

2. **Data Insertion Failure:**
    - **Likely Cause:** Data type mismatches or schema issues.
    - **Fix:** Verify the data types and ensure the schema matches the DataFrame structure.

3. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

### Wrap up

#### cell 10

- This cell sends an email alert if the task manager indicates that the process was not successful.
- Functionality:
  - Checks if the task manager's `_process_success` attribute is not "Success".
  - Generates the email subject and body using `task_mgr.generate_task_email(today_str)`.
  - Initializes an `DsEmail` client.
  - Sends an email alert with the generated subject and body to the "partners_in_care" group.

##### Cell 10 Expected Fail Cases and Fixes

1. Email Generation Failure:
   - Likely Cause: Issues with the task manager or email generation logic.
   - Fix: Verify the task manager's state and ensure the email generation logic is correct.

2. Email Sending Failure:
   - Likely Cause: Incorrect email client configuration or network issues.
   - Fix: Verify the email client configuration and ensure the network is accessible.

#### cell 11

- This cell performs cleanup of the logger.
- Functionality:
  - Calls the `cleanup` method on the `logger_manager` to perform any necessary cleanup operations.

##### Cell 11 Expected Fail Cases and Fixes

1. Logger Cleanup Failure:
   - Likely Cause: Issues with the logger manager or cleanup logic.
   - Fix: Verify the logger manager's state and ensure the cleanup logic is correct.

## DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.py

### py Overview

This script executes a Jupyter notebook using Papermill, which allows for parameterization and execution of notebooks.

### py Functionality

- Imports necessary libraries: `papermill` and `os`.
- Sets the main directory path to the current working directory.
- Defines the input notebook path (`in_notebook`) and the output notebook path (`out_notebook`).
- Executes the input notebook and saves the executed notebook to the output path using Papermill.

### py Expected Fail Cases and Fixes

1. **Notebook Execution Failure:**
    - **Likely Cause:** Errors within the notebook or incorrect notebook paths.
    - **Fix:** Verify the notebook paths and ensure the notebook runs without errors manually.

2. **File Path Issues:**
    - **Likely Cause:** Incorrect directory structure or missing directories.
    - **Fix:** Ensure the specified directories exist and the paths are correct.

3. **Papermill Import Failure:**
    - **Likely Cause:** Missing Papermill library.
    - **Fix:** Install Papermill using `pip install papermill`.

## DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.bat

### batch Overview

This batch file sets up the environment and executes the Python script for data ingestion from Looker.

### batch Functionality

- Changes the current directory to `C:\Public\partners_in_care`.
- Activates the Python virtual environment located in the `venv` directory.
- Executes the `DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.py` script.

### batch Expected Fail Cases and Fixes

1. **Directory Change Failure:**
    - **Likely Cause:** Incorrect directory path.
    - **Fix:** Verify the directory path and ensure it exists.

2. **Virtual Environment Activation Failure:**
    - **Likely Cause:** Missing or incorrectly set up virtual environment.
    - **Fix:** Ensure the virtual environment is correctly set up in the `venv` directory.

3. **Python Script Execution Failure:**
    - **Likely Cause:** Errors within the Python script or missing dependencies.
    - **Fix:** Verify the Python script runs without errors and all dependencies are installed.
