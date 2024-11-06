import papermill as pm
import os

main_directory_path = str(os.getcwd())

in_notebook = main_directory_path + "\\DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.ipynb"
out_notebook = (
    main_directory_path
    + "\\output_nbs\\Output_DATA_INGESTION_FROM_LOOKER_DAILY_ACTIVITY.ipynb"
)

pm.execute_notebook(in_notebook, out_notebook)
