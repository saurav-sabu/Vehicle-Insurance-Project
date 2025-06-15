import sys
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import *
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact, ClassificationMetricArtifact
from src.entity.estimator import MyModel

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config: ModelTrainerConfig):
        # Initialize ModelTrainer with data transformation artifact and config
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self,train,test):
        """
        Trains a RandomForestClassifier on the training data and evaluates it on the test data.
        Returns the trained model and a metric artifact.
        """
        try:
            logging.info("Training RandomForestClassifier with specified parameters")
            # Split features and labels for train and test sets
            X_train,y_train,X_test,y_test = train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]
            logging.info("train and test split done")

            # Initialize RandomForestClassifier with parameters from config
            model = RandomForestClassifier(
                n_estimators=self.model_trainer_config._n_estimators,
                min_samples_leaf=self.model_trainer_config._min_samples_leaf,
                min_samples_split=self.model_trainer_config._min_samples_split,
                max_depth=self.model_trainer_config._max_depth,
                criterion=self.model_trainer_config._criterion,
                random_state=self.model_trainer_config._random_state
            )

            logging.info("Model Training going on")
            # Train the model
            model.fit(X_train,y_train)
            logging.info("Model Training Done")

            # Predict on test set
            y_pred = model.predict(X_test)
            # Calculate evaluation metrics
            accuracy = accuracy_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)

            # Create metric artifact
            metric_artifact = ClassificationMetricArtifact(f1_score=f1,precision_score=precision,recall_score=recall)
            return model, metric_artifact
        
        except Exception as e:
            # Raise custom exception in case of error
            raise MyException(e,sys)
        
    
    def initiate_model_trainer(self):
        """
        Loads transformed data, trains the model, evaluates it, and saves the model if performance is acceptable.
        Returns a ModelTrainerArtifact.
        """
        logging.info("Entered initiate Model Trainer")
        try:
            print("-------------------------------------------------------")
            print("Starting Model Trainer")

            # Load transformed training and testing data
            train_arr = load_numpy_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_data(self.data_transformation_artifact.transformed_test_file_path)
            logging.info("Train and test data loaded")

            # Train model and get metrics
            trained_model, metric_artifact = self.get_model_object_and_report(train_arr,test_arr)
            logging.info("Model oject and artifact loaded")

            # Load preprocessing object
            preprocessing_obj = load_object(self.data_transformation_artifact.transformed_object_file_path)
            logging.info("Preprocessing object loaded")

            # Check if model meets expected accuracy on training data
            if accuracy_score(train_arr[:,-1],trained_model.predict(train_arr[:,:-1])) < self.model_trainer_config.expected_accuracy:
                logging.info("No model found with score above the base score")
                raise Exception("No model found with score above the base score")
            
            logging.info("Saving new model as performance is better than previous one")
            # Create and save final model object
            my_model = MyModel(preprocessing_obj,trained_model)
            save_object(self.model_trainer_config.trained_model_file_path,my_model)
            logging.info("Saved final model object")

            # Create and return model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )
            logging.info("Model Trainer Artifact created")
            return model_trainer_artifact
        
        except Exception as e:
            # Raise custom exception in case of error
            raise MyException(e,sys)