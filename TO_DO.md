# Pokémon ML Dataset - Complete Guide
**File**: `pokemon_biological_fixed.csv`  
**Rows**: 1085 Pokémon (Generations 1-9)  
**Purpose**: Predict Gen 10 Pokémon stats and types using Machine Learning


---

# TO DO:

- [X] Clean pokemon names as `morpeko_full_belly` or `mimikyu_disguised`. Both in Data base and images.
- [X] Change generation of regional forms to the real generation they belong to (7, 8, 9).
- [X] Drop `is_legendary`, `is_mythical` and leave simply `category`.
- [X] Drop `habitat`.
- [X] Split `typing` into 2 columns.
- [X] Split `egg_group` into 2 columns.
- [X] Fix issue with data_cleaning.py
- [X] Merge `legendary` and `mythical`. 
- [X] Think how to rephrase `regular` and `baby` based on `base_exp ` (so that one creates something like initial_stage, medium, final)
- [X] Chage number and names in list and also in sprites so that it counts up to 1081.
- [X] Identify bst average evolution accross generations (power creep)
- [X] Identify probable fitting for F3
- [X] Double check linear fit for Singles??
- [X] Find average distribution on each stage by type (correlations?)
- [X] Focus on deviation for each type for each stage.
- [X] Rewrite plot functions to package.
- [X] Plot overall stats distributions over generations (first plot to add in README)
- [X] Understand better previous findings
- [X] Fix a simple XGBoost model with encoding to get BST values
- [X] Design pipeline to implement all 4 models at same time
- [X] Move those preprocessor functions to src after checking everything works.
- [X] Add nice pictures for 3 initials and expected BST.
- [X] Create function to explore GridSearch, extract best parameters and feed in get_leaderboard

- [ ] Create .py file to easily execute everything.
- [ ] Drop all info into .pdf from old_readme
- [ ] Add documentation.pdf to download.
- [ ] Enhance Readme + link Documentation to it.
- [ ] Create gitignore for all sprites and unneccesary .tex files.


---
- [ ] Fix extract importance in leaderboard for each feat. (understand it)
- [ ] Explore correlation matrix. (Evaluate if it is the same thing as importance)
- [ ] Think better on renormalisation of s3c3 and single to s2c2. Increase sample, but bias? (see notes)
- [ ] Find relation between pokemon shape and stats?? 
- [ ] What about shape and type??
- [ ] Determine biological zoomorphology to compute density.
- [ ] Recall the normalised density to avoide big spikes.
- [ ] Think of other biological features to be added to the model.







