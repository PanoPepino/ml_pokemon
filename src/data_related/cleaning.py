import pandas as pd


IN_DIR = '../../datasets/raw/pokemon_database_raw.csv'
OUT_DIR = '../../datasets/processed/pkdx_clean.csv'


# Loading the raw document to be modified
df = pd.read_csv(IN_DIR)


# As for the moment, I will not use these features
cleaning_df = df.drop(['is_mythical', 'is_baby', 'is_legendary', 'gender_rate', 'sprite'], axis=1)


# Replacing any "-" with underbar "_"
cleaning_df['name'] = cleaning_df['name'].str.replace("-", "_")


# Replacing any "origin" with hisui (Dialga and Palkia from Hisui)
cleaning_df['name'] = cleaning_df['name'].str.replace("origin", "hisui")

# Rearranging generations, so that each pokemon really corresponds to the iteration when it was created.


def update_generation(df, search_column, target_column):
    """
    Update target_column where search_column contains word. When a given string (in words) is detected,
    the generation in gens get updated.
    """

    words = ['alola', 'galar', 'hisui', 'paldea']
    gens = ['7', '8', '9', '9']
    for word, gen in zip(words, gens):
        mask = df[search_column].str.contains(word, case=False, na=False)
        df.loc[mask, target_column] = int(gen)
    return df


# Throwing the function to clean those pesky generations
cleaning_df = update_generation(cleaning_df, 'name', 'generation')

# Rename Paldean Tauros
cleaning_df.loc[(cleaning_df['name'].isin(['tauros_paldea_combat_breed'])) &
                (cleaning_df['generation'] == 9), 'name'] = 'tauros_paldea'


# Identifying annoying pokemon with "_" in the name that does not correspond to any given region.
no_underscored_df = cleaning_df[(cleaning_df['name'].str.count('_') >= 1) & (
    ~cleaning_df['name'].str.contains('alola|hisui|paldea|galar', case=False, na=False))]


# Printing all names that does not contain a _region, but contain still a _ character. Uncomment to see.
for i in range(1, 10):
    filter_annoying = no_underscored_df[(no_underscored_df['name'].str.count('_') >= 1)
                                        & (no_underscored_df['generation'] == i)]
    fa = filter_annoying[['name', 'generation']]

    # View the no_underscored dataframe
    # print(fa.head(30))

# List of exceptions to not be killed
exceptions = ['nidoran_f',
              'nidoran_m',
              'mr_mime',
              'ho_oh',
              'mime_jr',
              'porygon_z',
              'type_null',
              'jangmo_o',
              'hakamo_o',
              'kommo_o',
              'tapu_koko',
              'tapu_lele',
              'tapu_bulu',
              'tapu_fini',
              'mr_rime',
              'great_tusk',
              'scream_tail',
              'brute_bonnet',
              'flutter_mane',
              'slither_wing',
              'sandy_shocks',
              'iron_treads',
              'iron_bundle',
              'iron_hands',
              'iron_jugulis',
              'iron_moth',
              'iron_thorns',
              'wo_chien',
              'chien_pao',
              'ting_lu',
              'chi_yu',
              'roaring_moon',
              'iron_valiant',
              'walking_wake',
              'iron_leaves',
              'gouging_fire',
              'raging_bolt',
              'iron_boulder',
              'iron_crown',
              '_alola',
              '_galar',
              '_hisui',
              '_paldea',
              'tauros_paldea'
              ]


regional_forms = ['_alola', '_galar', '_hisui', '_paldea']


# Paradox Pokémon list (with underscores after name replacement)
paradox = ['great_tusk',
           'scream_tail',
           'brute_bonnet',
           'flutter_mane',
           'slither_wing',
           'sandy_shocks',
           'iron_treads',
           'iron_bundle',
           'iron_hands',
           'iron_jugulis',
           'iron_moth',
           'iron_thorns',
           'roaring_moon',
           'iron_valiant',
           'walking_wake',
           'iron_leaves',
           'gouging_fire',
           'raging_bolt',
           'iron_boulder',
           'iron_crown']


# paradox and beast of gen 9that are legendary:
paradox_legend = ['walking_wake', 'gouging_fire', 'raging_bolt', 'iron_leaves', 'iron_crown', 'iron_boulder']
beast_gen_9 = ['wo_chien', 'chien_pao', 'ting_lu', 'chi_yu']

