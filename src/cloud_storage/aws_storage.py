import boto3
from src.configuration.aws_connection import S3Client
from src.logger import logging
from src.exception import MyException
import pickle
from mypy_boto3_s3.service_resource import Bucket
import sys
import os

class SimpleStorageService:
    def __init__(self):
        """
        Initialize the SimpleStorageService with S3 resource and client.
        """
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource  # S3 resource object for high-level operations
        self.s3_client = s3_client.s3_client      # S3 client object for low-level operations
        logging.info("Initialized SimpleStorageService with S3 resource and client.")

    def s3_key_path_available(self, bucket_name, s3_key):
        """
        Check if a given S3 key path exists in the specified bucket.

        Args:
            bucket_name (str): Name of the S3 bucket.
            s3_key (str): Key path to check in the bucket.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        try:
            logging.info(f"Checking if key '{s3_key}' exists in bucket '{bucket_name}'.")
            bucket = self.get_bucket(bucket_name)  # Get the bucket resource
            # Filter objects in the bucket with the given prefix (key)
            file_object = [file_obj for file_obj in bucket.objects.filter(Prefix=s3_key)]
            exists = len(file_object) > 0
            logging.info(f"Key '{s3_key}' exists: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Error checking key path: {e}")
            raise MyException(e, sys)

    def get_bucket(self, bucket_name):
        """
        Get the S3 bucket resource object.

        Args:
            bucket_name (str): Name of the S3 bucket.

        Returns:
            Bucket: S3 bucket resource object.
        """
        try:
            logging.info(f"Getting bucket resource for '{bucket_name}'.")
            bucket = self.s3_resource.Bucket(bucket_name)
            return bucket
        except Exception as e:
            logging.error(f"Error getting bucket '{bucket_name}': {e}")
            raise MyException(e, sys)

    def get_file_object(self, file_name, bucket_name):
        """
        Retrieve file object(s) from the specified bucket and file name.

        Args:
            file_name (str): Name (key) of the file in S3.
            bucket_name (str): Name of the S3 bucket.

        Returns:
            S3 Object(s): The file object(s) matching the file_name.
        """
        try:
            logging.info(f"Retrieving file object '{file_name}' from bucket '{bucket_name}'.")
            bucket = self.get_bucket(bucket_name)
            # Filter objects in the bucket with the given prefix (file_name)
            file_object = [file_obj for file_obj in bucket.objects.filter(Prefix=file_name)]
            # If only one object is found, return it directly; otherwise, return the list
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(file_object)
            logging.info(f"Retrieved file object(s): {file_objs}")
            return file_objs
        except Exception as e:
            logging.error(f"Error retrieving file object '{file_name}': {e}")
            raise MyException(e, sys)

    def load_model(self, model_name, bucket_name, model_dir=None):
        """
        Load a pickled model from S3.

        Args:
            model_name (str): Name of the model file.
            bucket_name (str): Name of the S3 bucket.
            model_dir (str, optional): Directory in S3 where the model is stored.

        Returns:
            object: The loaded model object.
        """
        try:
            # Construct the full path to the model file in S3
            model_file = model_dir + "/" + model_name if model_dir else model_name
            logging.info(f"Loading model '{model_file}' from bucket '{bucket_name}'.")
            file_object = self.get_file_object(model_file, bucket_name)
            # Download the file object from S3 and load the pickle
            if hasattr(file_object, 'get'):
                file_content = file_object.get()['Body'].read()
                model = pickle.loads(file_content)
                logging.info(f"Model '{model_file}' loaded successfully.")
                return model
            else:
                logging.error(f"File object for '{model_file}' not found or invalid.")
                raise MyException(f"File object for '{model_file}' not found or invalid.", sys)
        except Exception as e:
            logging.error(f"Error loading model '{model_name}': {e}")
            raise MyException(e, sys)
        

    def upload_file(self, from_filename, to_filename, bucket_name, remove=True):
        """
        Upload a local file to S3 and optionally remove it locally.

        Args:
            from_filename (str): Path to the local file to upload.
            to_filename (str): Destination key (path) in the S3 bucket.
            bucket_name (str): Name of the S3 bucket.
            remove (bool, optional): Whether to remove the local file after upload. Default is True.
        """
        try:
            logging.info(f"Uploading {from_filename} to {to_filename} in {bucket_name}")
            # Upload the file to S3
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            logging.info(f"Uploaded {from_filename} to {to_filename} in {bucket_name}")

            # Remove the local file if specified
            if remove:
                os.remove(from_filename)
                logging.info(f"Removed the local file {from_filename} after upload")

        except Exception as e:
            raise MyException(e, sys)
