import os
import sys

import numpy as np
import dill
import yaml

from src.exception import MyException
from src.logger import logging

def read_yaml(file_path: str):
    """
    Reads a YAML file and returns its contents as a Python object.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML file content.

    Raises:
        MyException: If any exception occurs during file reading or parsing.
    """
    try:
        # Open the YAML file in binary read mode
        with open(file_path, "rb") as yaml_file:
            # Parse and return the YAML content
            return yaml.safe_load(yaml_file)
    except Exception as e:
        # Raise custom exception if any error occurs
        raise MyException(e, sys)

def load_object(file_path: str):
    """
    Loads a Python object from a file using dill.

    Args:
        file_path (str): Path to the file containing the serialized object.

    Returns:
        object: The deserialized Python object.

    Raises:
        MyException: If any exception occurs during file loading or deserialization.
    """
    try:
        # Open the file in binary read mode
        with open(file_path, "rb") as file_obj:
            # Load and return the object using dill
            obj = dill.load(file_obj)
        return obj
    except Exception as e:
        # Raise custom exception if any error occurs
        raise MyException(e, sys)
    
    

def save_object(file_path,obj):
    """
    Saves a Python object to a file using dill.

    Args:
        file_path (str): Path to the file where the object will be saved.

    Raises:
        MyException: If any exception occurs during file saving or serialization.
    """
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Open the file in binary write mode and serialize the object
        with open(file_path, "wb") as file_object:
            dill.dump(obj, file_object)
    except Exception as e:
        # Raise custom exception if any error occurs
        raise MyException(e, sys)
    

def save_numpy_data(file_path,array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise MyException(e,sys)
    

def load_numpy_data(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MyException(e,sys)
