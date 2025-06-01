from math import comb
import pandas as pd

indexes = ["Resources", "Food (S)", "Food (W)", "Ore (S)", "Ore (W)", "Oil (S)", "Oil (W)", "Titanium", "Xanium"]

def main():
    generate_and_export_named_dfs(value_sets)

def binomial_probabilities(n, p):
    return [comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in range(n + 1)]

def multi_binomial_probabilities(n, values):
    probabilities = [v / 1000 for v in values]
    data = {}
    for i, p in enumerate(probabilities):
        data[indexes[i + 1]] = binomial_probabilities(n, p)  # skip "Resources" in columns

    df = pd.DataFrame(data)
    df = df * (10**10)

    # Ensure index goes from 0 to 8
    df = df.reindex(range(0, 9), fill_value=0)

    # Cap settings per column (for 8 columns)
    caps = [5, 3, 5, 3, 3, 1, 2, 1]

    for i, cap in enumerate(caps):
        col = df.columns[i]
        overflow = df.loc[cap+1:, col].sum()
        df.loc[cap, col] += overflow
        df.loc[cap+1:8, col] = 0  # Clear overflow rows

    return df

def generate_and_export_named_dfs(named_value_sets, output_dir='.'):
    for value_set in named_value_sets:
        name = value_set[0]
        values = value_set[1:9]  # Only take the 8 values
        df = multi_binomial_probabilities(10, values)
        file_path = f"{output_dir}/{name}.csv"
        df.to_csv(file_path)
        print(f"Exported: {file_path}")

value_sets = [
    ["Abundant", 150, 100, 150, 100, 100, 100, 100, 0],
    ["Fertile", 400, 400, 100, 100, 0, 0, 0, 0],
    ["Mountain", 0, 0, 250, 250, 100, 100, 0, 0],
    ["Desert", 0, 0, 0, 0, 250, 250, 150, 0],
    ["Volcanic", 0, 0, 250, 250, 200, 200, 0, 0],
    ["Highlands", 250, 250, 250, 250, 0, 0, 0, 0],
    ["Swamp", 250, 250, 0, 0, 100, 100, 100, 0],
    ["Barren", 0, 0, 50, 50, 50, 50, 200, 25],
    ["Radiant", 0, 0, 0, 0, 0, 0, 400, 0]
]

if __name__ == "__main__":
    main()
