from src.entity.config_entity import VehiclePredictorConfig
from src.entity.s3_estimator import VehicleEstimator
from src.exception import MyException
from src.logger import logging
from pandas import DataFrame

import sys

class VehicleData:
    def __init__(self,
                 Gender,
                 Age,
                 Driving_License,
                 Region_Code,
                 Previously_Insured,
                 Annual_Premium,
                 Policy_Sales_Channel,
                 Vintage,
                 Vehicle_Age,
                 Vehicle_Damage):
        """
        Initialize VehicleData object with all required features.
        """
        try:
            logging.info("Initializing VehicleData object with provided features.")
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
            self.Vehicle_Age = Vehicle_Age
            self.Vehicle_Damage = Vehicle_Damage

        except Exception as e:
            logging.error(f"Error initializing VehicleData: {e}")
            raise MyException(e,sys)
        

    def get_vehicle_input_dataframe(self):
        """
        Returns a pandas DataFrame containing the vehicle data.
        """
        try:
            logging.info("Converting vehicle data to DataFrame.")
            vehicle_input_data = self.get_vehicle_data_as_dict()
            df = DataFrame(vehicle_input_data)
            logging.info(f"Vehicle input DataFrame created with shape: {df.shape}")
            return df
        
        except Exception as e:
            logging.error(f"Error creating DataFrame from vehicle data: {e}")
            raise MyException(e,sys)
        

    def get_vehicle_data_as_dict(self):
        """
        Returns the vehicle data as a dictionary.
        """
        try:
            logging.info("Converting vehicle data to dictionary.")
            input_data = {
                "Gender":[self.Gender],
                "Age":[self.Age],
                "Driving_License":[self.Driving_License],
                "Region_Code":[self.Region_Code],
                "Previously_Insured":[self.Previously_Insured],
                "Annual_Premium":[self.Annual_Premium],
                "Policy_Sales_Channel":[self.Policy_Sales_Channel],
                "Vintage":[self.Vintage],
                "Vehicle_Age":[self.Vehicle_Age],
                "Vehicle_Damage":[self.Vehicle_Damage]
            }
            logging.info(f"Vehicle data dictionary created: {input_data}")
            return input_data
        
        except Exception as e:
            logging.error(f"Error converting vehicle data to dictionary: {e}")
            raise MyException(e,sys)
        

class VehicleDataClassifer:

    def __init__(self,prediction_pipeline_config: VehiclePredictorConfig = VehiclePredictorConfig()):
        """
        Initialize VehicleDataClassifer with prediction pipeline configuration.
        """
        try:
            logging.info("Initializing VehicleDataClassifer with provided config.")
            self.prediction_pipeline_config = prediction_pipeline_config

        except Exception as e:
            logging.error(f"Error initializing VehicleDataClassifer: {e}")
            raise MyException(e,sys)
        

    def predict(self,dataframe):
        """
        Predicts the output using the trained model and input dataframe.
        """
        try:
            logging.info("Loading VehicleEstimator model for prediction.")
            model = VehicleEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path = self.prediction_pipeline_config.model_file_path
            )
            logging.info("Model loaded successfully. Starting prediction.")
            result = model.predict(dataframe)
            logging.info(f"Prediction completed. Result: {result}")
            return result
        
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise MyException(e,sys)
