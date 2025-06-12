from dataclasses import dataclass

# Data class to store file paths for data ingestion artifacts
@dataclass
class DataIngestionArtifact:
    trained_file_path : str  # Path to the file containing the training dataset
    test_file_path : str     # Path to the file containing the test dataset

@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str
    validation_report_file_path: str