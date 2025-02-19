# DATA_INGESTION_FROM_LOOKER_VETERANS process documentation

## DATA_INGESTION_FROM_LOOKER_VETERANS.ipynb

### Initialization

#### cell 1

- This cell sets up the environment for the notebook.
- Functionality:
  - Imports necessary libraries such as `pandas`, `numpy`, and `looker_sdk`.
  - Configures display options for better readability of DataFrames.

##### Cell 1 Expected Fail Cases and Fixes

1. Library Import Failure:
   - Likely Cause: Missing library or incorrect installation.
   - Fix: Ensure all required libraries are installed using `pip install <library_name>`.

2. Display Configuration Failure:
   - Likely Cause: Incorrect display option settings.
   - Fix: Verify the display options and correct any syntax errors.

#### cell 2

- This cell imports utility modules and database connection classes.
- Functionality:
  - Imports `DsEmail`, `ConfigTools`, `Task`, `TaskManager`, and `MultiThreadedLogger` from `ds_general_utils`.
  - Imports `GsAutomationReliefAssistanceConnection` from `ds_sql_connections`.

##### Cell 2 Expected Fail Cases and Fixes

1. Import Failure:
   - Likely Cause: Missing or incorrect module installation.
   - Fix: Ensure the `ds_general_utils` and `ds_sql_connections` modules are installed and accessible.

#### cell 3

- This cell initializes the task manager.
- Functionality:
  - Creates a `TaskManager` instance with the task name "partners in care clarity looker veterans data ingestion".

##### Cell 3 Expected Fail Cases and Fixes

1. Task Manager Initialization Failure:
   - Likely Cause: Incorrect initialization parameters.
   - Fix: Verify the parameters passed to the `TaskManager` and ensure they are correct.

#### cell 4

- This cell initializes the logging system.
- Functionality:
  - Creates a log file with a timestamped filename.
  - Sets up a `MultiThreadedLogger` instance for logging.
  - Logs the start of the data ingestion process.
  - Updates the task tracker with the status of the log file initialization.

##### Cell 4 Expected Fail Cases and Fixes

1. Log File Initialization Failure:
   - Likely Cause: Incorrect file path or permissions.
   - Fix: Verify the file path and ensure the necessary permissions are granted.

2. Logger Setup Failure:
   - Likely Cause: Incorrect logger configuration.
   - Fix: Review the logger configuration and correct any errors.

#### cell 5

- This cell initializes global variables.
- Functionality:
  - Checks for errors in the task manager.
  - Sets up the main directory path and configuration manager.
  - Loads configuration data from `looker.ini`.
  - Initializes variables for Looker queries and SQL credentials.
  - Sets up date and time variables in different formats.
  - Updates the task tracker with the status of the global variable initialization.

##### Cell 5 Expected Fail Cases and Fixes

1. Global Variable Initialization Failure:
   - Likely Cause: Missing or incorrect configuration data.
   - Fix: Verify the configuration files and ensure they are correctly formatted and accessible.

2. Date and Time Variable Setup Failure:
   - Likely Cause: Incorrect date and time formatting.
   - Fix: Review the date and time formatting and correct any errors.

### Ingestion

#### cell 6

- This cell connects to the database and ingests veteran data from Looker.
- Functionality:

- Initializes the Looker SDK.
- Defines the queries to be executed.
- Runs the queries.
- Processes the results.
- Merges the data into a single DataFrame.
- Updates the task tracker with the status of the data ingestion process.

##### Cell 6 Expected Fail Cases and Fixes

1. Looker SDK Initialization Failure:
   - Likely Cause: Incorrect SDK configuration or missing credentials.
   - Fix: Verify the SDK configuration and ensure that the correct credentials are provided.

2. Query Execution Failure:
   - Likely Cause: Syntax errors in the query or connectivity issues with the Looker instance.
   - Fix: Check the query syntax and ensure that the Looker instance is accessible.

3. Data Processing Errors:
   - Likely Cause: Inconsistent or unexpected data formats.
   - Fix: Validate the data formats and handle any inconsistencies in the processing logic.

4. DataFrame Merge Issues:
   - Likely Cause: Mismatched keys or incompatible data structures.
   - Fix: Ensure that the keys used for merging are consistent and that the data structures are compatible.

