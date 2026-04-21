# PoKemon ML Predictor

- This project aims to predict the `BST`, known as `total_stats` (sum of base stats: HP + atk + def + sp.atk + sp.def + spe) for existing and future Pokémon generations using ML.

- The project will train different models and will dive down in feature engineering inspired by zoomorphology, the biology discipline that studies animal shapes. This will provide a further boost to the model predictions. 

- Game Freak, the Pokemon videogame developers, are probably biased by nature when creating pokemons. In that sense, these creatures should follow this underlying bias and their properties, like `BST` are secretly related to this nature imprint.

- For detailed explanations on this project and exploration data analysis, see [PDF_DOCUMENTATION](ml_pokemon_documentation.pdf)



## Predicted values for New Generation Pokemon
<table align="center">
  <tr>
    <td align="center"><img src="plots/browt.png" width="320" height="320" style="border: 3px solid #78C850;  border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></td>
    <td align="center"><img src="plots/pombon.png" width="320" height="320" style="border: 3px solid #F08030; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></td>
    <td align="center"><img src="plots/gecqua.png" width="320" height="320" style="border: 3px solid #2da1ef; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></td>
  </tr>
</table>

<p align="center">
<!-- PREDICTIONS -->

|  Unnamed: 0  |  Browt   |  Pombon  |  Gecqua  |
|:------------:|:--------:|:--------:|:--------:|
|  cat_native  | 297 ± 18 | 311 ± 15 | 306 ± 11 |
| cat_ordinal  | 292 ± 20 | 303 ± 9  | 299 ± 10 |
|  light_gbm   | 277 ± 57 | 309 ± 26 | 295 ± 36 |
<!-- PREDICTIONS -->
</p>


## The metrics leaderboard (best current iteration) for 3 different models

<p align="center">
<!-- LEADERBOARD -->

|    model    |  tr_R2  |  tr_RMSE  |  tr_MAE  |  val_R2  |  val_RMSE  |  val_MAE  |  overfit_R2  |  overfit_RMSE  |  max_res  |
|:-----------:|:-------:|:---------:|:--------:|:--------:|:----------:|:---------:|:------------:|:--------------:|:---------:|
| cat_native  |  0.84   |   45.98   |  32.98   |   0.82   |   46.56    |   34.59   |     0.02     |     -0.58      |  192.71   |
| cat_ordinal |  0.84   |   45.44   |  33.02   |   0.82   |   46.20    |   33.83   |     0.02     |     -0.76      |  199.81   |
|  light_gbm  |  0.86   |   42.54   |  31.83   |   0.82   |   45.71    |   34.71   |     0.04     |     -3.17      |  191.69   |
<!-- LEADERBOARD -->
</p>



