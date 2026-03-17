# PoKemon ML Predictor

- This project aims to predict the `BST`, known as `total_stats` (sum of base stats: HP + atk + def + sp.atk + sp.def + spe) for existing and future Pokémon generations using ML.

- The project will train different models and will dive down in feature engineering inspired by zoomorphology, the biology discipline that studies animal shapes. This will provide a further boost to the model predictions. 

- Game Freak, the Pokemon videogame developers, are probably biased by nature when creating pokemons. In that sense, these creatures should follow this underlying bias and their properties, like `BST` are secretly related to this nature imprint.

- For detailed explanations on this project and exploration data analysis, see [PDF_DOCUMENTATION](ml_pokemon_documentation.pdf)



## Predicted values for New Generation Pokemon

<!-- Leaderboard Section -->
<table align="center" style="table-layout: fixed; width: 100%; max-width: 1000px;">
<tr>
  <td align="center">
    <img src="./figures/stats_ld.png" 
         style="border: 3px solid #0c2eb6; border-radius: 5px; height: 200px; max-width: 100%; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <br><strong>BST Predictions for different models</strong>
  </td>
</tr>
</table>

<table align="center">
  <tr>
    <td align="center"><img src="figures/browt.png" width="320" height="320" style="border: 3px solid #78C850;  border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></td>
    <td align="center"><img src="figures/pombon.png" width="320" height="320" style="border: 3px solid #F08030; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></td>
    <td align="center"><img src="figures/gecqua.png" width="320" height="320" style="border: 3px solid #2da1ef; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"></td>
  </tr>
  <tr>
    <td align="center"><strong>Best BST so far<br>272±2</strong></td>
    <td align="center"><strong>Best BST so far<br>306±9</strong></td>
    <td align="center"><strong>Best BST so far<br>297±5</strong></td>
  </tr>
</table>

## The metrics leaderboard for 3 different models. Currently, no training at all.
<!-- Leaderboard Section -->
<table align="center" style="table-layout: fixed; width: 100%; max-width: 1000px;">
<tr>
  <td align="center">
    <img src="./figures/metrics_ld.png" 
         style="border: 3px solid #890613; border-radius: 5px; height: 200px; max-width: 100%; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <br><strong>R2 Leaderboard for different models</strong>
  </td>
</tr>
</table>

>
