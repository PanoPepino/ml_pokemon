# Here, I will define 4 different preprocessors to adapt data before model training.
# For convenience, I have also defined a function to check shapes match after preprocessing.
# At the moment prep_xgboost_ohe does not work when running the model fit function.
# In any case, that does not seem like a big deal, as CatBoost seems to yield a better fitting.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Defining preprocessing for xgboost


def prep_xgboost_ohe(X_train,
                     X_test,
                     new_gen,  # Recall, we need to convert initials also:
                     cat_feats=None,  # Do not forget to rewrite if new features added
                     num_feats=None):  # same
    """
    Preprocessor for xgboost. Will onehot encode categorical features defined as input.

    Args:
        X_train (DataFrame): 
        X_test (DataFrame): 
        new_gen (DataFrame): 
        cat_feats, optional: To be enhance by input when feature eng.
        num_feats, optional: To be enhance by input when feature eng.


    Returns:
        X_train, X_test, new_gen, cats. All preprocessed.
    """

    if cat_feats is None:
        cat_feats = ['type_1', 'type_2', 'rarity', 'stage', 'color']
    if num_feats is None:
        num_feats = ['generation', 'height', 'weight']
    # Ideally, I guess these list should be inputs when feat eng.

    # One hot encoding definition
    encoder = OneHotEncoder(sparse_output=False,
                            handle_unknown='ignore')

    dfs = [X_train, X_test, new_gen]
    dfs_out = []

    for i, df in enumerate(dfs):

        if i == 0:
            df_enc = encoder.fit_transform(df[cat_feats])
        else:
            df_enc = encoder.transform(df[cat_feats])

        df_num = df[num_feats]
        cats_out = encoder.get_feature_names_out()
        df_out = pd.concat([pd.DataFrame(df_enc, columns=cats_out, index=df.index), df_num], axis=1)
        dfs_out.append(df_out)

    return tuple(dfs_out) + ([],)

# Testing
# X_tr, X_te, gen_ohe, _ = prep_xgboost_ohe(X_train, X_test, new_gen_initials)
# shape_checker(X_tr, X_te, gen_ohe)


# We now define a preprocessor for catboost with ordinality transformation

def prep_catboost_ordinal(X_train,
                          X_test,
                          new_gen,
                          reg_cat_feats=None,  # In case new categorical features appear
                          new_maps=None):  # To enhance if future feat. eng.
    """
    Preproccessor for catboostregressor. In this case, we create a map for two categories, to transform into simple numbers. 

    Args:
        X_train (DataFrame): 
        X_test (DataFrame): 
        new_gen (DataFrame): 
        reg_cat_feats (list, optional): In case new categories appear in feat. eng.
        new_maps (dict, optional): In case previous new cats require a mapping, this is the place

    Returns:
        X_train, X_test, new_gen, cats. All preprocessed.
    """

    # Original maps
    maps = {'rarity': {'regular': 0,
                       'legendary': 1},
            'stage': {'s1c3': 1,
                      's1c2': 1.05,
                      's2c3': 1.47,
                      'single': 1.8,
                      's2c2': 1.85,
                      's3c3': 2}}

    # Regular cat feats
    cat_feats = ['type_1', 'type_2', 'shape', 'color']

    dfs = [X_train, X_test, new_gen]
    dfs_out = []

    # In case of new maps
    if new_maps is not None:  # Must be a dict of dicts
        maps.update(new_maps)

    if reg_cat_feats is not None:
        cat_feats.extend(reg_cat_feats)

    for col, mapping in maps.items():
        for df in dfs:
            df[col] = df[col].map(mapping).astype('float')

    dfs_out.extend(dfs)

    return tuple(dfs_out) + (cat_feats,)


# Testing
# my_reg_cat = ['type_1', 'type_2', 'shape', 'color']
# X_tr, X_te, gen_cat_ord, _ = prep_catboost_ordinal(X_train, X_test, new_gen_initials,my_reg_cat)
# shape_checker(X_tr, X_te, gen_cat_ord)


# I will define now with catboost with natural, without any strange ordinality

def prep_catboost_native(X_train,
                         X_test,
                         new_gen,
                         new_cat_feats=None):  # To enhance if future feat. eng.
    """
    Another preprocessor function for catboost, but in this case native.

    Args:
        X_train (DataFrame): 
        X_test (DataFrame): 
        new_gen (DataFrame): 
        new_cat_feats (list, optional): If new categories appear after feat. eng. Defaults to None.

    Returns:
        X_train, X_test, new_gen, cats. All preprocessed.
    """

    cat_feats = ['type_1', 'type_2', 'rarity', 'stage', 'shape', 'color']

    if new_cat_feats is not None:
        cat_feats.extend(new_cat_feats) if isinstance(new_cat_feats, list) else [new_cat_feats]

    # Transforming those columns to category
    dfs = [X_train, X_test, new_gen]
    for df in dfs:
        for col in cat_feats:
            df[col] = df[col].astype('category')

    return X_train, X_test, new_gen, cat_feats


# Testing
# X_tr, X_te, gen_cat_nat, _ = prep_catboost_native(X_train, X_test, new_gen_initials)
# shape_checker(X_tr, X_te, gen_cat_nat)


# Finally, time to define same preprocessor but for lightgbm

def prep_lightgbm(X_train,
                  X_test,
                  new_gen,
                  new_cat_feats=None):  # To enhance if future feat. eng.
    """
    Another preprocessor function for LGBM.

    Args:
        X_train (DataFrame): 
        X_test (DataFrame): 
        new_gen (DataFrame): 
        new_cat_feats (list, optional): If new categories appear after feat. eng. Defaults to None.

    Returns:
        X_train, X_test, new_gen, cats. All preprocessed.
    """

    cat_feats = ['type_1', 'type_2', 'rarity', 'stage', 'shape', 'color']

    if new_cat_feats is not None:
        cat_feats.extend(new_cat_feats) if isinstance(new_cat_feats, list) else [new_cat_feats]

    # Transforming those columns to category
    dfs = [X_train, X_test, new_gen]
    for df in dfs:
        for col in cat_feats:
            df[col] = df[col].astype('category')

    return X_train, X_test, new_gen, cat_feats


def shape_checker(x_train, x_test, new_gen_df):
    print("Shapes:", x_train.shape, x_test.shape, new_gen_df.shape)
    print("Columns match:", (x_train.columns == x_test.columns).all())
    print("Indices preserved:", x_train.index.equals(x_train.index))
