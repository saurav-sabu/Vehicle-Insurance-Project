from dataclasses import dataclass

# Data class to store file paths for data ingestion artifacts
@dataclass
class DataIngestionArtifact:
    trained_file_path : str  # Path to the file containing the training dataset
    test_file_path : str     # Path to the file containing the test dataset

# Data class to store results and metadata from data validation step
@dataclass
class DataValidationArtifact:
    validation_status: bool                # Indicates if validation passed or failed
    message: str                           # Message or summary about the validation
    validation_report_file_path: str        # Path to the validation report file

# Data class to store file paths for data transformation artifacts
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str      # Path to the serialized transformation object (e.g., scaler, encoder)
    transformed_train_file_path: str       # Path to the transformed training dataset
    transformed_test_file_path: str        # Path to the transformed test dataset

# Data class to store classification metrics
@dataclass
class ClassificationMetricArtifact:
    f1_score : float                      # F1 score of the model
    precision_score: float                # Precision score of the model
    recall_score: float                   # Recall score of the model

# Data class to store model trainer artifacts, including metrics
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str          # Path to the trained model file
    metric_artifact: ClassificationMetricArtifact  # Classification metrics for the trained model