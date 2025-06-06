import pandas as pd
from tensorflow.keras.layers import Embedding
from tensorflow.keras import layers, Model
from pandas import DataFrame

# load the pre-processed data
def load_preprocessed_data():
    df = pd.read_csv("../data/pre-processed-data.csv", delimiter=",", encoding="utf-8")

    embedding_columns = ['Artist_IDS', 'Genre_IDS', 'Emotion_IDS']
    embedding_data = df[embedding_columns]
    df = df.drop(columns=embedding_columns)

    return df, embedding_data

# get the number of features, artists, genres, and emotions inside of the training data
def get_training_data_stats(df: DataFrame):
    df = pd.read_csv("../data/counts.csv", delimiter=",", encoding="utf-8")
    counts = df["Count"]

    num_artists = counts[0]
    num_genres = counts[1]
    num_emotions = counts[2]

    return num_artists, num_genres, num_emotions

# buidl the autoenc
def build_autoencoder(num_features, num_artists, num_genres, num_emotions, embedding_dim_artist=50, 
    embedding_dim_genre=25, embedding_dim_emotion=25,latent_dim=22):

    # Define inputs
    input_numerical = layers.Input(shape=(num_features), name="numerical_input")
    input_artist = layers.Input(shape=(num_artists), name="artist_input")
    input_genre = layers.Input(shape=(num_genres), name="genre_input")
    input_emotion = layers.Input(shape=(num_emotions), name="emotion_input")

    return 0

if __name__ == "__main__":
    df, embedding_data = load_preprocessed_data()
    num_artists, num_genres, num_emotions = get_training_data_stats(df)



