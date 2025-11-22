import os
import sys
import numpy as np
import pandas as pd
import pickle
import dill
from src.components.exception import CustomException
from src.components.logger import logging

def save_object(file_path: str, obj: object) -> None:
    """Saves a Python object to a file using dill serialization.

    Args:
        file_path (str): The path to the file where the object will be saved.
        obj (object): The Python object to be saved.

    Raises:
        CustomException: If there is an error during the saving process.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        logging.info(f"Object saved successfully at {file_path}")
    except Exception as e:
        logging.error(f"Error saving object at {file_path}: {e}")
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models: dict, param: dict):
    """Train and evaluate multiple models using provided parameter grids.

    This will perform grid search (if parameters provided) for each model,
    fit the best estimator, compute R2 on the test set, and return a
    dict mapping model name -> test R2 score. The `models` dict will be
    updated in-place so that each entry points to the fitted estimator.
    """
    try:
        from sklearn.model_selection import GridSearchCV
    except Exception as e:
        logging.error("GridSearchCV import failed")
        raise CustomException(e, sys)

    report = {}
    best_params_report = {}

    for name, model in models.items():
        logging.info(f"Evaluating model: {name}")
        params = param.get(name, {}) if param is not None else {}

        if params:
            gs = GridSearchCV(model, params, cv=3, n_jobs=-1, verbose=0)
            gs.fit(X_train, y_train)
            best_estimator = gs.best_estimator_
            logging.info(f"Best params for {name}: {gs.best_params_}")
            best_params_report[name] = gs.best_params_
        else:
            best_estimator = model
            best_estimator.fit(X_train, y_train)
            best_params_report[name] = {}

        # replace model with fitted estimator
        models[name] = best_estimator

        # evaluate on test set
        try:
            pred = best_estimator.predict(X_test)
            from sklearn.metrics import r2_score
            score = r2_score(y_test, pred)
        except Exception:
            logging.exception(f"Failed to evaluate model {name}")
            score = float('-inf')

        report[name] = score
        logging.info(f"Model {name} test R2: {score}")

    return report, best_params_report