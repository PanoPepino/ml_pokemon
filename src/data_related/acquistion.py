"""
Pokémon Feature Engineering Pipeline
Generates complete dataset with stats, sprites, and evolution stages (s1c3 notation)
OUTPUT: ../../datasets/raw/pokemon_database_raw.csv
"""

import requests
import pandas as pd
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# CONFIG - Your original paths and notation preserved
BASE_URL = "https://pokeapi.co/api/v2"
OUTDIR_SPRITES = "../../figures/sprites"
OUTDIR_DATA = "../../datasets/raw"
OUTPUT_CSV = f"{OUTDIR_DATA}/pokemon_database_raw.csv"

Path(OUTDIR_SPRITES).mkdir(exist_ok=True)
Path(OUTDIR_DATA).mkdir(exist_ok=True)


def download_sprite(url: str, poke_id: int, name: str) -> Optional[str]:
    """
    Download sprite with format id_name.png
    """

    try:
        if not url:
            return None
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            filename = f"{poke_id:04d}_{name.replace('-', '.').png}"
            with open(f"{OUTDIR_SPRITES}/{filename}", 'wb') as f:
                f.write(r.content)
            return filename
        return None
    except Exception:
        return None


def get_pokemon_data(identifier: str) -> Optional[Dict[str, Any]]:
    """Fixed version - generation parsing corrected"""
    try:
        poke = requests.get(f"{BASE_URL}/pokemon/{identifier}", timeout=10).json()
        species = requests.get(poke['species']['url'], timeout=10).json()

        # Stats & EVs (unchanged)
        stats = {
            'hp': poke['stats'][0]['base_stat'],
            'atk': poke['stats'][1]['base_stat'],
            'def_': poke['stats'][2]['base_stat'],  # Note: 'def' is keyword
            'sp_atk': poke['stats'][3]['base_stat'],
            'sp_def': poke['stats'][4]['base_stat'],
            'spe': poke['stats'][5]['base_stat']
        }
        total_stats = sum(stats.values())

        evs = {
            'ev_hp': poke['stats'][0]['effort'],
            'ev_atk': poke['stats'][1]['effort'],
            'ev_def': poke['stats'][2]['effort'],
            'ev_sp_atk': poke['stats'][3]['effort'],
            'ev_sp_def': poke['stats'][4]['effort'],
            'ev_spe': poke['stats'][5]['effort']
        }

        types = [t['type']['name'] for t in poke['types']]
        height = poke['height'] / 10
        weight = poke['weight'] / 10

        # FIXED: Egg groups (handle empty)
        egg_groups_raw = species.get('egg_groups', [])
        egg_groups = [eg['name'] for eg in egg_groups_raw] if egg_groups_raw else ['undiscovered']
        egg_groups = ' | '.join(egg_groups)

        # FIXED: Generation parsing - your exact original logic
        generation_dict = species.get('generation', {})
        generation_url = generation_dict.get('url')
        if generation_url:
            # rstrip('/') then split('/')[-1] → '1'
            gen_str = generation_url.rstrip('/').split('/')[-1]
            generation = int(gen_str)
        else:
            generation = None

        # Rest unchanged...
        is_legendary = species.get('is_legendary', False)
        is_mythical = species.get('is_mythical', False)
        is_baby = species.get('is_baby', False)

        category = ('legendary' if is_legendary else
                    'mythical' if is_mythical else
                    'baby' if is_baby else 'regular')

        base_experience = poke.get('base_experience', 0)
        sprite_url = (poke['sprites'].get('other', {})
                      .get('official-artwork', {})
                      .get('front_default') or poke['sprites'].get('front_default'))

        data = {
            'id': poke['id'],
            'name': poke['name'],
            'types': ' | '.join(types),
            'height': height,
            'weight': weight,
            'total_stats': total_stats,
            **stats,  # Unpack individual stats
            **evs,
            'shape': species.get('shape', {}).get('name'),
            'color': species.get('color', {}).get('name'),
            'capture_rate': species.get('capture_rate', 0),
            'gender_rate': species.get('gender_rate', -1),
            'growth_rate': species.get('growth_rate', {}).get('name'),
            'generation': generation,
            'egg_groups': egg_groups,
            'is_legendary': is_legendary,
            'is_mythical': is_mythical,
            'is_baby': is_baby,
            'category': category,
            'base_experience': base_experience,
            'sprite': download_sprite(sprite_url, poke['id'], poke['name'])
        }
        return data
    except Exception as e:
        print(f"Error {identifier}: {e}")
        return None


