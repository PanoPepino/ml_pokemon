# PoKemon ML Predictor

This project aims to predict the `BST`, known as `total_stats` (sum of base stats: HP + atk + def + sp.atk + sp.def + spe) for existing and future Pokémon generations using ML.

## Model Leaderboard

Best models ranked by R² on test set (Base Stats Total prediction).

| Rank | Model   | R²    | Browt | Pombonon | Gecqua |
|------|---------|-------|-------------|----------------|--------------|
| 1    | LGBM    | 0.856 | 255 ± 103    | 304 ± 70       | 283 ± 92     |
| 2    | Ordinal | 0.861 | 269 ± 2    | 295 ± 2       | 291 ± 1     |
| 3    | Native  | 0.860 | 276 ± 1    | 303 ± 2        | 296 ± 5     |

*Updated: Mar 11, 2026*  
*Target: R² ≥ 0.9, Uncertainty ~ 10*

