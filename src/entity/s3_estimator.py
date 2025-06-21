from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel
from src.logger import logging
import sys
from pandas import DataFrame

class VehicleEstimator:
    """
    Class to handle loading, saving, and predicting with a vehicle insurance model stored in AWS S3.
    """

    def __init__(self, bucket_name, model_path):
        """
        Initialize the VehicleEstimator with S3 bucket details and model path.
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model = None
        logging.info(f"VehicleEstimator initialized with bucket: {bucket_name}, model_path: {model_path}")

    def is_model_present(self, model_path):
        """
        Check if the model exists in the specified S3 bucket.

        Args:
            model_path (str): The S3 key/path for the model.

        Returns:
            bool: True if model exists, False otherwise.
        """
        try:
            logging.info(f"Checking if model exists at {model_path} in bucket {self.bucket_name}")
            # Check if the model file exists in S3
            present = self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
            logging.info(f"Model presence at {model_path}: {present}")
            return present
        except Exception as e:
            logging.error(f"Error checking model presence: {e}")
            raise MyException(e, sys)

    def load_model(self):
        """
        Load the model from S3.

        Returns:
            Loaded model object.
        """
        try:
            logging.info(f"Loading model from {self.model_path} in bucket {self.bucket_name}")
            model = self.s3.load_model(self.model_path, bucket_name=self.bucket_name)
            logging.info("Model loaded successfully.")
            return model
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise MyException(e, sys)
    
    def save_model(self, from_file, remove=False):
        """
        Upload the model file to S3.

        Args:
            from_file (str): Local path to the model file.
            remove (bool): Whether to remove the local file after upload.
        """
        try:
            logging.info(f"Uploading model from {from_file} to {self.model_path} in bucket {self.bucket_name}")
            # Upload the model file to S3
            self.s3.upload_file(
                from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove
            )
            logging.info("Model upload successful.")
        except Exception as e:
            logging.error(f"Error uploading model: {e}")
            raise MyException(e, sys)
        
    def predict(self, dataframe):
        """
        Make predictions using the loaded model.

        Args:
            dataframe (DataFrame): Input data for prediction.

        Returns:
            Prediction results from the model.
        """
        try:
            if self.loaded_model is None:
                logging.info("Model not loaded. Loading model now.")
                # Load the model if not already loaded
                self.loaded_model = self.load_model()
            logging.info("Making predictions.")
            # Make predictions using the loaded model
            predictions = self.loaded_model.predict(dataframe=dataframe)
            logging.info("Predictions made successfully.")
            return predictions
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise MyException(e, sys)
