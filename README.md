# Partners in Care Data Ingestion

## Overview

This repository contains scripts and notebooks for ingesting and processing data from Looker for the Partners in Care project. The primary goal is to automate the data ingestion process, perform necessary transformations, and upload the processed data to a database for further analysis and reporting.

## Repository Structure

- **Notebooks:**
  - `DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.ipynb`: Ingests data related to Length of Stay (LOS) and utilization from Looker.
  - `DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.ipynb`: Ingests daily activity data from Looker.

- **Python Scripts:**
  - `DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.py`: Executes the `DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.ipynb` notebook using Papermill.
  - `DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.py`: Executes the `DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.ipynb` notebook using Papermill.

- **Batch Files:**
  - `DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.bat`: Sets up the environment and executes the `DATA_INGESTION_FROM_LOOKER_LOS_UTILIZATION.py` script.
  - `DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.bat`: Sets up the environment and executes the `DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.py` script.

## Processes

### Length of Stay and Utilization Data Ingestion

1. **Initialization:**
   - Sets up the environment and imports necessary libraries.
   - Initializes the task manager and log file.

2. **Global Variables Initialization:**
   - Loads configuration data and sets up global variables for the data ingestion process.

3. **Data Ingestion:**
   - Connects to the Looker API and retrieves program-level data for various time periods.
   - Processes the retrieved data and calculates necessary metrics.

4. **Data Upload:**
   - Uploads the processed data to the database.

### Daily Activity Data Ingestion

1. **Initialization:**
   - Sets up the environment and imports necessary libraries.
   - Initializes the task manager and log file.

2. **Global Variables Initialization:**
   - Loads configuration data and sets up global variables for the data ingestion process.

3. **Data Ingestion:**
   - Connects to the Looker API and retrieves daily activity data.
   - Processes the retrieved data and prepares it for upload.

4. **Data Upload:**
   - Uploads the processed data to the database.

## Configuration

The configuration files are located in the `utils` directory and contain necessary credentials and settings for connecting to Looker and the database.

## Helper Modules

This repo has many extra python modules that are used across files, they mostly live in .py files in the utils folder, but the ds_general_utils package is stored in teh library files themselves.

## Contact

For any questions or issues, please contact Josh Allen at [Joshua.allen@Horne.com](mailto:Joshua.allen@Horne.com) or [jaa.joshua.allen@gmail.com](mailto:jaa.joshua.allen@gmail.com)
