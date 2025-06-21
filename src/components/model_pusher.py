from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_estimator import VehicleEstimator
import sys

class ModelPusher:
    """
    Handles pushing the trained model to AWS S3 storage.
    """

    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifact,model_pusher_config:ModelPusherConfig):
        """
        Initializes ModelPusher with evaluation artifact and pusher config.

        Args:
            model_evaluation_artifact (ModelEvaluationArtifact): Contains path to trained model.
            model_pusher_config (ModelPusherConfig): Contains S3 bucket and model key path.
        """
        self.s3 = SimpleStorageService()  # Initialize S3 service
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        # Initialize estimator for uploading model to S3
        self.vehicle_estimator = VehicleEstimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path
        )

    def initiate_model_pusher(self):
        """
        Uploads the trained model to the specified S3 bucket.

        Returns:
            ModelPusherArtifact: Artifact containing S3 bucket and model path.
        """
        logging.info("Initiate Model Pusher for Model Trainer Class")
        try:
            logging.info("Uploading artifact folder to S3 bucket")

            # Save the trained model to S3 using the estimator
            self.vehicle_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            # Create artifact with S3 details
            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path
            )
            logging.info("Uploaded artifacts to S3 bucket")
            return model_pusher_artifact
        except Exception as e:
            # Raise custom exception if upload fails
            raise MyException(e,sys)