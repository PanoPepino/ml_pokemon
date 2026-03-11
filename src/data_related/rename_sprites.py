# GPT generated. Human modification.

import re
import os
MY_DIR = "../../figures/sprites"


def rename_pokemon_png_files(directory_path, exceptions, regional_forms):
    """
    Renames .png files in the given directory from 'number_pkmnname_something.png' 
    to 'pkmnname.png', preserving exceptions and regional forms.

    exceptions: list of names to keep as-is (e.g., 'nidoran_f').
    regional_forms: list of suffixes to preserve (e.g., '_paldea').
    """

    # Compile regex for matching files: optional number_, pokemon name, optional _something.png
    pattern = re.compile(r'^(\d+_)?([a-zA-Z0-9_]+)(?:_.*)?\.png$')

    renamed_count = 0
    for filename in os.listdir(directory_path):
        if not filename.lower().endswith('.png'):
            continue

        match = pattern.match(filename)
        if not match:
            print(f"Skipping non-matching file: {filename}")
            continue

        # Extract base name (group 2)
        base_name = match.group(2).lower()

        # Check if should keep as-is
        if (base_name in exceptions or
            '_' not in base_name or
                any(base_name.endswith(region) for region in regional_forms)):
            new_filename = base_name + '.png'
        else:
            # Split on first _, take pokemon name
            new_base = base_name.split('_', 1)[0]
            new_filename = new_base + '.png'

        old_path = os.path.join(directory_path, filename)
        new_path = os.path.join(directory_path, new_filename)

        if old_path != new_path:
            if os.path.exists(new_path):
                print(f"Skipping {filename} -> {new_filename} (already exists)")
            else:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
        else:
            print(f"No change needed: {filename}")

    print(f"\nTotal files renamed: {renamed_count}")


# Usage example (replace '/path/to/your/png/folder' with actual directory)
exceptions = ['nidoran_f', 'nidoran_m', 'mr_mime', 'ho_oh', 'mime_jr', 'porygon_z', 'type_null',
              'jangmo_o', 'hakamo_o', 'kommo_o', 'tapu_koko', 'tapu_lele', 'tapu_bulu', 'tapu_fini',
              'mr_rime', 'great_tusk', 'scream_tail', 'brute_bonnet', 'flutter_mane', 'slither_wing',
              'sandy_shocks', 'iron_treads', 'iron_bundle', 'iron_hands', 'iron_jugulis', 'iron_moth',
              'iron_thorns', 'wo_chien', 'chien_pao', 'ting_lu', 'chi_yu', 'roaring_moon', 'iron_valiant',
              'walking_wake', 'iron_leaves', 'gouging_fire', 'raging_bolt', 'iron_boulder', 'iron_crown',
              '_alola', '_galar', '_hisui', '_paldea']

regional_forms = ['_alola', '_galar', '_hisui', '_paldea']  # Paldea added.


rename_pokemon_png_files(MY_DIR, exceptions, regional_forms)
