import pandas as pd

def load_data(path="data/games.csv"):
    df = pd.read_csv(path)
    return df