5. Task Tracker Update Failure:
   - Likely Cause: Issues with the task tracker service or incorrect update logic.
   - Fix: Verify the task tracker service is running and check the update logic for correctness.

### Aggregation and Transformation

#### cell 7

- This cell converts date columns to datetime format for later comparison.
- Functionality:
  - Converts the following columns to datetime format using `pd.to_datetime` with `errors="coerce"`:
    - `Enrollments Project Start Date`
    - `Enrollments Project Exit Date`
    - `Client Assessments Assessment Date`
    - `Referrals Created Date_completed`
    - `Referrals Created Date_pending`
    - `Entry Screen Approximate Date this Episode of Homelessness Started Date`
  - Updates the task tracker with the status of the conversion.

##### Cell 7 Expected Fail Cases and Fixes

1. Date Conversion Failure:
   - Likely Cause: Incorrect date format or invalid date values.
   - Fix: Ensure the date values are in a recognizable format and handle any invalid dates appropriately.

#### cell 8

- This cell calculates the count of total self-identified veterans in HMIS for the past 12 months.
- Functionality:
  - Creates a new DataFrame `result_veterans_df` to store the results.
  - Generates the last date of each month for the past 12 months.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in an eligible program at the end of each month.
  - Counts the number of unique clients for each month.
  - Appends the results to `result_veterans_df`.
  - Sets the index of `result_veterans_df` to the month.
  - Updates the task tracker with the status of the calculation.

##### Cell 8 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

#### cell 9

- This cell calculates the count of self-identified veterans in HMIS who are in coordinated entry programs for the past 12 months.
- Functionality:
  - Adds a new column `Coordinated Entry Vets in HMIS` to `result_veterans_df` initialized to 0.
  - Generates the last date of each month for the past 12 months.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of each month.
  - Counts the number of unique clients for each month.
  - Updates the `result_veterans_df` DataFrame with the count of coordinated entry vets for each month.
  - Updates the task tracker with the status of the calculation.

##### Cell 9 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

#### cell 10

- This cell calculates the count of veterans on the By-Name List (BNL) for the past 12 months.
- Functionality:
  - Adds a new column `Vets on BNL` to `result_veterans_df` initialized to 0.
  - Generates the last date of each month for the past 12 months.
  - Calculates the date one year prior to each month's last date.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of each month and had an assessment in the past year.
  - Counts the number of unique clients for each month.
  - Updates the `result_veterans_df` DataFrame with the count of veterans on BNL for each month.
  - Updates the task tracker with the status of the calculation.

##### Cell 10 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

#### cell 11

- This cell calculates the count of veterans on the By-Name List (BNL) with eligible discharge statuses for the past 12 months.
- Functionality:
  - Defines a list of eligible discharge statuses.
  - Adds a new column `Vets on BNL with Eligible Discharge` to `result_veterans_df` initialized to 0.
  - Generates the last date of each month for the past 12 months.
  - Calculates the date one year prior to each month's last date.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of each month, had an assessment in the past year, and have an eligible discharge status.
  - Counts the number of unique clients for each month.
  - Updates the `result_veterans_df` DataFrame with the count of veterans on BNL with eligible discharge for each month.
  - Updates the task tracker with the status of the calculation.

##### cell 11 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

#### cell 12

- This cell calculates the count of veterans on the By-Name List (BNL) with eligible discharge statuses who are not on the community queue or do not have an open referral for the past 12 months.
- Functionality:
  - Adds a new column `Vets not on Community Queue or Referred` to `result_veterans_df` initialized to 0.
  - Generates the last date of each month for the past 12 months.
  - Calculates the date one year prior to each month's last date.
  - Filters the `veterans_df` DataFrame to include clients who have an open referral at the end of the month.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of each month, had an assessment in the past year, have an eligible discharge status, are not on the community queue, and do not have an open referral.
  - Counts the number of unique clients for each month.
  - Updates the `result_veterans_df` DataFrame with the count of veterans not on the community queue or referred for each month.
  - Updates the task tracker with the status of the calculation.

##### Cell 12 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

#### cell 13

