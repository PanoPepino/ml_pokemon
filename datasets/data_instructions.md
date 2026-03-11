# Pokémon Dataset Features - Quick Reference

**Total**: 1,083 Pokémon (1,025 base + 58 regional forms)  
**Features**: 25 columns



## Identifier Columns

| Column | Type | Range / Values | Description |
|--------|------|----------------|-------------|
| `id` | Integer | 1 – 1082 | National Pokédex number (Regional forms after 1025) |
| `name` | String | e.g. `bulbasaur`, `charizard` | Pokémon name in lowercase; regional forms use hyphen (e.g. `rattata_alola`) |
| `generation` | Integer | 1 – 9 | Generation in which the Pokémon was introduced |

---

| Column | Type | Range / Values | Description |
|--------|------|----------------|-------------|
| `type_1` | String | ![normal](https://img.shields.io/badge/normal-A8A878?style=flat) ![fire](https://img.shields.io/badge/fire-F08030?style=flat&logoColor=white) ![water](https://img.shields.io/badge/water-6890F0?style=flat&logoColor=white) ![electric](https://img.shields.io/badge/electric-F8D030?style=flat) ![grass](https://img.shields.io/badge/grass-78C850?style=flat)<br>![ice](https://img.shields.io/badge/ice-98D8D8?style=flat) ![fighting](https://img.shields.io/badge/fighting-C03028?style=flat&logoColor=white) ![poison](https://img.shields.io/badge/poison-A040A0?style=flat&logoColor=white) ![ground](https://img.shields.io/badge/ground-E0C068?style=flat) ![flying](https://img.shields.io/badge/flying-A890F0?style=flat)<br>![psychic](https://img.shields.io/badge/psychic-F85888?style=flat&logoColor=white) ![bug](https://img.shields.io/badge/bug-A8B820?style=flat) ![rock](https://img.shields.io/badge/rock-B8A038?style=flat&logoColor=white) ![ghost](https://img.shields.io/badge/ghost-705898?style=flat&logoColor=white) ![dragon](https://img.shields.io/badge/dragon-7038F8?style=flat&logoColor=white)<br>![dark](https://img.shields.io/badge/dark-705848?style=flat&logoColor=white) ![steel](https://img.shields.io/badge/steel-B8B8D0?style=flat) ![fairy](https://img.shields.io/badge/fairy-EE99AC?style=flat) | Primary type |
| `type_2` | String | Same as `type_1`, or empty | Secondary type; empty if mono-typed |
| `height` | Float | 0.1 – 32.0 (metres) | Official height in metres |
| `weight` | Float | 0.1 – 999.9 (kg) | Official weight in kilograms |
| `color` | String | ![red](https://img.shields.io/badge/red-E8231A?style=flat&logoColor=white) ![blue](https://img.shields.io/badge/blue-4A90D9?style=flat&logoColor=white) ![yellow](https://img.shields.io/badge/yellow-F5D000?style=flat) ![green](https://img.shields.io/badge/green-3DAC3A?style=flat&logoColor=white) ![black](https://img.shields.io/badge/black-222222?style=flat&logoColor=white)<br>![brown](https://img.shields.io/badge/brown-8B5E3C?style=flat&logoColor=white) ![purple](https://img.shields.io/badge/purple-8B4FA6?style=flat&logoColor=white) ![gray](https://img.shields.io/badge/gray-9E9E9E?style=flat&logoColor=white) ![white](https://img.shields.io/badge/white-F0F0F0?style=flat) ![pink](https://img.shields.io/badge/pink-F4A7C0?style=flat) | Official Pokédex colour classification |
| `shape` | String | `quadruped` `upright` `wings` `armor` `blob`<br>`humanoid` `squiggle` `fish` `ball` `bug-wings`<br>`legs` `heads` `arms` `tentacles` | Official body shape from PokeAPI |


## Classification Columns

| Column | Type | Values | Description |
|--------|------|--------|-------------|
| `category` | String | `regular`, `legendary`, `mythical` | Rarity/special status of the Pokémon |
| `stage` | String | `s1c2`, `s1c3`, `s2c2`, `s2c3`, `s3c3`, `single` | Evolutionary stage and chain length. Format: `s{stage}c{chain_length}`. E.g. `s2c3` = stage 2 of a 3-stage chain. `single` = no evolution |

---

## Base Stats Columns
Sum of all 6 stats = `total_stats`.

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `total_stats` | Integer | 175 – 720 | Sum of all 6 base stats (BST) |
| `hp` | Integer | 1 – 255 | Hit Points — determines max health in battle |
| `atk` | Integer | 5 – 190 | Attack — physical move damage |
| `def` | Integer | 5 – 250 | Defense — physical damage resistance |
| `sp_atk` | Integer | 10 – 194 | Special Attack — special move damage |
| `sp_def` | Integer | 20 – 250 | Special Defense — special damage resistance |
| `spe` | Integer | 5 – 200 | Speed — determines turn order in battle |

---

## EV (Effort Value) Columns
EVs are points granted to the player's Pokémon after defeating this species. Exactly one or two columns are non-zero per Pokémon.

| Column | Type | Values | Description |
|--------|------|--------|-------------|
| `ev_hp` | Integer | 0 – 3 | HP EVs granted on defeat |
| `ev_atk` | Integer | 0 – 3 | Attack EVs granted on defeat |
| `ev_def` | Integer | 0 – 3 | Defense EVs granted on defeat |
| `ev_sp_atk` | Integer | 0 – 3 | Special Attack EVs granted on defeat |
| `ev_sp_def` | Integer | 0 – 3 | Special Defense EVs granted on defeat |
| `ev_spe` | Integer | 0 – 3 | Speed EVs granted on defeat |

---

## Training / Breeding Columns

| Column | Type | Range / Values | Description |
|--------|------|----------------|-------------|
| `capture_rate` | Integer | 3 – 255 | Difficulty to catch; higher = easier. Legendaries typically 3–45, common Pokémon 190–255 |
| `growth_rate` | String | `fast`, `medium`, `medium-slow`, `slow`, `erratic`, `fluctuating` | How much experience is needed to reach level 100 |
| `base_experience` | Integer | 36 – 608 | Experience points granted when this species is defeated. Scales with BST and stage |
| `egg_group_1` | String | `monster`, `water1`, `water2`, `water3`, `bug`, `flying`, `ground`, `fairy`, `plant`, `humanlike`, `mineral`, `amorphous`, `dragon`, `indeterminate`, `no-eggs` | Primary egg group for breeding compatibility |
| `egg_group_2` | String | Same as egg_group_1, or empty | Secondary egg group; empty if only one group |

---

## Notes
- `type_2`, `egg_group_2` are empty strings for mono-typed or single-egg-group Pokémon
- `stage` was derived via PokeAPI evolution chain endpoint
- `height` and `weight` are the basis for engineered features: `density_ratio`, `streamlining`, `power_density`

---

