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
    artifact_dir: str = os.path.join(ARTFACT_DIR, TIME_STAMP)
    # Timestamp for this pipeline run
    timestamp: str = TIME_STAMP

# Create a global instance of TrainingPipelineConfig
training_pipeline_config : TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    # Directory for data ingestion artifacts
    data_ingestion_dir : str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    # Path to the feature store file
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    # Path to the training data file
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    # Path to the testing data file
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    # Ratio for splitting data into train and test sets
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    # Name of the collection in the data source (e.g., database)
    collection_name: str = DATA_INGESTION_COLLECTION_NAME

@dataclass
class DataValidationConfig:
    # Directory for data validation artifacts
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    # Path to the validation report file
    validation_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_REPORT_FILE_NAME)

@dataclass
class DataTransformationConfig:
    # Directory for data transformation artifacts
    data_transformation_dir : str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
    # Path to the transformed training data file (in .npy format)
    transformed_train_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TRAIN_FILE_NAME.replace("csv", "npy")
    )
    # Path to the transformed testing data file (in .npy format)
    transformed_test_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
        TEST_FILE_NAME.replace("csv", "npy")
    )
    # Path to the serialized preprocessing object file
    transformed_object_file_path: str = os.path.join(
        data_transformation_dir,
        DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        PREPROCESSING_OBJECT_FILE_NAME
    )

@dataclass
class ModelTrainerConfig:
    # Directory for model trainer artifacts
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
    # Path to the trained model file
    trained_model_file_path: str = os.path.join(model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME)
    # Expected accuracy for the model
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE 
    # Path to the model config file
    model_config_file_path = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    # Number of estimators for the model
    _n_estimators = MODEL_TRAINER_N_ESTIMATORS
    # Minimum samples required to split an internal node
    _min_samples_split = MODEL_TRAINER_MIN_SAMPLES_SPLIT
    # Minimum samples required to be at a leaf node
    _min_samples_leaf = MODEL_TRAINER_MIN_SAMPLES_LEAF
    # Maximum depth of the tree
    _max_depth = MIN_SAMPLES_SPLIT_MAX_DEPTH
    # Criterion for splitting
    _criterion = MIN_SAMPLES_SPLIT_CRITERION
    # Random state for reproducibility
    _random_state = MIN_SAMPLES_SPLIT_RANDOM_STATE

@dataclass
class ModelEvaluationConfig:
    # Threshold score to determine if model performance has changed
    changed_threshold_score: float = MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE
    # Name of the S3 bucket for model storage
    bucket_name: str = MODEL_BUCKET_NAME
    # S3 key path for the model file
    s3_model_key_path: str = MODEL_FILE_NAME

@dataclass
class ModelPusherConfig:
    # Name of the S3 bucket for model pushing
    bucket_name:str = MODEL_BUCKET_NAME
    # S3 key path for the model file to be pushed
    s3_model_key_path: str = MODEL_FILE_NAME

@dataclass
class VehiclePredictorConfig:
    # Path to the model file for prediction
    model_file_path: str = MODEL_FILE_NAME
    # Name of the S3 bucket containing the model
    model_bucket_name : str = MODEL_BUCKET_NAME