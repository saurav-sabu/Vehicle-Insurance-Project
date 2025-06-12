import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

class TrainPipeline:
    def __init__(self):
        # Initialize the data ingestion and validation configuration objects
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion process:
        - Logs the process steps
        - Initiates data ingestion from MongoDB
        - Returns the data ingestion artifact
        """
        try:
            logging.info("Entered the data ingestion method of training pipeline")
            logging.info("Getting data from mongodb")
            # Create a DataIngestion object with the configuration
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            # Start the data ingestion process and get the artifact
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got train and test data from mongoDB")
            logging.info("Exited the data ingestion method of training pipeline")
            return data_ingestion_artifact
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        """
        Starts the data validation process:
        - Logs the process steps
        - Validates the ingested data
        - Returns the data validation artifact
        """
        logging.info("Entered the start_data_validation function in training pipeline")
        try:
            # Create a DataValidation object with the ingestion artifact and config
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            # Start the data validation process and get the artifact
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start data validation method")
            return data_validation_artifact
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e, sys)

    def run_pipeline(self):
        """
        Runs the complete training pipeline:
        - Starts data ingestion
        - Starts data validation
        - Handles exceptions using custom exception class
        """
        try:
            # Start the data ingestion process
            data_ingestion_artifact = self.start_data_ingestion()
            # Start the data validation process
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
        except Exception as e:
            # Raise a custom exception if any error occurs during pipeline run
            raise MyException(e, sys)