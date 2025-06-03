import pandas as pd
from pprint import pprint

def load_data(p_col_names: bool, max_rows: int):
    data = pd.read_csv("../data/spotify_dataset.csv", nrows=max_rows)
    data.dropna()
    
    if p_col_names:
        print("Column Names:")
        for col in data.columns:
            pprint(col)

    return data

# loaded the data, now filter it with the data that we do not need
def filter_data(data):
    pass



if __name__ == "__main__":
    data = load_data(p_col_names=True, max_rows=5000)
    
    
    
