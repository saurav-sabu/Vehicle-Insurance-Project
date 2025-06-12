import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get MongoDB connection URL from environment variable
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Database and collection configuration
DATABASE_NAME = "vehicle-db"  # Name of the MongoDB database
COLLECTION_NAME = "vehicle-data"  # Name of the main collection
MONGODB_URL_KEY = MONGO_DB_URL  # MongoDB connection URL

# Pipeline and artifact directory configuration
PIPELINE_NAME : str = ""  # Name of the pipeline (to be set as needed)
ARTFACT_DIR: str = "artifacts"  # Directory to store pipeline artifacts

# File names for data processing
FILE_NAME: str = "data.csv"  # Raw data file name
TRAIN_FILE_NAME: str = "train.csv"  # Training data file name
TEST_FILE_NAME: str = "test.csv"  # Test data file name

# Data ingestion constants
DATA_INGESTION_COLLECTION_NAME: str = "vehicle-data"  # Collection name for data ingestion
DATA_INGESTION_DIR_NAME: str = "data_ingestion"  # Directory for data ingestion artifacts
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Directory for feature store
DATA_INGESTION_INGESTED_DIR: str = "ingested"  # Directory for ingested data
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25  # Train-test split ratio for data ingestion

# Data validation constants
DATA_VALIDATION_DIR_NAME: str = "data_validation"  # Directory for data validation artifacts
DATA_VALIDATION_REPORT_FILE_NAME:str = "reports.yaml"  # File name for data validation report

# Path to the schema file used for data validation
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")