# DATA_INGESTION_FROM_LOOKER_VETERANS process documentation

## DATA_INGESTION_FROM_LOS_UTILIZATION.ipynb

### Initialization

#### Cell 1

This cell sets up the environment for the notebook.

**Functionality:**

- Imports necessary libraries such as pandas, numpy, and looker_sdk.
- Configures display options for better readability of DataFrames.

**Cell 1 Expected Fail Cases and Fixes:**

1. **Library Import Failure:**

    - **Likely Cause:** Missing library or incorrect installation.
    - **Fix:** Ensure all required libraries are installed using `pip install <library_name>`.

2. **Display Configuration Failure:**
    - **Likely Cause:** Incorrect display option settings.
    - **Fix:** Verify the display options and correct any syntax errors.

#### Cell 2

This cell imports utility modules and database connection classes.

**Functionality:**

- Imports `DsEmail`, `ConfigTools`, `Task`, `TaskManager`, and `MultiThreadedLogger` from `ds_general_utils`.
- Imports `GsAutomationReliefAssistanceConnection` from `ds_sql_connections`.

**Cell 2 Expected Fail Cases and Fixes:**

1. **Import Failure:**
    - **Likely Cause:** Missing or incorrect module installation.
    - **Fix:** Ensure the `ds_general_utils` and `ds_sql_connections` modules are installed and accessible.

#### Cell 3

- This cell initializes the task manager.
- Functionality:
  - Creates a `TaskManager` instance with the task name "partners in care clarity looker veterans data ingestion".

##### Cell 3 Expected Fail Cases and Fixes

1. Task Manager Initialization Failure:
   - Likely Cause: Incorrect initialization parameters.
   - Fix: Verify the parameters passed to the `TaskManager` and ensure they are correct.

#### Cell 4

This cell initializes the log file for the data ingestion process.

**Functionality:**

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

This cell initializes the starting global variables for the data ingestion process.

**Functionality:**

- Checks for any errors in the task manager.
- Sets up the main directory path and configuration manager.
- Loads configuration data from the `looker.ini` file.
- Defines variables for pulling records from Looker, including model, view, and limit.
- Retrieves SQL credentials from the configuration object.
- Sets up date and time variables in different formats.
- Defines enrollment filter ranges and their corresponding labels.

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

This cell connects to the Looker API and ingests program-level data for various time periods.

**Functionality:**

- Initializes the Looker SDK using the configuration file.
- Defines the fields to be retrieved from the Looker API.
- Generates query bodies for different date filters.
- Runs queries to retrieve data for each date filter.
- Processes the results by adding a "Reporting Period" column and renaming specific columns.
- Collects all DataFrames and concatenates them into one DataFrame (`program_level_df`).
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

This cell pulls bed inventory data, calculates days in the reporting period, and determines beds available during the reporting period.

**Functionality:**

- Defines the fields to be retrieved from the Looker API.
- Generates query bodies for different date filters.
- Runs queries to retrieve data for each date filter.
- Processes the results by calculating overlap days and total bed inventory for the reporting period.
- Collects all DataFrames and concatenates them into one DataFrame (`total_inventory_df`).
- Updates the task tracker with the status of the data retrieval and processing.

**Cell 7 Expected Fail Cases and Fixes:**

1. **Query Execution Failure:**
    - **Likely Cause:** Incorrect query parameters or API endpoint issues.
    - **Fix:** Verify the query parameters and ensure the API endpoint is correct and accessible.

2. **Data Processing Failure:**
    - **Likely Cause:** Issues with the data format returned by the API.
    - **Fix:** Verify the data format and ensure it is compatible with pandas DataFrame.

3. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

#### Cell 8

This cell connects to the database and ingests count program-level data for various time periods.

**Functionality:**

- Defines the fields to be retrieved from the Looker API.
- Generates query bodies for different date filters and move-in statuses.
- Runs queries to retrieve data for each date filter and move-in status.
- Processes the results by renaming specific columns.
- Merges the DataFrames for 'with' and 'without' move-ins.
- Collects all DataFrames and concatenates them into one DataFrame (`final_counts_df`).
- Updates the task tracker with the status of the data retrieval and processing.

**Cell 8 Expected Fail Cases and Fixes:**

1. **Query Execution Failure:**
    - **Likely Cause:** Incorrect query parameters or API endpoint issues.
    - **Fix:** Verify the query parameters and ensure the API endpoint is correct and accessible.

2. **Data Processing Failure:**
    - **Likely Cause:** Issues with the data format returned by the API.
    - **Fix:** Verify the data format and ensure it is compatible with pandas DataFrame.

3. **DataFrame Merge Failure:**
    - **Likely Cause:** Mismatched columns or data types.
    - **Fix:** Ensure the columns and data types are consistent across DataFrames before merging.

4. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

#### Cell 9

This cell connects to the database and ingests enrollment-level data for various time periods.

**Functionality:**

