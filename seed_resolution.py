import pandas as pd
import random
import json
import re
from namegen import generate_name, generate_system_name

# Maps seed prefixes (int ranges) to world type CSV names
world_type_map = {
    "Abundant": (0, 12),
    "Fertile": (13, 62),
    "Mountain": (63, 112),
    "Desert": (113, 137),
    "Volcanic": (138, 162),
    "Highlands": (163, 200),
    "Swamp": (201, 238),
    "Barren": (239, 243),
    "Radiant": (244, 249),
    "Barred": (250, 250),
    "Null": (251, 999)
}

def main():
    seed_32 = random.randint(0, 10**32 - 1)
    worlds = process_system_seed(seed_32)

    json_str = json.dumps(worlds, indent=2)

    # Fix for compacting the planet_resources list to one line correctly
    json_str = re.sub(
        r'"planet_resources": \[\s+([^]]+?)\s+\]',
        lambda m: f'''"planet_resources": [{", ".join(
            line.strip().rstrip(',') for line in m.group(1).splitlines() if line.strip().strip(',') != ""
        )}]''',
        json_str
    )

    print(json_str)

def get_world_type_from_seed(seed, world_type_map):
    seed_str = str(seed).zfill(20)
    first_three_digits = int(seed_str[:3])
    for world, (start, end) in world_type_map.items():
        if start <= first_three_digits <= end:
            return world
    return "Null"

def get_success_from_roll(df_column, value):
    """Return the number of successes corresponding to the value using CDF lookup."""
    cdf = df_column.cumsum()
    for k, threshold in cdf.items():
        if value <= threshold:
            return k
    return cdf.index[-1]

def resolve_planet_seed(df, seed):
    """
    Given a DataFrame and a 20-digit seed,
    returns a list of 8 success values based on slices of the seed.
    """
    seed_str = str(seed).zfill(20)
    # Use digits 4-20 (17 digits), take 8 slices of 10 digits each starting at i
    # This requires overlapping slices, so slicing carefully:
    # slices: [3:13], [4:14], [5:15], ..., [10:20]
    # or maybe slices starting at 3, 4, 5,... to 10 for length 10 each
    results = []
    for i in range(8):
        slice_str = seed_str[3 + i : 3 + i + 10]
        value = int(slice_str)
        column = df.iloc[:, i]
        success = get_success_from_roll(column, value)
        results.append(success)
    return results

def process_seed(seed):
    # Determine world type
    world_type = get_world_type_from_seed(seed, world_type_map)
    if world_type == "Null":
        return world_type, [0,0,0,0,0,0,0,0]
    if world_type == "Barred":
        return world_type,[0,0,0,0,0,0,0,2]
    
    # Load corresponding CSV
    df = pd.read_csv(f"system_tables/{world_type}.csv", index_col=0)
    
    # Resolve successes
    results = resolve_planet_seed(df, seed)
    return world_type, results

def process_system_seed(seed_32_digit):
    seed_str = str(seed_32_digit).zfill(32)
    subseeds = [
        seed_str[0:20],   # 20-digit subseeds starting at 0:20 with 3 digit offsets
        seed_str[3:23],
        seed_str[6:26],
        seed_str[9:29],
        seed_str[12:32]
    ]

    system_name = generate_system_name()
    planets = []

    for subseed_str in subseeds:
        subseed_int = int(subseed_str)
        world_type, resources = process_seed(subseed_int)
        if world_type != "Null":
            planet = {
                "planet_name": generate_name(world_type),
                "planet_type": world_type,
                "planet_resources": resources
            }
            planets.append(planet)

    return {
        "system_seed": seed_32_digit,
        "system_name": system_name,
        "system_planets": planets if planets else [{"planet_name": None, "planet_type": "None", "planet_resources": []}]
    }

if __name__ == "__main__":
    main()