def get_regional_forms() -> List[str]:
    """
    Verified regional forms ONLY
    """

    alolan = [
        'rattata-alola', 'raticate-alola', 'raichu-alola', 'sandshrew-alola',
        'sandslash-alola', 'vulpix-alola', 'ninetales-alola', 'diglett-alola',
        'dugtrio-alola', 'meowth-alola', 'persian-alola', 'geodude-alola',
        'graveler-alola', 'golem-alola', 'grimer-alola', 'muk-alola',
        'exeggutor-alola', 'marowak-alola'
    ]
    galarian = [
        'meowth-galar', 'ponyta-galar', 'rapidash-galar', 'slowpoke-galar',
        'slowbro-galar', 'slowking-galar', 'farfetchd-galar', 'weezing-galar',
        'mr-mime-galar', 'articuno-galar', 'zapdos-galar', 'moltres-galar',
        'corsola-galar', 'zigzagoon-galar', 'linoone-galar', 'darumaka-galar',
        'darmanitan-galar-zen', 'yamask-galar', 'stunfisk-galar'
    ]
    hisuian = [
        'growlithe-hisui', 'arcanine-hisui', 'voltorb-hisui', 'electrode-hisui',
        'typhlosion-hisui', 'qwilfish-hisui', 'sneasel-hisui', 'samurott-hisui',
        'lilligant-hisui', 'zorua-hisui', 'zoroark-hisui', 'braviary-hisui',
        'sliggoo-hisui', 'goodra-hisui', 'avalugg-hisui', 'decidueye-hisui',
        'dialga-origin', 'palkia-origin'
    ]
    paldean = ['wooper-paldea', 'tauros-paldea-combat-breed']
    return alolan + galarian + hisuian + paldean


def get_chain_length(chain: Dict) -> int:
    """
    Recursively find longest path in evolution chain
    """

    if not chain.get('evolves_to'):
        return 1
    return 1 + max(get_chain_length(e) for e in chain['evolves_to'])


def find_depth(chain: Dict, name: str, depth: int = 1) -> Optional[int]:
    """Find depth where name appears in chain"""
    if chain['species']['name'] == name:
        return depth
    for evolution in chain['evolves_to']:
        result = find_depth(evolution, name, depth + 1)
        if result:
            return result
    return None


def get_stage(name: str) -> str:
    """
    Design sXcN notation: s1c3 or 'single
    '"""
    try:
        name_clean = name.split('-')[0]  # rattata-alola → rattata
        species = requests.get(
            f"https://pokeapi.co/api/v2/pokemon-species/{name_clean}", timeout=10
        ).json()
        chain_url = species['evolution_chain']['url']
        chain = requests.get(chain_url, timeout=10).json()['chain']

        chain_length = get_chain_length(chain)
        if chain_length == 1:
            return 'single'

        depth = find_depth(chain, name_clean)
        if depth is None:
            return 'single'

        return f"s{depth}c{chain_length}"
    except Exception as e:
        print(f"Error fetching {name}: {e}")
        return 'single'


def main():
    """Unified pipeline: scrape → sprites → evolution stages → save"""
    print("=" * 80)
    print("POKÉMON FEATURE ENGINEERING PIPELINE")
    print("=" * 80)

    all_data = []

    # PHASE 1: Base Pokémon 1-1025 (your scrapper logic)
    print("PHASE 1: BASE POKÉMON 1-1025")
    print("-" * 80)
    for i in range(1, 1026):
        data = get_pokemon_data(str(i))
        if data:
            all_data.append(data)
            category_emoji = {
                'legendary': '⭐', 'mythical': '🌟', 'baby': '👶', 'regular': '⚪'
            }.get(data['category'], '')
            print(
                f"{category_emoji} {i:04d} {data['name'][:20]:20s} Gen {data['generation']} EXP:{data['base_experience']:3d} BST:{data['total_stats']:3d} {data['types'][:18]}")
        else:
            print(f"{i:04d} Failed to fetch")
        time.sleep(0.05)

    # PHASE 2: Regional forms (your lists preserved)
    regional = get_regional_forms()
    print("-" * 80)
    print(f"PHASE 2: REGIONAL FORMS ({len(regional)} forms)")
    print("-" * 80)
    for form in regional:
        data = get_pokemon_data(form)
        if data:
            all_data.append(data)
            region = form.split('-')[-1].upper() if '-' in form else ''
            category_emoji = {
                'legendary': '⭐', 'mythical': '🌟', 'baby': '👶', 'regular': '⚪'
            }.get(data['category'], '')
            print(
                f"{category_emoji} {data['id']:04d} {data['name'][:20]:20s} Gen {data['generation']} {region} {data['types'][:18]}")
        else:
            print(f"{form[:20]:20s} Failed to fetch")
        time.sleep(0.1)

    # PHASE 3: Add evolution stages (your evol_chain logic)
    df = pd.DataFrame(all_data)
    print("-" * 80)
    print(f"PHASE 3: ADDING EVOLUTION STAGES ({len(df)} Pokémon)")
    print("-" * 80)
    stages = []
    for i, row in df.iterrows():
        name = row['name']
        stage = get_stage(name)
        stages.append(stage)
        print(f"{i+1:4d}/{len(df)} {name[:20]:20s} → {stage}")
        time.sleep(0.3)  # Rate limit PokeAPI

    df['stage'] = stages
    df.to_csv(OUTPUT_CSV, index=False)

    print("\n✅ Saved to", OUTPUT_CSV)
    print("\nStage distribution:")
    print(df['stage'].value_counts().head(10))
    print(f"\nTotal Pokémon: {len(df)} | Legendary: {df['is_legendary'].sum()}")


if __name__ == "__main__":
    main()
