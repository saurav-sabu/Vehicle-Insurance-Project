import json
import sys
import os
import pandas as pd

from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH

from src.utils.main_utils import read_yaml

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        Initialize DataValidation with ingestion artifact and validation config.
        Loads schema configuration from YAML file.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e, sys)
        
    def validate_number_of_columns(self, dataframe):
        """
        Validate if the number of columns in the dataframe matches the schema.
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is number of required columns present: [{status}]")
            return status
        except Exception as e:
            raise MyException(e, sys)
        
    def is_columns_exists(self, df):
        """
        Check if all required numerical and categorical columns exist in the dataframe.
        Logs missing columns if any.
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            # Check for missing numerical columns
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns) > 0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            # Check for missing categorical columns
            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns) > 0:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            # Return True if no columns are missing, else False
            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True
        
        except Exception as e:
            raise MyException(e, sys)
        
    @staticmethod
    def read_data(file_path):
        """
        Read CSV data from the given file path and return as a DataFrame.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)
        
    def initiate_data_validation(self):
        """
        Perform data validation on train and test datasets.
        Checks for correct number of columns and required columns.
        Writes validation report to file and returns DataValidationArtifact.
        """
        try:
            validation_error_msg = ""
            logging.info("Starting data Validation")

            # Read train and test data
            train_df = DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            # Validate number of columns in train data
            status = self.validate_number_of_columns(dataframe=train_df)
            if not status:
                validation_error_msg += "Columns are missing in training dataframe"
            else:
                logging.info("All required columns present in training dataframe")

            # Validate number of columns in test data
            status = self.validate_number_of_columns(dataframe=test_df)
            if not status:
                validation_error_msg += "Columns are missing in testing dataframe"
            else:
                logging.info("All required columns present in testing dataframe")

            # Validate required columns in train data
            status = self.is_columns_exists(df=train_df)
            if not status:
                validation_error_msg += "Columns are missing in training dataframe"
            else:
                logging.info("All required columns present in training dataframe")

            # Validate required columns in test data
            status = self.is_columns_exists(df=test_df)
            if not status:
                validation_error_msg += "Columns are missing in testing dataframe"
            else:
                logging.info("All required columns present in testing dataframe")

            # Determine overall validation status
            validation_status = len(validation_error_msg) == 0

            # Create DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            # Ensure report directory exists
            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            # Prepare validation report
            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_msg.strip()
            }

            # Write validation report to file
            with open(self.data_validation_config.validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4) 

            logging.info("Data validation artifact created and saved")
            return DataValidationArtifact
        
        except Exception as e:
            raise MyException(e, sys)