import os
from pathlib import Path

# Name of the main project directory
project_name = "src"

# List of files to be created with their relative paths
list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/mongo_db_connection.py",
    f"{project_name}/configuration/aws_connection.py",
    f"{project_name}/cloud_storage/__init__.py",
    f"{project_name}/cloud_storage/aws_storage.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/estimator.py",
    f"{project_name}/entity/s3_estimator.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/data_access/proj_data.py",
    f"{project_name}/experiments/experiment.ipynb",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "pyproject.toml",
    "config/model.yaml",
    "config/schema.yaml"
    ]

# Iterate over each file path in the list
for file_path in list_of_files:
    file_path = Path(file_path)  # Convert to Path object for compatibility
    file_dir, file_name = os.path.split(file_path)  # Split into directory and file name

    # Create the directory if it doesn't exist
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        print(f"Created directory: {file_dir}")

    # Create the file if it doesn't exist or is empty
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, "w") as f:
            pass  # Create an empty file
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists and is not empty: {file_path}")