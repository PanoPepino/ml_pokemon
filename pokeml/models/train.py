
import json
import joblib
import matplotlib.pyplot as plt

from pathlib import Path
from pokeml.models.trainers import Cat_Trainer, LGBM_Trainer
from pokeml.visualisation.loss_plt import plot_loss


def train(prep_data,
          params: dict,
          output_name):
    """
    Train models and save one combined figure with 3 loss-curve subplots
    (one subplot per model).
    """

    trained_models = {}
    evals = []  # For plots
    summary = []  # Recommended summary
    results = []  # Similarly as tuning, display more info

    # Defining path for out
    p = Path(output_name)
    out_dir = p.parent
    last = p.name

    out_dir.mkdir(parents=True, exist_ok=True)

    plot_dir = Path("plots/training")
    plot_dir.mkdir(parents=True, exist_ok=True)

    for name, (X_tr_p, X_te_p, y_tr, y_te, cats) in prep_data.items():
        if name in ("cat_ordinal", "cat_native"):
            trainer = Cat_Trainer(cat_features=cats, **params[name])
        else:
            trainer = LGBM_Trainer(**params["light_gbm"])

        eval_full = [(X_tr_p, y_tr), (X_te_p, y_te)]
        pipeline = trainer.fit(X_tr_p, y_tr, eval_set=eval_full)
        trained_models[name] = pipeline

        # Saving each model in joblib + information in summary
        model_path = out_dir / f"{last}_{name}.joblib"
        joblib.dump(pipeline, model_path, compress=3)

        summary.append({
            "model_name": name,
            "model_path": str(model_path),
            "n_train_rows": len(X_tr_p),
            "n_test_rows": len(X_te_p)
        })

        # Saving evaluations for easier plotting of train/validation curves
        test_evals = trainer.get_evals()
        evals.append({
            "model_name": f"{last}_{name}",
            "evals": test_evals
        })

    # One single figure with 3 subplots, one for each model
    n_models = len(evals)
    fig, axs = plt.subplots(1, n_models, figsize=(7 * n_models, 6), squeeze=False)
    axs = axs.ravel()

    for ax, item in zip(axs, evals):
        plot_loss(
            name_model=item["model_name"],
            evals=item["evals"],
            ax=ax
        )

    fig.suptitle(f"Training / Validation for {last} Run", fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(plot_dir / f"{last}_all_models_loss.png", dpi=500, bbox_inches="tight")
    plt.close(fig)

    summary_path = out_dir / f"{last}_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    return trained_models
