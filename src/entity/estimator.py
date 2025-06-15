import sys
from src.logger import logging
from src.exception import MyException

class MyModel:
    def __init__(self, preprocessing_obj, trained_model_obj):
        """
        Initializes MyModel with preprocessing and trained model objects.

        Args:
            preprocessing_obj: Object used to preprocess input data.
            trained_model_obj: Trained model used for making predictions.
        """
        self.preprocessing_obj = preprocessing_obj
        self.trained_model_obj = trained_model_obj

    def predict(self, dataframe):
        """
        Transforms the input dataframe using the preprocessing object and
        makes predictions using the trained model.

        Args:
            dataframe: Input data as a pandas DataFrame.

        Returns:
            predictions: Model predictions on the transformed data.

        Raises:
            MyException: If any error occurs during prediction.
        """
        try:
            logging.info("Starting prediction process")
            # Transform the input features using the preprocessing object
            transformed_feature = self.preprocessing_obj.transform(dataframe)

            logging.info("Using trained model to get predictions")
            # Use the trained model to make predictions on the transformed features
            predictions = self.trained_model_obj.predict(transformed_feature)

            return predictions
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e, sys)