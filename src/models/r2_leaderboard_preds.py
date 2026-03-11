#  Let us first import material in this cell.
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor
from ..features.preprocessing import *


def get_leaderboard(df, gen_initials):
    X, y = df.drop('total_stats', axis=1), df['total_stats']
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=1)
    models = {
        'Ordinal': prep_catboost_ordinal(X_tr.copy(), X_te.copy(), gen_initials.copy(), []),  # Add here arguments
        'Native':  prep_catboost_native(X_tr.copy(), X_te.copy(), gen_initials.copy(), []),
        'LGBM':    prep_lightgbm(X_tr.copy(), X_te.copy(), gen_initials.copy(), []),
        # 'XGBoost': prep_xgboost_ohe(X_tr.copy(), X_te.copy(), gen_initials.copy()) Not working
    }

    leaderboard = []
    for name, (X_tr_p, X_te_p, gen_p, cats) in models.items():

        if 'Ordinal' in name or 'Native' in name:
            m = CatBoostRegressor(
                loss_function='RMSEWithUncertainty',  # Catboost has uncertainty computations inbuilt
                posterior_sampling=True,
                cat_features=[X_tr_p.columns.get_loc(c) for c in cats],
                iterations=2500,
                learning_rate=0.005,
                verbose=0)

            m.fit(X_tr_p, y_tr)
            gen_preds = m.virtual_ensembles_predict(
                gen_p, prediction_type='TotalUncertainty')  # This will give you val + unc
            test_preds = m.predict(X_te_p)[:, 0]  #  Choose column 0 from previous output to get r2
            gen10_vals = gen_preds[:, 0]
            gen10_uncs = gen_preds[:, 1]

        else:
            quantiles = [0.025, 0.5, 0.975]
            gen_preds_inter = []
            for q in quantiles:
                m = LGBMRegressor(
                    objective='quantile',
                    alpha=q,
                    n_estimators=2500,
                    learning_rate=0.005,
                    verbosity=-1)

                m.fit(X_tr_p, y_tr)
                gen_preds_inter.append(m.predict(gen_p))

            gen10_vals = gen_preds_inter[1]
            gen10_uncs = [(up-low)/2 for up, low in zip(gen_preds_inter[-1], gen_preds_inter[0])]

            # Fit the median/mid model for test preds
            m = LGBMRegressor(objective='quantile',
                              alpha=0.5,
                              n_estimators=2500,
                              learning_rate=0.005,
                              verbosity=-1)
            m.fit(X_tr_p, y_tr)
            test_preds = m.predict(X_te_p)

        # Preparing output
        r2 = r2_score(y_te, test_preds)
        leaderboard.append({'Model': name,
                            'R²': f"{r2:.3f}",
                            "Browt": f"{round(gen10_vals[0])} ± {round(gen10_uncs[0])}",
                            "Pombon": f"{round(gen10_vals[1])} ± {round(gen10_uncs[1])}",
                            "Gecqua": f"{round(gen10_vals[-1])} ± {round(gen10_uncs[-1])}"
                            })

    pred_df = pd.DataFrame(leaderboard)
    pred_df = pred_df.sort_values('R²', ascending=False).reset_index(drop=True)
    return pred_df
