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
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
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
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)
        return obj
    except Exception as e:
        raise MyException(e, sys)
    

