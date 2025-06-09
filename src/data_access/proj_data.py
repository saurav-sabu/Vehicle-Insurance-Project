import sys
import pandas as pd
import numpy as np

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException
from typing import Optional

class ProjData:
    """
    Data access class for project data stored in MongoDB.
    """

    def __init__(self):
        """
        Initializes the MongoDB client using the specified database name.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            # Raise a custom exception if initialization fails
            raise MyException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str]=None):
        """
        Exports a MongoDB collection as a pandas DataFrame.

        Args:
            collection_name (str): Name of the MongoDB collection.
            database_name (str): Name of the MongoDB database.

        Returns:
            pd.DataFrame: DataFrame containing the collection data.
        """
        try:
            # Select the collection from the specified or default database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            print("Fetching data from MongoDB")
            # Fetch all documents from the collection and convert to DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Drop the 'id' column if it exists
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)
            # Replace 'na' string values with np.nan
            df.replace({"na": np.nan}, inplace=True)
            return df
        
        except Exception as e:
            # Raise a custom exception if export fails
            raise MyException(e, sys)