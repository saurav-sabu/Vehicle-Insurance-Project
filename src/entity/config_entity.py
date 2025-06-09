import os
from src.constants import *
from dataclasses import dataclass
from datetime import datetime

# Generate a timestamp string for unique artifact directory naming
TIME_STAMP : str = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}"

@dataclass
class TrainingPipelineConfig:
    # Name of the pipeline
    pipeline_name : str = PIPELINE_NAME
    # Directory where all artifacts for this pipeline run will be stored
    artifact_dir: str = os.path.join(ARTFACT_DIR,TIME_STAMP)
    # Timestamp for this pipeline run
    timestamp: str = TIME_STAMP

# Create a global instance of TrainingPipelineConfig
training_pipeline_config : TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    # Directory for data ingestion artifacts
    data_ingestion_dir : str = os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    # Path to the feature store file
    feature_store_file_path: str = os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
    # Path to the training data file
    training_file_path: str = os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
    # Path to the testing data file
    testing_file_path: str = os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
    # Ratio for splitting data into train and test sets
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    # Name of the collection in the data source (e.g., database)
    collection_name:str = DATA_INGESTION_COLLECTION_NAME