- This cell calculates the count of veterans with DD214 for the past 12 months.
- Functionality:
  - Adds a new column `Vets with DD214` to `result_veterans_df` initialized to 0.
  - Generates the last date of each month for the past 12 months.
  - Calculates the date one year prior to each month's last date.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of each month, had an assessment in the past year, have an eligible discharge status, and have a DD214.
  - Counts the number of unique clients for each month.
  - Updates the `result_veterans_df` DataFrame with the count of veterans with DD214 for each month.
  - Adds a new column `Vets with DD214 Percentage` to `result_veterans_df` to store the percentage of vets with DD214.
  - Updates the task tracker with the status of the calculation.

##### cell 13 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

4. Percentage Calculation Failure:
   - Likely Cause: Division by zero or missing data.
   - Fix: Ensure the denominator is not zero and the data is complete and correctly formatted.

#### cell 14

- This cell calculates the count of veterans that are chronically homeless and sheltered or unsheltered for the past 12 months.
- Functionality:
  - Defines a list of sheltered programs.
  - Adds new columns `Chronic Vets`, `Sheltered Vets`, and `Chronic Sheltered Vets` to `result_veterans_df` initialized to 0.
  - Generates the last date of each month for the past 12 months.
  - Calculates the date one year prior to each month's last date.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in transitional housing at the end of the month.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of each month, had an assessment in the past year, and have an eligible discharge status.
  - Determines if the client is chronically homeless by checking if they are chronically homeless at project start or have a disabling condition and have been houseless for more than a year.
  - Counts the number of unique clients who are chronically homeless.
  - Filters the `veterans_df` DataFrame to include clients who were on the BNL for the month and were enrolled in a sheltered program at the end of the month.
  - Counts the number of unique clients who are sheltered.
  - Counts the number of unique clients who are chronically homeless and sheltered.
  - Updates the `result_veterans_df` DataFrame with the counts for each month.
  - Calculates the number of unsheltered veterans and chronically homeless unsheltered veterans through subtraction.
  - Updates the task tracker with the status of the calculation.

##### cell 14 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

4. Chronic Homelessness Determination Failure:
   - Likely Cause: Incorrect logic for determining chronic homelessness.
   - Fix: Review the logic for determining chronic homelessness and ensure it is correctly implemented.

#### cell 15

- This cell calculates the inflow and outflow of veterans on the By-Name List (BNL) for the past 12 months.
- Functionality:
  - Adds new columns `Total Inflow` and `Total Outflow` to `result_veterans_df` initialized to 0.
  - Generates the last date of each month for the past 12 months.
  - Calculates the last date of the previous month and the date one year prior to each month's last date.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of the previous month, had an assessment in the past year, and have an eligible discharge status.
  - Filters the `veterans_df` DataFrame to include clients who were enrolled in the coordinated entry program at the end of the current month, had an assessment in the past year, and have an eligible discharge status.
  - Filters the data to include clients who were on the BNL in the previous month but not in the current month (outflow).
  - Filters the data to include clients who were on the BNL in the current month but not in the previous month (inflow).
  - Counts the number of unique clients for outflow and inflow for each month.
  - Updates the `result_veterans_df` DataFrame with the counts for each month.
  - Updates the task tracker with the status of the calculation.

##### Cell 15 Expected Fail Cases and Fixes

1. Date Calculation Failure:
   - Likely Cause: Incorrect date manipulation or invalid date values.
   - Fix: Ensure the date values are correctly calculated and handle any invalid dates appropriately.

2. Data Filtering Failure:
   - Likely Cause: Incorrect filtering conditions or missing data.
   - Fix: Verify the filtering conditions and ensure the data is complete and correctly formatted.

3. Count Calculation Failure:
   - Likely Cause: Incorrect counting logic or missing data.
   - Fix: Review the counting logic and ensure the data is complete and correctly formatted.

### Uploading

#### cell 16

- This cell inserts the calculated data into the database.
- Functionality:
  - Resets the index of `result_veterans_df`.
  - Adds columns `Update Time HST`, `Update Time CST`, and `Update Time UTC` to `result_veterans_df` with the current time in different time zones.
  - Establishes a connection to the database using `GsAutomationReliefAssistanceConnection`.
  - Inserts the data from `result_veterans_df` into the `partners_in_care_veterans_summary` table in the database.
  - Updates the task tracker with the status of the insertion.

##### Cell 16 Expected Fail Cases and Fixes

