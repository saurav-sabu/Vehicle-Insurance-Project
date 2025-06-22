from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from imblearn.combine import SMOTEENN

import sys
import numpy as np
import os
import pandas as pd

from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact, DataTransformationArtifact
from src.entity.config_entity import DataValidationConfig, DataTransformationConfig
from src.constants import SCHEMA_FILE_PATH,TARGET_COLUMN
from src.utils.main_utils import read_yaml, save_object, save_numpy_data, load_numpy_data


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        """
        Initialize DataTransformation with required artifacts and configs.
        Loads schema configuration from YAML.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml(file_path=SCHEMA_FILE_PATH)
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


    def get_data_transformer_object(self):
        """
        Create and return a data transformation pipeline for numeric and min-max features.
        """
        logging.info("Entered get_data_transformer_object method")
        try:
            # Standard scaler for numeric features
            numeric_transformer = StandardScaler()
            # MinMax scaler for specified columns
            min_max_scaler = MinMaxScaler()
            logging.info("transformer initialized")

            # Get feature lists from schema config
            num_features = self._schema_config["num_features"]
            mm_features = self._schema_config["mm_columns"]
            logging.info("Columns loaded")

            # Create column transformer for preprocessing
            preprocessor = ColumnTransformer(
                [
                    ("StandardScaler",numeric_transformer,num_features),
                    ("MinMaxScaler",min_max_scaler,mm_features)
                ],
                remainder="passthrough"
            )

            # Wrap preprocessor in a pipeline
            final_pipeline = Pipeline(steps=[("preprocessor",preprocessor)])
            logging.info("Final Pipeline created")
            logging.info("Exited get_data_transformer_object method")
            return final_pipeline
        
        except Exception as e:
            raise MyException(e,sys)
        

    def map_gender_column(self,df):
        """
        Map 'Gender' column to binary values: Female=0, Male=1.
        """
        logging.info("Mapping 'Gender' to binary values")
        df["Gender"] = df["Gender"].map({"Female":0,"Male":1}).astype(int)
        return df
    
    def map_vehicle_damage(self, df):
        """
        Map 'Vehicle_Damage' column to binary values: No=0, Yes=1.
        """
        logging.info("Mapping 'Vehicle_Damage' column to binary values: No=0, Yes=1")
        df["Vehicle_Damage"] = df["Vehicle_Damage"].map({"No": 0, "Yes": 1}).astype(int)
        logging.info("'Vehicle_Damage' column mapped successfully")
        return df

    def map_vehicle_age(self, df):
        """
        Map 'Vehicle_Age' column to integer codes:
        - "< 1 Year" -> 0
        - "1-2 Year" -> 1
        - "> 2 Years" -> 2
        Handles both string and numeric input types.
        """
        logging.info("Mapping 'Vehicle_Age' column to integer codes")
        if 'Vehicle_Age' in df.columns:
            if df['Vehicle_Age'].dtype == 'object':
                vehicle_age_mapping = {
                    "< 1 Year": 0,
                    "1-2 Year": 1,
                    "> 2 Years": 2
                }
                df["Vehicle_Age"] = df["Vehicle_Age"].map(vehicle_age_mapping).astype(int)
                logging.info("'Vehicle_Age' mapped from string to integer codes")
            else:
                df["Vehicle_Age"] = df["Vehicle_Age"].astype(int)
                logging.info("'Vehicle_Age' column already numeric, converted to int type")
        else:
            logging.info("'Vehicle_Age' column not found, skipping mapping")
        return df

    
    def drop_id_columns(self,df):
        """
        Drop ID or unwanted columns as specified in schema config.
        """
        logging.info("Drop id column")
        drop_col = self._schema_config["drop_columns"]
        if drop_col in df.columns:
            df = df.drop(drop_col,axis=1)
        return df
    
    def initiate_data_transformation(self):
        """
        Main method to perform data transformation:
        - Reads data
        - Applies custom transformations
        - Applies preprocessing pipeline
        - Applies SMOTEENN for balancing
        - Saves transformed objects and arrays
        - Returns DataTransformationArtifact
        """
        try:
            logging.info("Data Transformation Started")
            # Check validation status before proceeding
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            # Load transformed train and test data
            train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info("Tran and test loaded")

            # Separate input features and target for train and test
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            logging.info("Input and output both defined for train and test df")

            # Apply custom transformations to train data
            input_feature_train_df = self.map_gender_column(input_feature_train_df)
            input_feature_train_df = self.drop_id_columns(input_feature_train_df)
            input_feature_train_df = self.map_vehicle_age(input_feature_train_df)
            input_feature_train_df = self.map_vehicle_damage(input_feature_train_df)

            # Apply custom transformations to test data
            input_feature_test_df = self.map_gender_column(input_feature_test_df)
            input_feature_test_df = self.drop_id_columns(input_feature_test_df)
            input_feature_test_df = self.map_vehicle_age(input_feature_test_df)
            input_feature_test_df = self.map_vehicle_damage(input_feature_test_df)
            logging.info("Custom transformation applied")

            # Get preprocessing pipeline
            preprocessor = self.get_data_transformer_object()
            logging.info("Got the preprocessor object")

            # Transform train and test features
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info("Data transformation array created")

            # Apply SMOTEENN for balancing classes
            smt = SMOTEENN(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(input_feature_train_arr,target_feature_train_df)
            input_feature_test_final, target_feature_test_final = smt.fit_resample(input_feature_test_arr,target_feature_test_df)
            logging.info("SMOTEEN applied to both test and train")

            # Concatenate features and targets for saving
            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]
            logging.info("Feature tranformation done")

            # Save preprocessor and transformed arrays
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            save_numpy_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            logging.info("Saving objects")

            logging.info("Data Transformation completed")

            # Return artifact with file paths
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.transformed_test_file_path
            )
        
        except Exception as e:
            raise MyException(e,sys)
