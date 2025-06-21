from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from src.exception import MyException
from src.utils.main_utils import load_object,load_numpy_data
from src.logger import logging
from src.constants import TARGET_COLUMN
from src.entity.s3_estimator import VehicleEstimator
from dataclasses import dataclass
import sys

@dataclass
class EvaluateModelResponse:
    # Stores the evaluation results
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:

    def __init__(self,
                 model_eval_config: ModelEvaluationConfig,
                 data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        """
        Initializes ModelEvaluation with config and artifacts.
        """
        try:
            self.model_eval_config = model_eval_config
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys)
        

    def get_best_model(self):
        """
        Loads the best model from S3 if present.
        """
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            estimator = VehicleEstimator(bucket_name=bucket_name,model_path=model_path)

            if estimator.is_model_present(model_path=model_path):
                return estimator
            
        except Exception as e:
            raise MyException(e,sys)
        
    
    def evaluate_model(self):
        """
        Compares the trained model with the best model (if any) using F1 score.
        Returns an EvaluateModelResponse.
        """
        try:
            # Load transformed test data
            test_df = load_numpy_data(self.data_transformation_artifact.transformed_test_file_path)

            x = test_df[:, :-1]  # All columns except last
            y = test_df[:, -1]   # Last column as target

            logging.info("Test data loaded and transformed")

            # Load the newly trained model
            trained_model = load_object(file_path=self.model_trainer_artifact.trained_model_file_path)
            logging.info("Trained model loaded")

            # Get F1 score of the trained model
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            logging.info(f"F1 score: {trained_model_f1_score}")

            best_model_f1_score = None
            best_model = self.get_best_model()

            # If a best model exists, compute its F1 score
            if best_model is not None:
                logging.info(f"Computing f1 score for production model")
                y_hat = best_model.predict(x)
                best_model_f1_score = f1_score(y,y_hat)
                logging.info(f"F1-score prod: {best_model_f1_score} and F1-score new:{trained_model_f1_score}")

            # If no best model, set score to 0
            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score

            # Prepare evaluation response
            result = EvaluateModelResponse(trained_model_f1_score=trained_model_f1_score,
                                           best_model_f1_score=best_model_f1_score,
                                           is_model_accepted=trained_model_f1_score>tmp_best_model_score,
                                           difference=trained_model_f1_score-tmp_best_model_score)
            
            logging.info(f"Result: {result}")
            return result
        
        except Exception as e:
            raise MyException(e,sys)
        

    
    def initiate_model_evaluation(self):
        """
        Initiates the model evaluation process and returns a ModelEvaluationArtifact.
        """
        try:
            print("------------------------------------------------------")
            logging.info("Initialized Model Evaluation")
            evaluate_model_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path

            # Create artifact with evaluation results
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference
            )

            logging.info("Model Evaluation Done")
            return model_evaluation_artifact
        
        except Exception as e:
            raise MyException(e,sys)