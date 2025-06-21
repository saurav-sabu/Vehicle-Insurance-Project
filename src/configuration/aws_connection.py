import boto3
import os
from src.constants import AWS_ACCESS_KEY_ID_ENV_KEY, AWS_SECRET_ACCESS_KEY_ENV_KEY, REGION_NAME

class S3Client:
    # Class variables to hold the singleton S3 client and resource
    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        # Initialize the S3 client and resource only once (singleton pattern)
        if S3Client.s3_resource is None or S3Client.s3_client is None:
            # Get AWS credentials from constants (these should be environment variable keys)
            __access_key_id = AWS_ACCESS_KEY_ID_ENV_KEY
            __secret_access_key = AWS_SECRET_ACCESS_KEY_ENV_KEY

            # Raise exception if credentials are not set
            if __access_key_id is None:
                raise Exception(f"AWS Access ID is not set")
            if __secret_access_key is None:
                raise Exception(f"AWS Secret Access Key is not set")
            
            # Create the S3 resource using boto3
            S3Client.s3_resource = boto3.resource(
                's3',
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
            )
            
            # Create the S3 client using boto3
            S3Client.s3_client = boto3.client(
                's3',
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
            )
        
        # Assign the class-level S3 resource and client to the instance
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client