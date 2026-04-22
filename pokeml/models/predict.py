import joblib
import pandas as pd

from pathlib import Path
from pokeml.utils.utils_train import get_model


def predict_stats(
        input_model: str,
        new_poke_data: dict,
        to_save: bool = True,
        output_preds: str = None,
) -> pd.DataFrame:
    """
    Load one or more saved model, predict on prepared new Pokémon data, and save CSV.
    """

    model = joblib.load(Path(str(f"{input_model}.joblib")))

    the_model = get_model(input_model)

    df_pred = new_poke_data[the_model][0].copy()
    if "name" not in df_pred.columns:
        raise KeyError(f"'name' column not found in prediction dataframe for {the_model}")

    poke_names = df_pred["name"]
    X_pred = df_pred.drop("name", axis=1)

    vals, uncs = model.predict_unc(X_pred)

    result = pd.DataFrame(
        {
            "name": poke_names,
            "pred_bst": [round(v) for v in vals],
            "uncertainty": [round(u) for u in uncs],
            "pred_bst_text": [f"{round(v)} ± {round(u)}" for v, u in zip(vals, uncs)],
            "model": the_model,
        }
    )

    # Output csv name

    if to_save:
        out_dir = Path(f"artifacts/predictions/")
        out_dir.mkdir(parents=True, exist_ok=True)
        result.to_csv(f"{out_dir}/{output_preds}.csv", index=False)

    return result


def predict_all_models(
    run: str,
    new_poke_data: dict,
    output_preds: str,
) -> pd.DataFrame:
    """
    Predict with all selected models and save one CSV where:
    - columns = pokemon names
    - rows = model predictions as 'value ± uncertainty'
    """
    model_suffixes = ["cat_native", "cat_ordinal", "light_gbm"]
    input_models = [f"{run}_{model}" for model in model_suffixes]

    all_rows = []

    for model_name in input_models:
        df_model = predict_stats(
            input_model=model_name,
            new_poke_data=new_poke_data,
            to_save=False
        )

        current_model = df_model["model"].iloc[0]

        temp = df_model.set_index("name")[["pred_bst_text"]].T
        temp.index = [f"{current_model}"]

        all_rows.append(temp)

    df_out = pd.concat(all_rows, axis=0)

    p = Path(output_preds)
    parent = str(p.parent)
    last = p.name

    out_dir = Path(parent)
    out_dir.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(out_dir / f"{last}")

    return df_out
