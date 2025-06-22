import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get MongoDB connection URL and AWS credentials from environment variables
MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # MongoDB connection URL from environment
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")  # AWS access key ID from environment
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")  # AWS secret access key from environment

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
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")  # Path to schema file

# Data transformation constants
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"  # Directory for data transformation artifacts
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"  # Directory for transformed data
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"  # Directory for transformed objects

# Model trainer constants
MODEL_TRAINER_DIR_NAME: str = "model_trainer"  # Directory for model trainer artifacts
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"  # Directory for trained models
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"  # File name for the trained model
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6  # Expected minimum model score
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config","model.yaml")  # Path to model config file
MODEL_TRAINER_N_ESTIMATORS: int = 200  # Number of estimators for model training
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7  # Minimum samples required to split an internal node
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6  # Minimum samples required to be at a leaf node
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10  # Maximum depth of the tree
MIN_SAMPLES_SPLIT_CRITERION: str = "entropy"  # Criterion for splitting
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101  # Random state for reproducibility

# Preprocessing and target column constants
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"  # File name for the preprocessing object (pickle file)
TARGET_COLUMN = "Response"  # Name of the target column

# AWS credentials and region configuration
AWS_ACCESS_KEY_ID_ENV_KEY = AWS_ACCESS_KEY_ID  # AWS access key ID
AWS_SECRET_ACCESS_KEY_ENV_KEY = AWS_SECRET_ACCESS_KEY  # AWS secret access key
REGION_NAME = "us-east-1"  # AWS region name

# Model evaluation and S3 bucket configuration
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE : float = 0.02  # Threshold for model evaluation score change
MODEL_BUCKET_NAME = "vehicle-model-bucket-1"  # S3 bucket name for model storage
MODEL_PUSHER_S3_KEY = "model-registry"  # S3 key for model registry
MODEL_FILE_NAME = "model.pkl"  # Model file name for S3 upload

# Application host and port configuration
APP_HOST = "0.0.0.0"  # Host for running the application
APP_PORT = 5000       # Port for running the application