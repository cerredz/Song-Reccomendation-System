import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Embedding
from tensorflow.keras import layers, Model
from pandas import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split

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

# Prepares the pre-processed data to be inputted into the autoencoder
def prepare_data(df, embedding_data):

    # Numerical Data
    num_cols = df.columns.tolist()
    num_data = df[num_cols].values

    # Non-Numical Data
    artist_data = embedding_data["Artist_IDS"].values
    genre_data = embedding_data["Genre_IDS"].values
    emotion_data = embedding_data["Emotion_IDS"].values

    train_num_data, test_num_data = train_test_split(num_data, test_size=.2, random_state=42)
    train_artist_data, test_artist_data = train_test_split(artist_data, test_size=.2, random_state=42)
    train_genre_data, test_genre_data = train_test_split(genre_data, test_size=.2, random_state=42)
    train_emotion_data, test_emotion_data = train_test_split(emotion_data, test_size=.2, random_state=42)  

    return num_cols, train_num_data, test_num_data, train_artist_data, test_artist_data, train_genre_data, test_genre_data, train_emotion_data, test_emotion_data

# buidl the autoenc
def build_autoencoder(num_features, num_artists, num_genres, num_emotions, embedding_dim_artist=50, 
    embedding_dim_genre=25, embedding_dim_emotion=25,latent_dim=32):

    # Define inputs
    input_numerical = layers.Input(shape=(num_features + 1), name="numerical_input")
    input_artist = layers.Input(shape=(1,), name="artist_input", dtype=tf.int32)
    input_genre = layers.Input(shape=(1,), name="genre_input", dtype=tf.int32)
    input_emotion = layers.Input(shape=(1,), name="emotion_input", dtype=tf.int32)

    # Create embedding layers
    artist_embedding = layers.Embedding(num_artists, embedding_dim_artist, name="artist_embedding")(input_artist)
    artist_embedding = layers.Flatten()(artist_embedding)

    genre_embedding = layers.Embedding(num_genres, embedding_dim_genre, name="genre_embedding")(input_genre)
    genre_embedding = layers.Flatten()(genre_embedding)

    emotion_embedding = layers.Embedding(num_emotions, embedding_dim_emotion, name="emotion_embedding")(input_emotion)
    emotion_embedding = layers.Flatten()(emotion_embedding)

    # Concatenate Inputs
    concat_inputs = layers.Concatenate()([input_numerical, artist_embedding, genre_embedding, emotion_embedding])

    # Encoder
    encoder = layers.Dense(64, activation="relu")(concat_inputs)
    encoder = layers.Dropout(.15)(encoder)
    encoder = layers.Dense(latent_dim, activation=None, name="latent_vector")(encoder)

    # Decoder
    decoder = layers.Dense(64, activation="relu")(encoder)
    decoder = layers.Dropout(.15)(decoder)
    decoder = layers.Dense(num_features + embedding_dim_artist + embedding_dim_genre + embedding_dim_emotion, activation="sigmoid", name="reconstructed_output")(decoder)

    # Models
    autoencoder = Model(inputs=[input_numerical, input_artist, input_genre, input_emotion], outputs=decoder)
    encoder_model = Model(inputs=[input_numerical, input_artist, input_genre, input_emotion], outputs=encoder)

    # Compile
    autoencoder.compile(optimizer="adam", loss="mse", metrics=["mse"])

    return autoencoder, encoder_model

# trains the autoencoder on our traing and test data
def train_autoencoder(autoencoder, num_cols, train_num_data, test_num_data, train_artist_data, test_artist_data, train_genre_data, test_genre_data, train_emotion_data, test_emotion_data, epochs=20, batch_size=32):
    pass

if __name__ == "__main__":

    # number of input features
    num_features = 17

    # load pre-processed data
    df, embedding_data = load_preprocessed_data()

    # prepare the pre-processed data
    num_cols, train_num_data, test_num_data, train_artist_data, test_artist_data, train_genre_data, test_genre_data, train_emotion_data, test_emotion_data = prepare_data(df, embedding_data)

    # get number stats for embedding layers
    num_artists, num_genres, num_emotions = get_training_data_stats(df)

    #autoencoder, encoder_model = build_autoencoder(num_features=num_features, num_artists=num_artists,num_emotions=num_emotions, num_genres=num_genres)
    