1. Database Connection Failure:
   - Likely Cause: Incorrect connection credentials or network issues.
   - Fix: Verify the connection credentials and ensure the network is accessible.

2. Data Insertion Failure:
   - Likely Cause: Incorrect table schema or data type mismatch.
   - Fix: Verify the table schema and ensure the data types match the expected format.

3. Index Reset Failure:
   - Likely Cause: Issues with the DataFrame structure.
   - Fix: Ensure the DataFrame is correctly structured before resetting the index.

### Wrap up

#### cell 17

- This cell sends an email alert if the task manager indicates that the process was not successful.
- Functionality:
  - Checks if the task manager's `_process_success` attribute is not "Success".
  - Generates the email subject and body using `task_mgr.generate_task_email(today_str)`.
  - Initializes an `DsEmail` client.
  - Sends an email alert with the generated subject and body to the "partners_in_care" group.

##### Cell 17 Expected Fail Cases and Fixes

1. Email Generation Failure:
   - Likely Cause: Issues with the task manager or email generation logic.
   - Fix: Verify the task manager's state and ensure the email generation logic is correct.

2. Email Sending Failure:
   - Likely Cause: Incorrect email client configuration or network issues.
   - Fix: Verify the email client configuration and ensure the network is accessible.

#### cell 18

- This cell performs cleanup of the logger.
- Functionality:
  - Calls the `cleanup` method on the `logger_manager` to perform any necessary cleanup operations.

##### Cell 18 Expected Fail Cases and Fixes

1. Logger Cleanup Failure:
   - Likely Cause: Issues with the logger manager or cleanup logic.
   - Fix: Verify the logger manager's state and ensure the cleanup logic is correct.

## DATA_INGESTION_FROM_LOOKER_VETERANS.py

### Script Description

- This script executes a Jupyter notebook using Papermill.

### Functionality

1. **Import Libraries**:
   - Imports the `papermill` library as `pm` for executing Jupyter notebooks.
   - Imports the `os` library for interacting with the operating system.

2. **Set Main Directory Path**:
   - Sets the `main_directory_path` variable to the current working directory using `os.getcwd()`.

3. **Define Notebook Paths**:
   - Defines the input notebook path `in_notebook` as `DATA_INGESTION_FROM_LOOKER_VETERANS.ipynb` in the main directory.
   - Defines the output notebook path `out_notebook` as `Output_DATA_INGESTION_FROM_LOOKER_VETERANS.ipynb` in the `output_nbs` subdirectory of the main directory.

4. **Execute Notebook**:
   - Uses `pm.execute_notebook` to execute the input notebook and save the output to the specified output notebook path.

### Script Expected Fail Cases and Fixes

1. **Library Import Failure**:
   - Likely Cause: Missing library or incorrect installation.
   - Fix: Ensure the `papermill` library is installed using `pip install papermill`.

2. **Directory Path Issues**:
   - Likely Cause: Incorrect directory path or missing directories.
   - Fix: Verify the directory paths and ensure the necessary directories exist.

3. **Notebook Execution Failure**:
   - Likely Cause: Errors within the notebook being executed.
   - Fix: Review the notebook for errors and ensure it runs correctly in a Jupyter environment.

## DATA_INGESTION_FROM_LOOKER_VETERANS.bat

### batch Description

- This batch file sets up the environment and executes the Python script for data ingestion from Looker.

### Batch Functionality

1. **Change Directory**:
   - Changes the current directory to `C:\Public\partners_in_care` using the `cd` command.

2. **Activate Virtual Environment**:
   - Activates the Python virtual environment located in the `venv` directory using the `call` command to run `venv/Scripts/activate`.

3. **Execute Python Script**:
   - Runs the `DATA_INGESTION_FROM_LOOKER_VETERANS.py` script using the `python` command.

### Batch Expected Fail Cases and Fixes

1. **Directory Change Failure**:
   - Likely Cause: Incorrect directory path or missing directory.
   - Fix: Verify the directory path and ensure the directory exists.

2. **Virtual Environment Activation Failure**:
   - Likely Cause: Missing virtual environment or incorrect path.
   - Fix: Ensure the virtual environment is created and the path is correct.

3. **Python Script Execution Failure**:
   - Likely Cause: Errors within the Python script or missing dependencies.
   - Fix: Review the Python script for errors and ensure all dependencies are installed.
