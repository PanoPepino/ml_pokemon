"""
Pokémon Scrapper for Pkdx Acquisition
Generates complete dataset with stats, and evolution stages (s1c3 notation)
"""

import time
import pandas as pd
import requests

from pathlib import Path
from typing import Dict, Any, Optional, List
from pathlib import Path
from typing import Callable
from pokeml.utils.utils_commands import PkdxUI
from rich.console import Console

console = Console()
ui = PkdxUI()


BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon_data(identifier: str) -> Optional[Dict[str, Any]]:
    try:
        poke = requests.get(f"{BASE_URL}/pokemon/{identifier}", timeout=10).json()
        species = requests.get(poke["species"]["url"], timeout=10).json()

        stats = {
            "hp": poke["stats"][0]["base_stat"],
            "atk": poke["stats"][1]["base_stat"],
            "def_": poke["stats"][2]["base_stat"],
            "sp_atk": poke["stats"][3]["base_stat"],
            "sp_def": poke["stats"][4]["base_stat"],
            "spe": poke["stats"][5]["base_stat"],
        }
        total_stats = sum(stats.values())

        evs = {
            "ev_hp": poke["stats"][0]["effort"],
            "ev_atk": poke["stats"][1]["effort"],
            "ev_def": poke["stats"][2]["effort"],
            "ev_sp_atk": poke["stats"][3]["effort"],
            "ev_sp_def": poke["stats"][4]["effort"],
            "ev_spe": poke["stats"][5]["effort"],
        }

        types = [t["type"]["name"] for t in poke["types"]]
        height = poke["height"] / 10
        weight = poke["weight"] / 10

        egg_groups_raw = species.get("egg_groups", [])
        egg_groups = [eg["name"] for eg in egg_groups_raw] if egg_groups_raw else ["undiscovered"]
        egg_groups = " | ".join(egg_groups)

        generation_dict = species.get("generation", {})
        generation_url = generation_dict.get("url")
        if generation_url:
            gen_str = generation_url.rstrip("/").split("/")[-1]
            generation = int(gen_str)
        else:
            generation = None

        is_legendary = species.get("is_legendary", False)
        is_mythical = species.get("is_mythical", False)
        is_baby = species.get("is_baby", False)

        category = (
            "legendary" if is_legendary else
            "mythical" if is_mythical else
            "baby" if is_baby else
            "regular"
        )

        base_experience = poke.get("base_experience", 0)

        return {
            "id": poke["id"],
            "name": poke["name"],
            "types": " | ".join(types),
            "height": height,
            "weight": weight,
            "total_stats": total_stats,
            **stats,
            **evs,
            "shape": species.get("shape", {}).get("name"),
            "color": species.get("color", {}).get("name"),
            "capture_rate": species.get("capture_rate", 0),
            "gender_rate": species.get("gender_rate", -1),
            "growth_rate": species.get("growth_rate", {}).get("name"),
            "generation": generation,
            "egg_groups": egg_groups,
            "is_legendary": is_legendary,
            "is_mythical": is_mythical,
            "is_baby": is_baby,
            "category": category,
            "base_experience": base_experience,
        }
    except Exception:
        return None


def get_regional_forms() -> List[str]:
    alolan = [
        "rattata-alola", "raticate-alola", "raichu-alola", "sandshrew-alola",
        "sandslash-alola", "vulpix-alola", "ninetales-alola", "diglett-alola",
        "dugtrio-alola", "meowth-alola", "persian-alola", "geodude-alola",
        "graveler-alola", "golem-alola", "grimer-alola", "muk-alola",
        "exeggutor-alola", "marowak-alola",
    ]
    galarian = [
        "meowth-galar", "ponyta-galar", "rapidash-galar", "slowpoke-galar",
        "slowbro-galar", "slowking-galar", "farfetchd-galar", "weezing-galar",
        "mr-mime-galar", "articuno-galar", "zapdos-galar", "moltres-galar",
        "corsola-galar", "zigzagoon-galar", "linoone-galar", "darumaka-galar",
        "darmanitan-galar-zen", "yamask-galar", "stunfisk-galar",
    ]
    hisuian = [
        "growlithe-hisui", "arcanine-hisui", "voltorb-hisui", "electrode-hisui",
        "typhlosion-hisui", "qwilfish-hisui", "sneasel-hisui", "samurott-hisui",
        "lilligant-hisui", "zorua-hisui", "zoroark-hisui", "braviary-hisui",
        "sliggoo-hisui", "goodra-hisui", "avalugg-hisui", "decidueye-hisui",
        "dialga-origin", "palkia-origin",
    ]
    paldean = ["wooper-paldea", "tauros-paldea-combat-breed"]
    return alolan + galarian + hisuian + paldean


