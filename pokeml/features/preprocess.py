# Here, I will define 3 different preprocessors to adapt data before model training.
# For convenience, I have also defined a function to check shapes match after preprocessing.

import pandas as pd
from sklearn.model_selection import train_test_split

from pokeml.data.load import load_data


# First, we define a function to accommodate all data (to provide category flag + fill-in missing entries) to objects and also split X, y into train and test


def cat_fill(my_df):
    """
    (OBS there should exist a function before this one to add those NEW FEATURES when engineering)

    This function will do three main things:

    1) Fill in missing values for Type 2.
    2) Check all objects in my_dfs and assign category tag.

    Args:
        df (DataFrame): the dataframe to process.

    Returns:
        df's objects conversed to categorical features and missing values.
    """

    # As the new_pokes my_df will contain names, we need to drop, as this will not be required for the whole training.
    my_df = load_data(my_df)

    new_df = my_df.copy()
    new_df = new_df.drop('name', axis=1, errors='ignore')

    # We need to imput missing types for type_2 and transform some of them to categories in tdf. We also gonna transform objects into categories in tdf.

    new_df['type_2'] = new_df['type_2'].fillna('None')
    new_df[new_df.select_dtypes('object').columns] = new_df.select_dtypes('object').astype('category')

    return new_df

# We now define a preprocessor for catboost with ordinality transformation


def prep_catboost_ordinal(dataframe,
                          new_cat_feats=None,  # In case new categorical features appear
                          new_maps=None):  # To enhance if future feat. eng.
    """
    Preproccessor for catboostregressor. In this case, we create a map for two categories, to transform into simple numbers. 

    Args:
        dataframe (DataFrame): The Dataframe to be massaged. 
        new_cat_feats (list, optional): In case new categories appear in feat. eng.
        new_maps (dict, optional): In case previous new cats require a mapping, this is the place

    Returns:
        new_dataframe, cats. All preprocessed.
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

    # In case of new maps
    if new_maps is not None:  # Must be a dict of dicts
        maps.update(new_maps)

    if new_cat_feats is not None:
        cat_feats.extend(new_cat_feats)

    new_dataframe = dataframe.copy()

    for col, mapping in maps.items():
        new_dataframe[col] = new_dataframe[col].map(mapping).astype('float')

    return new_dataframe, cat_feats


# I will define now with catboost with natural, without any strange ordinality

def prep_catboost_native(dataframe,
                         new_cat_feats=None):  # To enhance if future feat. eng.
    """
    Another preprocessor function for catboost, but in this case native.

    Args:
        dataframe (DataFrame): The Dataframe to be massaged.
        new_cat_feats (list, optional): If new categories appear after feat. eng. Defaults to None.

    Returns:
        new_dataframe, cats. All preprocessed.
    """

    cat_feats = ['type_1', 'type_2', 'rarity', 'stage', 'shape', 'color']

    if new_cat_feats is not None:
        cat_feats.extend(new_cat_feats) if isinstance(new_cat_feats, list) else [new_cat_feats]

    # Transforming those columns to category
    new_dataframe = dataframe.copy()

    for col in cat_feats:
        new_dataframe[col] = new_dataframe[col].astype('category')

    return new_dataframe, cat_feats


# Finally, time to define same preprocessor but for lightgbm

def prep_lightgbm(dataframe,
                  new_cat_feats=None):  # To enhance if future feat. eng.
    """
    Another preprocessor function for LGBM.

    Args:
        dataframe (DataFrame): The Dataframe to be massaged.
        new_cat_feats (list, optional): If new categories appear after feat. eng. Defaults to None.

    Returns:
        new_dataframe, cats. All preprocessed.
    """

    cat_feats = ['type_1', 'type_2', 'rarity', 'stage', 'shape', 'color']

    if new_cat_feats is not None:
        cat_feats.extend(new_cat_feats) if isinstance(new_cat_feats, list) else [new_cat_feats]

    # Transforming those columns to category
    new_dataframe = dataframe.copy()
    for col in cat_feats:
        new_dataframe[col] = new_dataframe[col].astype('category')

    return new_dataframe, cat_feats


def prepare_data_train(df, tsize=0.3):
    """
    This function will do 4 main things:

        - 1) Encode and impute with :func:`cat_fill_split`
        - 2) Preprocess all your data in 3 different ways with :func:`prep_name_model_mode`
        - 3) Split the train and test values with :func:`train_test_split`
        - 4) Spit out all processed data as dict.

    Args:
        df (my_df): the pokedex to use
        tsize (float): In case you want another ratio for the training set.

    Returns:
        data (Dict): All data processed according to preprocessors.
    """

    # 1: Drop BST values, encode and impute and split df for training

    df_to_split = cat_fill(df)

    # 3: Here the dictionariony with all preprocessors. In case you add one more, do not forget to add here.
    prep = {
        "cat_ordinal": prep_catboost_ordinal,
        "cat_native":  prep_catboost_native,
        "light_gbm": prep_lightgbm,
    }

    # 4: Data will be output in a dic.
    data = {}
    for name, func in prep.items():  # dict.items will open and unzip keys and values!
        # func act as the value of the dict and map it.
        prep_data = func(df_to_split)
        cats = prep_data[-1]
        X, y = prep_data[0].drop(columns="total_stats"), prep_data[0]["total_stats"]
        X_tr, X_te, y_tr, y_te = train_test_split(X.copy(), y.copy(), test_size=tsize, random_state=1)
        data[name] = (X_tr, X_te, y_tr, y_te, cats)  # Spit out the values.

    return data


def prepare_data_predict(predict_df):
    """
    This function will do 4 main things:

        - 1) Encode and impute with :func:`cat_fill_split`
        - 2) Preprocess all your data in 3 different ways with :func:`prep_name_model_mode`
        - 3) Split the train and test values with :func:`train_test_split`
        - 4) Spit out all processed data as dict.

    Args:
        df (my_df): the pokedex to use
        tsize (float): In case you want another ratio for the training set.

    Returns:
        data (Dict): All data processed according to preprocessors.
    """

    # 1: Drop BST values, encode and impute and split df for training

    df_to_split = cat_fill(predict_df)
    just_names = load_data(predict_df)
    poke_names = just_names['name']

    # 3: Here the dictionariony with all preprocessors. In case you add one more, do not forget to add here.
    prep = {
        "cat_ordinal": prep_catboost_ordinal,
        "cat_native":  prep_catboost_native,
        "light_gbm": prep_lightgbm,
    }

    # 4: Data will be output in a dic.
    data = {}
    for name, func in prep.items():  # dict.items will open and unzip keys and values!
        # func act as the value of the dict and map it.
        prep_data = func(df_to_split)
        cats = prep_data[-1]
        X_pred = prep_data[0]
        X_pred['name'] = poke_names
        data[name] = (X_pred, cats)  # Spit out the values.

    return data
