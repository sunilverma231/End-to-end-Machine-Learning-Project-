from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.logger import logging


def run_pipeline():
    logging.info("Starting training pipeline")

    # Data ingestion
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()
    logging.info(f"Data ingestion completed: train={train_path}, test={test_path}")

    # Data transformation
    transformer = DataTransformation()
    train_arr, test_arr, preprocessor_path = transformer.initiate_data_transformation(train_path, test_path)
    logging.info(f"Data transformation completed. Preprocessor saved to {preprocessor_path}")

    # Model training
    trainer = ModelTrainer()
    r2 = trainer.initiate_model_trainer(train_arr, test_arr)
    logging.info(f"Model training completed. Test R2: {r2}")


if __name__ == "__main__":
    run_pipeline()
