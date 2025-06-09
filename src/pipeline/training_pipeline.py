import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        # Initialize the data ingestion configuration object
        self.data_ingestion_config = DataIngestionConfig()

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
        

    def run_pipeline(self):
        """
        Runs the complete training pipeline:
        - Starts data ingestion
        - Handles exceptions using custom exception class
        """
        try:
            # Start the data ingestion process
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            # Raise a custom exception if any error occurs during pipeline run
            raise MyException(e,sys)