def get_chain_length(chain: Dict) -> int:
    if not chain.get("evolves_to"):
        return 1
    return 1 + max(get_chain_length(e) for e in chain["evolves_to"])


def find_depth(chain: Dict, name: str, depth: int = 1) -> Optional[int]:
    if chain["species"]["name"] == name:
        return depth
    for evolution in chain["evolves_to"]:
        result = find_depth(evolution, name, depth + 1)
        if result:
            return result
    return None


def get_stage(name: str) -> str:
    try:
        name_clean = name.split("-")[0]
        species = requests.get(
            f"{BASE_URL}/pokemon-species/{name_clean}",
            timeout=10,
        ).json()
        chain_url = species["evolution_chain"]["url"]
        chain = requests.get(chain_url, timeout=10).json()["chain"]

        chain_length = get_chain_length(chain)
        if chain_length == 1:
            return "single"

        depth = find_depth(chain, name_clean)
        if depth is None:
            return "single"

        return f"s{depth}c{chain_length}"
    except Exception:
        return "single"


def acquire_full_pkdx(
    my_path: Path | str,
    printer: Callable[[str], None] = console.print,
) -> pd.DataFrame:
    my_path = Path(my_path)
    my_path.parent.mkdir(parents=True, exist_ok=True)

    ui.header("Pkdx Acquisition")
    console.print('')
    ui.info("Generates complete dataset with stats and evolution stages")

    all_data = []
    console.print('')
    ui.phase("PHASE 1 — BASE POKÉMON")
    console.print('')
    for i in range(1, 1026):
        data = get_pokemon_data(str(i))
        if data:
            all_data.append(data)
            category_emoji = {
                "legendary": "⭐",
                "mythical": "🌟",
                "baby": "👶",
                "regular": "⚪",
            }.get(data["category"], "")
            printer(
                f"{category_emoji} {i:04d} "
                f"{data['name'][:20]:20s} "
                f"Gen {data['generation']} "
                f"BST:{data['total_stats']:3d} "
                f"{data['types'][:18]}"
            )
        else:
            ui.warning(f"{i:04d} Failed to fetch")
        time.sleep(0.05)

    regional = get_regional_forms()
    console.print('')
    ui.phase(f"PHASE 2 — REGIONAL FORMS ({len(regional)} forms)")
    console.print('')
    with console.status("[bold green]Fetching regional forms...[/bold green]"):
        for form in regional:
            data = get_pokemon_data(form)
            if data:
                all_data.append(data)
                region = form.split("-")[-1].upper() if "-" in form else ""
                category_emoji = {
                    "legendary": "⭐",
                    "mythical": "🌟",
                    "baby": "👶",
                    "regular": "⚪",
                }.get(data["category"], "")
                printer(
                    f"{category_emoji} {data['id']:04d} "
                    f"{data['name'][:20]:20s} "
                    f"Gen {data['generation']} "
                    f"{region} "
                    f"{data['types'][:18]}"
                )
            else:
                ui.warning(f"{form[:20]:20s} Failed to fetch")
            time.sleep(0.1)

    df = pd.DataFrame(all_data)

    console.print('')
    ui.phase(f"PHASE 3 — ADDING EVOLUTION STAGES ({len(df)} Pokémon)")
    console.print('')
    stages = []
    with console.status("[bold green]Computing evolution stages...[/bold green]"):
        for i, row in df.iterrows():
            name = row["name"]
            stage = get_stage(name)
            stages.append(stage)
            printer(f"{i + 1:4d}/{len(df)} {name[:20]:20s} -> {stage}")
            time.sleep(0.3)

    df["stage"] = stages
    df.to_csv(my_path, index=False)

    ui.success(f"Pokédex saved to {my_path}")
    ui.summary(
        "Dataset Summary",
        f"Stage distribution:\n{df['stage'].value_counts().head(10).to_string()}\n\n"
        f"Total Pokémon: {len(df)} | Legendary: {df['is_legendary'].sum()}",
    )

    return df
