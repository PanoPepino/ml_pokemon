from catboost import CatBoostRegressor
import catboost as cb
from lightgbm import LGBMRegressor
from psutil import virtual_memory
from sklearn.base import BaseEstimator, RegressorMixin

# In this .py file I will design two Classes that will be the general models with several functions like fit, predict value and predict uncertainties.


class Cat_Trainer(BaseEstimator, RegressorMixin):  # To inherit other inbuilt funcs from other models
    """
    This Class a general CatBoost Model trainer. It has several in-built function to easily fit and train your model.

    Args:
    - It can eat some **params, i.e. a dictionary of parameters to pass when training!
    Methods:

        - fit (x,y): The data for training.
        - predict_val (test_data): The data X_test as input to predict its y.
        - predict_unc (test_data): CatBoost has built-in some methods to predict uncertainties of y.
    """

    def __init__(self,
                 cat_features=None,
                 **params):
        self.cat_features = cat_features or []
        self.params = {
            'loss_function': 'RMSEWithUncertainty',
            'posterior_sampling': True,
            'learning_rate': 0.01,
            'verbose': 0,
            **params}
        self.model = None
        # print(self.cat_features) To check if new cats have been added.

    def fit(self, x, y, eval_set=None, cat_features=None, **kwargs):
        all_features = [x.columns.get_loc(c) for c in self.cat_features]
        # print(all_features) To check all cats have been converted

        self.model = CatBoostRegressor(cat_features=all_features, **self.params)
        self.model.fit(x.copy(), y, eval_set=eval_set, cat_features=cat_features, **kwargs)
        return self

    def predict(self, test_data):
        return self.model.predict(test_data)[:, 0]

    def predict_unc(self, test_data):
        val_unc = self.model.virtual_ensembles_predict(test_data, prediction_type='TotalUncertainty')
        vals = val_unc[:, 0]
        uncs = val_unc[:, 1]
        return vals, uncs

    def get_params(self, deep=True):  # This is to clone **params to pass in the cross_validation, as cross_validation does not have my in-built models
        tunable_params = {
            'learning_rate': self.params.get('learning_rate'),
            'max_depth': self.params.get('max_depth'),
            'iterations': self.params.get('iterations'),
            'l2_leaf_reg': self.params.get('l2_leaf_reg'),
            'random_strength': self.params.get('random_strength'),
            'bagging_temperature': self.params.get('bagging_temperature'),
            'n_estimators': self.params.get('n_estimators')
            # Add others you tune: 'border_count', 'rsm', etc
        }
        tunable_params = {k: v for k, v in tunable_params.items() if v is not None}
        return {'cat_features': self.cat_features, **tunable_params}

    def set_params(self, **params):
        if hasattr(self, 'cat_features') and 'cat_features' in params:
            self.cat_features = params.pop('cat_features')
        self.params.update(params)
        self.model = None  # Reset fitted model
        if hasattr(self, 'median_model'):
            self.median_model = self.quantile_models = None
        return self


class LGBM_Trainer(BaseEstimator, RegressorMixin):
    """
    This Class a general LGBM Model trainer. It has several in-built function to easily fit and train your model.

    Args:
    - It can eat some **params, i.e. a dictionary of parameters to pass when training!
    Methods:

        - fit (x,y): The data for training.
        - predict_val (test_data): The data X_test as input to predict its y.
        - predict_unc (test_data): CatBoost has built-in some methods to predict uncertainties of y.
    """

    def __init__(self, **params):
        self.params = {'n_estimators': 2500,
                       'learning_rate': 0.01,
                       'verbosity': -1,
                       **params}
        self.median_model = None
        self.quantile_models = None

    def fit(self, x, y, eval_set=None, **kwargs):
        # The median value
        self.median_model = LGBMRegressor(objective='quantile',
                                          alpha=0.5,
                                          **self.params)
        self.median_model.fit(x, y)

        # The upper and lower for uncerteainty
        quants = [0.1, 0.9]
        self.quantile_models = {quant: LGBMRegressor(
            objective='quantile', alpha=quant, **self.params).fit(x, y) for quant in quants}

        return self

    def predict(self, X):
        return self.median_model.predict(X)

    def predict_unc(self, X):
        low = self.quantile_models[0.1].predict(X)
        high = self.quantile_models[0.9].predict(X)

        return (low + high)/2, (high - low)/2

    def get_params(self, deep=True):
        tunable = {k: v for k, v in self.params.items()
                   if k in ['learning_rate', 'n_estimators', 'num_leaves', 'reg_lambda']}
        return tunable

    def set_params(self, **params):
        if hasattr(self, 'cat_features') and 'cat_features' in params:
            self.cat_features = params.pop('cat_features')
        self.params.update(params)
        self.model = None  # Reset fitted model
        if hasattr(self, 'median_model'):
            self.median_model = self.quantile_models = None
        return self
