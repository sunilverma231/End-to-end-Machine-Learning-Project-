import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.components.exception import CustomException
from src.components.logger import logging
from src.components.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test input data")

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(objective="reg:squarederror"),
                "CatBoost Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            params = {
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest":{
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoost Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }

            # Evaluate models (returns scores and best params per model)
            model_report, best_params_report = evaluate_models(
                X_train=X_train, y_train=y_train,
                X_test=X_test, y_test=y_test,
                models=models, param=params
            )

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            logging.info(f"Best Model: {best_model_name} → Score: {best_model_score}")
            # Log best hyperparameters for transparency
            best_params = best_params_report.get(best_model_name, {})
            if best_params:
                logging.info(f"Best hyperparameters for {best_model_name}: {best_params}")
            else:
                logging.info(f"No hyperparameters were searched for {best_model_name} (default parameters used)")

            if best_model_score < 0.6:
                logging.warning("Model score below threshold of 0.6 — continuing anyway")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
