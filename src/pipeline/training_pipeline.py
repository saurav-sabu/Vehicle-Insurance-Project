import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig,ModelPusherConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelPusherArtifact,ModelEvaluationArtifact

class TrainPipeline:
    def __init__(self):
        # Initialize configuration objects for each pipeline stage
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_eval_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Starts the data ingestion process:
        - Logs the process steps
        - Initiates data ingestion from MongoDB
        - Returns the data ingestion artifact
        """
        try:
            logging.info("Entered the data ingestion method of training pipeline")
            logging.info("Getting data from mongodb")
            # Create a DataIngestion object with the configuration
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            # Start the data ingestion process and get the artifact
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got train and test data from mongoDB")
            logging.info("Exited the data ingestion method of training pipeline")
            return data_ingestion_artifact
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        """
        Starts the data validation process:
        - Logs the process steps
        - Validates the ingested data
        - Returns the data validation artifact
        """
        logging.info("Entered the start_data_validation function in training pipeline")
        try:
            # Create a DataValidation object with the ingestion artifact and config
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config
            )
            # Start the data validation process and get the artifact
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start data validation method")
            return data_validation_artifact
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e, sys)
        

    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact):
        """
        Starts the data transformation process:
        - Uses the artifacts from ingestion and validation
        - Applies data transformation logic
        - Returns the data transformation artifact
        """
        try:
            # Create a DataTransformation object with the required artifacts and config
            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact  # Pass validation artifact
            )
            # Start the data transformation process and get the artifact
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e, sys)
        

    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact):
        """
        Starts the model training process:
        - Uses the data transformation artifact
        - Trains the model and returns the model trainer artifact
        """
        try:
            # Create a ModelTrainer object with the transformation artifact and config
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config)
            # Start the model training process and get the artifact
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e,sys)
        
    def start_model_evaluation(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_artifact:ModelTrainerArtifact):
        """
        Starts the model evaluation process:
        - Uses the transformation and trainer artifacts
        - Evaluates the trained model and returns the evaluation artifact
        """
        try:
            # Create a ModelEvaluation object with the required configs and artifacts
            model_evaluation = ModelEvaluation(model_eval_config=self.model_eval_config,
                                               data_transformation_artifact=data_transformation_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            # Start the model evaluation process and get the artifact
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e,sys)
        
    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        """
        Starts the model pusher process:
        - Uses the model evaluation artifact
        - Pushes the accepted model to deployment/storage
        - Returns the model pusher artifact
        """
        try:
            # Create a ModelPusher object with the evaluation artifact and config
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                       model_pusher_config=self.model_pusher_config)
            # Start the model pusher process and get the artifact
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        
        except Exception as e:
            # Raise a custom exception if any error occurs
            raise MyException(e,sys)


    def run_pipeline(self):
        """
        Runs the complete training pipeline:
        - Starts data ingestion
        - Starts data validation
        - Starts data transformation
        - Starts model training
        - Starts model evaluation
        - Handles exceptions using custom exception class
        """
        try:
            # Start the data ingestion process
            data_ingestion_artifact = self.start_data_ingestion()
            # Start the data validation process
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            # Start the data transformation process
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            # Start the model training process
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            # Start the model evaluation process
            model_evaluation_artifact = self.start_model_evaluation(data_transformation_artifact=data_transformation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            
            # Check if the model is accepted before pushing
            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Model not accepted")
                return None
            
            # Start the model pusher process
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
        except Exception as e:
            # Raise a custom exception if any error occurs during pipeline run
            raise MyException(e, sys)