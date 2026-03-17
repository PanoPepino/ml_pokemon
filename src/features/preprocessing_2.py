# Here, I will define 4 different preprocessors to adapt data before model training.
# For convenience, I have also defined a function to check shapes match after preprocessing.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import argparse
import pickle

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
        X_train (my_df): 
        X_test (my_df): 
        new_gen (my_df): 
        new_cat_feats (list, optional): In case new categories appear in feat. eng.
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

    # In case of new maps
    if new_maps is not None:  # Must be a dict of dicts
        maps.update(new_maps)

    if new_cat_feats is not None:
        cat_feats.extend(new_cat_feats)

    new_dataframe = dataframe.copy()

    for col, mapping in maps.items():
        new_dataframe[col] = new_dataframe[col].map(mapping).astype('float')

    return dataframe, cat_feats


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
        X_train (my_df): 
        X_test (my_df): 
        new_gen (my_df): 
        new_cat_feats (list, optional): If new categories appear after feat. eng. Defaults to None.

    Returns:
        X_train, X_test, new_gen, cats. All preprocessed.
    """

    cat_feats = ['type_1', 'type_2', 'rarity', 'stage', 'shape', 'color']

    if new_cat_feats is not None:
        cat_feats.extend(new_cat_feats) if isinstance(new_cat_feats, list) else [new_cat_feats]

    # Transforming those columns to category
    dfs = [X_train.copy(), X_test.copy(), new_gen.copy()]
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
        X_train (my_df): 
        X_test (my_df): 
        new_gen (my_df): 
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
    """
    Function to check the shape of the newly preprocessed data.

    """

    print("Shapes:", x_train.shape, x_test.shape, new_gen_df.shape)
    print("Columns match:", (x_train.columns == x_test.columns).all())
    print("Indices preserved:", x_train.index.equals(x_train.index))


def prepare_data_train(df):
    """
    This function will do 4 main things:

        - 1) Drop values from X, y, encode and impute with :func:`cat_fill_split`
        - 2) Split the train and test values with :func:`train_test_split`
        - 3) Preprocess all your data in 3 different ways with :func:`prep_name_model_mode`
        - 4) Spit out all processed data as dict.

    Args:
        df (my_df): the pokedex to use
        new_poke_info (my_df): An extension of the new poke information.

    Returns:
        data (Dict): All data processed according to preprocessors.
    """

    # 1: Drop BST values, encode and impute and split df for training

    df_to_split = cat_fill(df)
    X, y = df_to_split.drop(columns="total_stats"), df["total_stats"]
    X_tr, X_te, y_tr, y_te = train_test_split(X.copy(), y.copy(), test_size=0.25, random_state=1)

    # 3: Here the dictionariony with all preprocessors. In case you add one more, do not forget to add here.
    prep = {
        "ordinal": prep_catboost_ordinal,
        # "native":  prep_catboost_native,
        # "light_gbm": prep_lightgbm,
    }

    # 4: Data will be output in a dic.
    data = {}
    for name, func in prep.items():  # dict.items will open and unzip keys and values!
        # func act as the value of the dict and map it.
        X_tr_p, X_te_p, cats = func(X_tr.copy(), X_te.copy(), [])
        data[name] = (X_tr_p, X_te_p, y_tr, y_te, cats)  # Spit out the values.

    return data


def main():
    parser = argparse.ArgumentParser(description='Loading data and Preprocess')
    parser.add_argument("--input", required=True, help='Relative path to .csv')
    parser.add_argument("--new-poke-info", default=None, help='Path to .csv with new poke info')
    parser.add_argument("--output", default='prep_data.pkl',
                        help='The already processed data as output, to be called in next func')

    args = parser.parse_args()

    # Loading the data
    df = pd.read_csv(args.input, index_col='id')
    new_poke_info = pd.read_csv(args.new_poke_info)

    # Reorganise the columns for easier reading and dropping names
    tdf = df[['generation', 'type_1', 'type_2', 'rarity', 'stage',
              'shape', 'color', 'height', 'weight', 'total_stats']].copy()

    # Calling the full prepare_data func
    data_ready = prepare_data(tdf, new_poke_info)

    # Saving data
    with open(args.output, 'wb') as f:
        pickle.dump(data_ready, f)
    print('-'*80)
    print(f"1) Preprocessed data located at: {args.output}")
    print(' '*30)
    print("Models are:", list(data_ready.keys()))
    print(' '*30)
    print('Shapes of preprocessed data are:')
    for mode, data in data_ready.items():
        print(f"    - {mode}: train shape {data[0].shape}")
    print('-'*80)


if __name__ == "__main__":
    main()