# Correcting some issue with stages in all paradox forms and rearranging all legendary and mythical under same umbrella and Tauros paldea_name


def change_stage(database, paradox_list):
    # Set all paradox Pokémon to 'single'
    database.loc[database['name'].isin(paradox_list), 'stage'] = 'single'
    database.loc[database['name'].isin(paradox_legend), 'category'] = 'legendary'
    # Meltan and Melmetal evolution chain is wrong
    database.loc[database['name'].isin(['meltan']), 'stage'] = 's1c2'
    database.loc[database['name'].isin(['melmetal']), 'stage'] = 's2c2'
    database.loc[database['name'].isin(beast_gen_9), 'stage'] = 'single'

    # 4 Chinese beasts in Gen 9 have no stage

    # Rearrange mythical under legendary category
    database.loc[database['stage'].isin(['mythical']), 'category'] = 'legendary'

    return database


cleaning_df = change_stage(cleaning_df, paradox)


# Removing annoying underscores
cleaning_df['name'] = cleaning_df['name'].apply(
    lambda x: x if (x in exceptions or '_' not in x or any(x.endswith(region) for region in regional_forms)) else x.split('_')[0])


# After cleaning names and some annoying features I will not use, let me split types and egg groups.
# Split types into type_1 and type_2
cleaning_df[['type_1', 'type_2']] = cleaning_df['types'].str.split('/', n=1, expand=True)


# Split egg_groups into egg_group_1, egg_group_2
cleaning_df[['egg_group_1', 'egg_group_2']
            ] = cleaning_df['egg_groups'].str.split('/', n=1, expand=True)


# Dropping old types and egg_groups columns
split_df = cleaning_df.drop(columns=['types', 'egg_groups'])


# Let me rearrange the columns to more practical ones
first_imp = ['id', 'generation', 'name', 'type_1', 'type_2', 'height', 'weight', 'color', 'shape', 'category', 'stage']
stats = ['total_stats', 'hp', 'atk', 'def', 'sp_atk', 'sp_def', 'spe']
evs = ['ev_hp', 'ev_atk', 'ev_def', 'ev_sp_atk', 'ev_sp_def', 'ev_spe']
second_imp = ['capture_rate', 'growth_rate', 'base_experience', 'egg_group_1', 'egg_group_2']
new_df = split_df[first_imp + stats + evs + second_imp]


def change_id(df, base_max=1025):
    """
    For rows with id > base_max, reassign ids to a new continuous range
    starting at base_max + 1, preserving order.
    """
    # Mask for rows to change
    mask = df['id'] > base_max

    # Get the unique ids to remap, in order of appearance
    unique_bad_ids = df.loc[mask, 'id'].unique()

    # Build a mapping: old_id -> new_id
    new_start = base_max + 1
    mapping = {
        old: new_start + i
        for i, old in enumerate(unique_bad_ids)
    }

    # Apply mapping only where id > base_max
    df.loc[mask, 'id'] = df.loc[mask, 'id'].map(mapping)

    return df


new_id = change_id(new_df, base_max=1025)
no_myth_old = new_id.replace('mythical', 'legendary')
no_myth = no_myth_old.replace('baby', 'regular')
no_myth.rename(columns={'category': 'rarity'}, inplace=True)  # To avoid confusion when ML features
print("=" * 70)
print(f"Names, numbers and structure of the data base has been rearranged!")
print("=" * 70)
print("The new structure is:")
print("-"*70)
print(no_myth.columns)
print("="*70)
no_myth.to_csv(OUT_DIR, index=False)


# Let me design a quick script to create .csv documents with selected columns, for easier manipulation


NEW_IN_DIR = '../../datasets/processed/pkdx_clean.csv'
NEW_OUT_DIR = '../../datasets/processed/pkdx_min.csv'
my_features = ['generation', 'name', 'type_1', 'type_2', 'rarity',
               'stage', 'shape', 'color', 'total_stats', 'height', 'weight']


def pkdx_trimmer(in_dir, out_dir, features):
    df = pd.read_csv(in_dir, index_col='id')
    trimmed_pkdx = df[features]
    return trimmed_pkdx.to_csv(out_dir)

# Let me call it here, for simplicity to generate the data to be used in this first stage of the project.


pkdx_trimmer(NEW_IN_DIR, NEW_OUT_DIR, my_features)
