import sys
import logging

def error_message_detail(error, error_detail):
    """
    Generates a detailed error message including the file name and line number where the error occurred,
    logs the error message, and returns it.

    Args:
        error (Exception): The exception object that was raised.
        error_detail (module): The sys module or similar, used to extract exception info.

    Returns:
        str: A formatted error message with file name and line number.
    """
    # Extract traceback information from the exception details
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename  # Get the file name where the exception occurred

    line_number = exc_tb.tb_lineno  # Get the line number where the exception occurred

    # Format the error message with file name and line number
    error_message = (
        f"Error Occurred in python script:[{file_name} at line number [{line_number}]]: {str(error)}"
    )

    logging.error(error_message)  # Log the error message

    return error_message  # Return the formatted error message


class MyException(Exception):
    """
    Custom exception class for handling application-specific errors.
    Args:
        error_message (str): The error message describing the exception.
        error_detail (Any): Additional details about the error (e.g., traceback or context).
    Attributes:
        error_message (str): The formatted error message with details.
    Methods:
        __str__(): Returns the formatted error message as a string.
    # Note:
    # The error_message is processed using the error_message_detail function,
    # which should combine the message and details into a single string.
    """
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)

        self.error_message = error_message_detail(error_message,error_detail)


    def __str__(self):
        return self.error_message