- Defines the fields to be retrieved from the Looker API.
- Generates query bodies for different date filters.
- Runs queries to retrieve data for each date filter.
- Processes the results by adding a "Reporting Period" column, calculating days since start, and categorizing enrollments based on thresholds.
- Collects all DataFrames and concatenates them into one DataFrame (`enrollment_level_df`).
- Updates the task tracker with the status of the data retrieval and processing.

**Cell 9 Expected Fail Cases and Fixes:**

1. **Query Execution Failure:**
    - **Likely Cause:** Incorrect query parameters or API endpoint issues.
    - **Fix:** Verify the query parameters and ensure the API endpoint is correct and accessible.

2. **Data Processing Failure:**
    - **Likely Cause:** Issues with the data format returned by the API.
    - **Fix:** Verify the data format and ensure it is compatible with pandas DataFrame.

3. **Condition Generation Failure:**
    - **Likely Cause:** Incorrect logic in the condition generation function.
    - **Fix:** Verify the logic and ensure it correctly categorizes the data.

4. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

#### Cell 10

This cell connects to the database and ingests referral-level data for various time periods.

**Functionality:**

- Defines the fields to be retrieved from the Looker API.
- Generates query bodies for different date filters.
- Runs queries to retrieve data for each date filter.
- Processes the results by adding a "Reporting Period" column and renaming specific columns.
- Collects all DataFrames and concatenates them into one DataFrame (`referral_level_df`).
- Updates the task tracker with the status of the data retrieval and processing.

**Cell 10 Expected Fail Cases and Fixes:**

1. **Query Execution Failure:**
    - **Likely Cause:** Incorrect query parameters or API endpoint issues.
    - **Fix:** Verify the query parameters and ensure the API endpoint is correct and accessible.

2. **Data Processing Failure:**
    - **Likely Cause:** Issues with the data format returned by the API.
    - **Fix:** Verify the data format and ensure it is compatible with pandas DataFrame.

3. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

### Aggregration and Transformtion

#### Cell 11

This cell merges data from various sources and creates extra fields for analysis.

**Functionality:**

- Merges program-level data with bed inventory totals.
- Merges program-level data with counts.
- Merges program-level data with referral data.
- Merges program-level data with enrollment data.
- Calculates program utilization during the reporting period.
- Fills missing values with 0 and converts specific columns to integers.
- Converts the "Enrollments Reporting Period End Date" column to datetime and replaces any dates after today with today's date.
- Converts the "Enrollments Reporting Period End Date" column back to string.
- Updates the task tracker with the status of the data merging and field generation.

**Cell 11 Expected Fail Cases and Fixes:**

1. **Data Merge Failure:**
    - **Likely Cause:** Mismatched columns or data types.
    - **Fix:** Ensure the columns and data types are consistent across DataFrames before merging.

2. **Calculation Failure:**
    - **Likely Cause:** Incorrect logic in the calculation functions.
    - **Fix:** Verify the logic and ensure it correctly calculates the desired values.

3. **Date Conversion Failure:**
    - **Likely Cause:** Incorrect date format or invalid date values.
    - **Fix:** Verify the date format and ensure all date values are valid.

4. **Task Tracker Update Failure:**
    - **Likely Cause:** Issues with the `Task` or `TaskManager` class.
    - **Fix:** Ensure the `Task` and `TaskManager` classes are correctly implemented and accessible.

### Uploading

#### Cell 12

This cell uploads the final results DataFrame to the database.

**Functionality:**

- Adds update timestamps in HST, CST, and UTC to the final results DataFrame.
- Establishes a connection to the database using `PicHorneDashesConnection`.
- Inserts the final results DataFrame into the specified database table with progress tracking.
- Updates the task tracker with the status of the data upload.

**Cell 12 Expected Fail Cases and Fixes:**

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

#### cell 13

- This cell sends an email alert if the task manager indicates that the process was not successful.
- Functionality:
  - Checks if the task manager's `_process_success` attribute is not "Success".
  - Generates the email subject and body using `task_mgr.generate_task_email(today_str)`.
  - Initializes an `DsEmail` client.
  - Sends an email alert with the generated subject and body to the "partners_in_care" group.

##### Cell 13 Expected Fail Cases and Fixes

1. Email Generation Failure:
   - Likely Cause: Issues with the task manager or email generation logic.
   - Fix: Verify the task manager's state and ensure the email generation logic is correct.

2. Email Sending Failure:
   - Likely Cause: Incorrect email client configuration or network issues.
   - Fix: Verify the email client configuration and ensure the network is accessible.

#### cell 14

- This cell performs cleanup of the logger.
- Functionality:
  - Calls the `cleanup` method on the `logger_manager` to perform any necessary cleanup operations.

##### Cell 14 Expected Fail Cases and Fixes

1. Logger Cleanup Failure:
   - Likely Cause: Issues with the logger manager or cleanup logic.
   - Fix: Verify the logger manager's state and ensure the cleanup logic is correct.

## DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.py

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

## DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.bat

### batch Overview

This batch file sets up the environment and executes the Python script for data ingestion from Looker.

### batch Functionality

- Changes the current directory to `C:\Public\partners_in_care`.
- Activates the Python virtual environment located in the `venv` directory.
- Executes the `DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.py` script.

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
