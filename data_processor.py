import os
import pandas as pd
import shutil

"""
Data Processor Script for Excel Files

This script processes Excel files stored in various thematic folders within a 'data' directory.
It converts each Excel file (with '.xls' or '.xlsx' extension) into a CSV format and saves
the output in corresponding thematic subfolders within a 'csv_data' directory. If the 'csv_data'
directory or its subdirectories do not exist, they are created.

The script processes each thematic folder within the 'data' directory. Within each folder,
it identifies Excel files, reads them into a pandas DataFrame, and then saves them as CSV files.
Each CSV file is named after the original Excel file and is stored in the corresponding thematic
subfolder in 'csv_data'.

The script is structured to handle and skip non-directory files encountered in the 'data' directory 
and also to skip files within each thematic folder that do not have an Excel file extension.

Usage:
    Run this script with Python in an environment where pandas is installed.

Example:
    To execute the script, use the following command:
    python <script_name>.py

Note:
    - The script requires the 'data' directory to be present in the same directory as the script.
    - The 'data' directory should contain subdirectories, each representing a theme with Excel files.
    - The script uses the 'pandas' library for reading and writing data.
    - This script is compatible with Python 3.8 or later.
"""

# Create csv_data directory if it doesn't exist
csv_data_path = "csv_data"
if not os.path.exists(csv_data_path):
    os.makedirs(csv_data_path)

for theme in os.listdir("data"):
    theme_path = os.path.join("data", theme)

    if os.path.isdir(theme_path):
        print(f"Processing theme: {theme}")

        # Create subdirectory for theme in csv_data if it doesn't exist
        theme_csv_dir = os.path.join(csv_data_path, theme)
        if not os.path.exists(theme_csv_dir):
            os.makedirs(theme_csv_dir)

        for filename in os.listdir(theme_path):
            print(f"Processing {filename}")
            file_path = os.path.join(theme_path, filename)
            file_extension = filename.split(".")[-1]

            if file_extension in ["xls", "xlsx"]:
                df = pd.read_excel(file_path)
                csv_filename = os.path.splitext(filename)[0] + ".csv"
                csv_path = os.path.join(theme_csv_dir, csv_filename)
                df.to_csv(csv_path, index=False)
                print(f"Done with {filename}")
            else:
                print(f"Skipping non-Excel file: {filename}")
    else:
        print(f"Skipping non-directory: {theme}")
