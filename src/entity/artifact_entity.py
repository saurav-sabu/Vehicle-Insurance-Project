from dataclasses import dataclass

# Data class to store file paths for data ingestion artifacts
@dataclass
class DataIngestionArtifact:
    trained_file_path : str  # Path to the file containing the training dataset
    test_file_path : str     # Path to the file containing the test dataset