import os
import pymongo
import sys

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

class MongoDBClient:
    # Class variable to hold the MongoDB client instance (singleton pattern)
    client = None

    def __init__(self, database_name: str = DATABASE_NAME):
        """
        Initializes the MongoDBClient instance.
        Establishes a connection to the MongoDB database if not already connected.
        """
        try:
            # Check if the client is already initialized
            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY  # Get MongoDB URL from constants
                if mongo_db_url is None:
                    # Raise exception if the MongoDB URL is not set
                    raise Exception(f"Environment Variable is not set")
                
                # Create a new MongoDB client
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)

                # Assign the client and database to instance variables
                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
                logging.info("MongoDB connection is established")

        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e, sys)