import os
import sys
import pandas 
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import MyException
from src.logger import logging
from src.data_access.proj_data import ProjData

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        Constructor for DataIngestion class.
        Initializes the data ingestion configuration.
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)
        
    def export_data_into_feature_store(self):
        """
        Exports data from MongoDB and saves it as a CSV file in the feature store.
        Returns the dataframe.
        """
        try:
            logging.info("Exporting data from mongoDB")
            my_data = ProjData()
            # Export data from the specified MongoDB collection as a DataFrame
            dataframe = my_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            # Create directory if it doesn't exist
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into feature store path: {feature_store_file_path}")
            # Save DataFrame to CSV
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise MyException(e,sys)
        

    def split_data_as_train_test(self,dataframe):
        """
        Splits the dataframe into train and test sets and saves them as CSV files.
        """
        try:
            # Split the data into train and test sets
            train_set , test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Splitting into train and test set")
            logging.info("Exited train test method")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            # Create directory if it doesn't exist
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test filepath")
            # Save train and test sets to CSV files
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info("Exported train and test file")

        except Exception as e:
            raise MyException(e,sys)
        

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Orchestrates the data ingestion process: exports data, splits it, and returns an artifact.
        """
        try:
            # Export data from MongoDB to feature store
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")
            # Split data into train and test sets
            self.split_data_as_train_test(dataframe)
            logging.info("Train test split performed on data")
            logging.info("Exited from initiate data ingestion method")
            # Create and return DataIngestionArtifact with file paths
            data_ingestion_artifact = DataIngestionArtifact(
                    trained_file_path=self.data_ingestion_config.training_file_path,
                    test_file_path = self.data_ingestion_config.testing_file_path
                    )
            return data_ingestion_artifact
            
        except Exception as e:
            raise MyException(e,sys)