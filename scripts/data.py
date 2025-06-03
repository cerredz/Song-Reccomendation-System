import pandas as pd
from pprint import pprint
from sklearn.preprocessing import MinMaxScaler



def load_data(p_col_names: bool, max_rows: int):
    data = pd.read_csv("../data/spotify_dataset.csv", nrows=max_rows)
    data = data.dropna()
    
    if p_col_names:
        print("Column Names:")
        for col in data.columns:
            pprint(col)

    return data

# Using the numerical features, compress highly correlated features into 1 and normalize all scores
def embed_num_data(data):
    data["Good For Meditation/Stretching"] = (
        data["Good for Relaxation/Meditation"] + data["Good for Yoga/Stretching"]
    )    
    
    features = get_num_features() + ["Good For Meditation/Stretching"]
    for feature in features:
        x_min = data[feature].min()
        x_max = data[feature].max()
        if x_max == x_min:
            data[feature] = 0.0
        else:
            data[feature] = (data[feature] - x_min) / (x_max - x_min)
    return data

# Process the artist non numerical features before training the data
def process_artists(data):
    # start with the artists
    artists = data["Artist(s)"]
    artist_mapping = {}
    artist_count = 1
    for art_list in artists:
        first_artist = art_list.split(",")[0].strip().lower()
        if first_artist and first_artist not in artist_mapping:
            artist_mapping[first_artist] = artist_count
            artist_count += 1

    data["Artist_IDS"] = data["Artist(s)"].apply(
        lambda x: artist_mapping.get(x.split(",")[0].strip().lower() if x else "unknown", 0)
    )

    return data

def get_num_features():
    return [
        "Popularity",
        "Energy",
        "Danceability",
        "Positiveness",
        "Speechiness",
        "Liveness",
        "Acousticness",
        "Instrumentalness",
        "Tempo",
    ]


if __name__ == "__main__":
    data = load_data(p_col_names=False, max_rows=2000)
    data = embed_num_data(data)
    pd.set_option('display.max_rows', None)  # Show all rows
    data = process_artists(data)
    print(data["Artist_IDS"])



    
    
    
