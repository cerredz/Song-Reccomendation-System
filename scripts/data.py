import pandas as pd
from pprint import pprint
import time
import json

def load_data(p_col_names: bool, max_rows: int):
    data = pd.read_csv("../data/spotify_dataset.csv", nrows=max_rows)
    data = data.dropna()

    print(data.size)
    print(data.shape)
    
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
    normalized_params = {}

    for feature in features:
        x_min = data[feature].min()
        x_max = data[feature].max()
        normalized_params[feature] = {"min": int(x_min), "max": int(x_max)}
        if x_max == x_min:
            data[feature] = 0.0
        else:
            data[feature] = (data[feature] - x_min) / (x_max - x_min)

    with open("../data/normalization-params.json", "w") as json_file:
        json.dump(normalized_params, json_file, indent=4)

    return data

# Process the non numerical features before training the data
def process_non_num_features(data):
    # create unqiue ID mappings for artists, genres, and emotion
    artists = data["Artist(s)"]
    genres = data["Genre"]
    emotions = data["emotion"]

    artist_mapping = {}
    genre_mapping = {}
    emotion_mapping = {}

    artist_count = genre_count = emotion_count = 0

    # artists
    for art_list in artists:
        first_artist = art_list.split(",")[0].strip().lower()
        if first_artist and first_artist not in artist_mapping:
            artist_mapping[first_artist] = artist_count
            artist_count += 1
    
    # genres
    for gen_list in genres:
        first_gen = gen_list.split(",")[0].strip().lower()
        if first_gen and first_gen not in genre_mapping:
            genre_mapping[first_gen] = genre_count
            genre_count += 1

    # emotions
    for emotion in emotions:
        if emotion and emotion not in emotion_mapping:
            emotion_mapping[emotion] = emotion_count
            emotion_count += 1

    data["Artist_IDS"] = data["Artist(s)"].apply(
        lambda x: artist_mapping.get(x.split(",")[0].strip().lower() if x else "unknown", 0)
    )

    data["Genre_IDS"] = data["Genre"].apply(
        lambda x: genre_mapping.get(x.split(",")[0].strip().lower() if x else "unknown", 0)
    )

    data["Emotion_IDS"] = data["emotion"].apply(
        lambda x: emotion_mapping.get(x.split(",")[0].strip().lower() if x else "unknown", 0)
    )

    # save the dictionaries to files
    with open("../data/artist-json.json", "w") as json_file:
        json.dump(artist_mapping, json_file, indent=4)
    
    with open("../data/genre-json.json", "w") as json_file:
        json.dump(genre_mapping, json_file, indent=4)
    
    with open("../data/emotion-json.json", "w") as json_file:
        json.dump(emotion_mapping, json_file, indent=4)

    return data, artist_count, genre_count, emotion_count

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
    start = time.time()
    n_rows = 10000000
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.max_columns', None)
    # load data
    data = load_data(p_col_names=False, max_rows=n_rows)

    # normalize numerical data
    data = embed_num_data(data)
    
    # turn non-numerical data into numerical data before we create embedding layers for it
    data, artist_count, genre_count, emotion_count = process_non_num_features(data)

    # filter out all data that we do not need
    data = data.drop(columns=["text", "Length", "Album", "Release Date", "Key", "Loudness (db)", "Time signature", "Explicit", "Good for Yoga/Stretching", "Good for Relaxation/Meditation", "Similar Artist 1", "Similar Song 1", "Similarity Score 1", "Similar Artist 2", "Similar Song 2", "Similarity Score 2", "Similar Artist 3", "Similar Song 3", "Similarity Score 3", "Artist(s)", "song", "emotion", "Genre"])
    
    # save pre-processed data to a csv file
    data.to_csv("../data/pre-processed-data.csv", index=False)

    # save the counts to another csv file
    counts_df = pd.DataFrame({
        'Category': ['Artists', 'Genres', 'Emotions'],
        'Count': [artist_count, genre_count, emotion_count]
    })

    counts_df.to_csv("../data/counts.csv", index=False)

    end = time.time()

    print(f"🟢 Pre-Processed {n_rows} rows of data in {end - start:.2f} seconds")
