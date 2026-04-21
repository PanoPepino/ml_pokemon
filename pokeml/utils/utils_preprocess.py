

def shape_checker(df):
    """
    Function to check the shape of the newly preprocessed data and the chosen categories for the model.
    """

    X_test, X_train, y_test, y_train, cats = df

    print("Shapes:", X_test.shape, X_train.shape, y_test.shape, y_train.shape)
    print("Columns match:", (X_train.columns == X_test.columns).all())
    print("Indices preserved:", X_train.index.equals(X_train.index))
    print(f'The chosen categorical features are: {cats}')

# Testing
# my_reg_cat = ['type_1', 'type_2', 'shape', 'color']
# X_tr, X_te, gen_cat_ord, _ = prep_catboost_ordinal(X_train, X_test, new_gen_initials,my_reg_cat)
# shape_checker(X_tr, X_te, gen_cat_ord)


# Testing
# X_tr, X_te, gen_cat_nat, _ = prep_catboost_native(X_train, X_test, new_gen_initials)
# shape_checker(X_tr, X_te, gen_cat_nat)
