from sklearn.model_selection import RandomizedSearchCV
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error
from ..models.trainers import Cat_Trainer, LGBM_Trainer


def tuning(prep_data, some_params, search_iter):
    """
    This function will search the best possible parameters to fit the model to get the best predictions.

    Args:
        prep_data (DatFrame): The data already encoded, imputed and properly massaged.
        some_params (Dict): The grid of parameters to search around
        search_iter (integer): The amount of times the process repeats.

    Returns:
        Dict: A dictionary containing the best possible parameter tunning for each model.
    """

    # Create empty rows to be append with info. Then throw basic decission tree.
    results = []
    future_fit = {}

    for name, (X_tr_p, X_te_p, _, cats, y_tr, y_te, _) in prep_data.items():

        if name in ("ordinal", "native"):
            trainer = Cat_Trainer(cat_features=cats)
            cv_kwargs = some_params['catboost']
            fit_kwargs = {'eval_set': (X_te_p, y_te)}

        else:
            trainer = LGBM_Trainer()
            cv_kwargs = some_params['light_gbm']
            fit_kwargs = {'eval_set': [(X_te_p, y_te)]}

        search = RandomizedSearchCV(trainer,
                                    cv_kwargs,
                                    n_iter=search_iter,
                                    cv=3,
                                    scoring='neg_mean_absolute_error',
                                    random_state=1,
                                    verbose=0)
        search.fit(X_tr_p, y_tr)

        best = search.best_estimator_
        best.fit(X_tr_p, y_tr, **fit_kwargs)
        y_pred = best.predict(X_te_p)
        r2_preds = r2_score(y_te, y_pred)

        results.append({
            'model': name,
            'cv_r2': - search.best_score_,
            'R2': r2_preds,
            'MAE': mean_absolute_error(y_te, y_pred),
            'best_params': search.best_params_
        })
        future_fit.update({
            name: search.best_params_
        })
    pd.DataFrame(results)

    return future_fit
