import joblib
import numpy as np
import pandas as pd

from pathlib import Path

from pokeml.utils.utils_train import get_model, regression_metrics
from pokeml.visualisation.residual_plot import residual_scatter


def real_vs_predicted(
        input_model: str,
        input_data: dict
) -> dict:

    metrics = []

    # Results

    the_model = joblib.load(Path(f"artifacts/models/{input_model}.joblib"))
    model_name = get_model(input_model)

    X_train, X_val, y_train, y_val, _ = input_data[model_name]
    y_val_real = np.asarray(y_val).ravel()  # Transform to simple list

    # Computing validation and training values
    y_pred_train, uncs_train = the_model.predict_unc(X_train)
    y_pred_val, uncs_val = the_model.predict_unc(X_val)

    # Computing residuals
    residuals_val = np.asarray(y_val - y_pred_val)
    max_residual_val = float(np.max(np.abs(residuals_val)))

    # Computing regression metrics for each train/val
    train_metrics = regression_metrics(y_train, y_pred_train)
    validation_metrics = regression_metrics(y_val, y_pred_val)

    # Saving information in dictionary to be displayed
    metrics.append(
        {'model': model_name,
            'tr_R2': train_metrics['R2'],
            'tr_RMSE': train_metrics['RMSE'],
            'tr_MAE': train_metrics['MAE'],
            'val_R2': validation_metrics['R2'],
            'val_RMSE': validation_metrics['RMSE'],
            'val_MAE': validation_metrics['MAE'],
            'overfit_R2': float(train_metrics['R2'] - validation_metrics['R2']),
            'overfit_RMSE': float(train_metrics['RMSE']-validation_metrics['RMSE']),
            'max_res': max_residual_val
         }
    )

    # Creating scatter plots of residuals and saving
    dic_model = {'y_real': y_val,
                 'y_pred': y_pred_val,
                 'uncs': uncs_val}

    residual_scatter(input_model, y_pred_val, y_val_real, uncs_val)

    # Saving metrics to csv

    out_dir = Path(f'artifacts/training/')
    out_dir.mkdir(parents=True, exist_ok=True)

    metrics_data = pd.DataFrame(metrics)
    metrics_data.to_csv(f"{out_dir}/metrics_data_{input_model}.csv", index=False)
