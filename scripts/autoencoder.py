import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Embedding
from tensorflow.keras import layers, Model
from pandas import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split
from visualize import plot_training_history, visualize_latent_space
from models import save_model

print("Tensorflow Version: ", tf.__version__)
print("Physical GPU Devices:", tf.config.list_physical_devices('GPU'))
if not tf.config.list_physical_devices('GPU'):
    print("WARNING: No GPU detected, training on CPU")

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

    num_artists = counts[0] + 1
    num_genres = counts[1] + 1
    num_emotions = counts[2] + 1
    
    return num_artists, num_genres, num_emotions

# Prepares the pre-processed data to be inputted into the autoencoder
def prepare_data(df, embedding_data):
    # Get numerical data
    num_cols = df.columns.tolist()
    num_data = df[num_cols].values

    # Get non-numerical data
    artist_data = embedding_data["Artist_IDS"].values
    genre_data = embedding_data["Genre_IDS"].values
    emotion_data = embedding_data["Emotion_IDS"].values

    # split data into train, val, and test data
    indices = np.arange(len(df))
    train_idx, temp_idx = train_test_split(indices, test_size=0.2, random_state=42)
    val_idx, test_idx = train_test_split(temp_idx, test_size=0.5, random_state=42)

    # concat into single arrays
    train_data = [num_data[train_idx], artist_data[train_idx], genre_data[train_idx], emotion_data[train_idx]]
    val_data = [num_data[val_idx], artist_data[val_idx], genre_data[val_idx], emotion_data[val_idx]]
    test_data = [num_data[test_idx], artist_data[test_idx], genre_data[test_idx], emotion_data[test_idx]]

    return num_cols, train_data, val_data, test_data

# buidl the autoenc
def build_autoencoder(num_features, num_artists, num_genres, num_emotions, embedding_dim_artist=100, 
    embedding_dim_genre=50, embedding_dim_emotion=25, latent_dim=20):

    # Define inputs
    input_numerical = layers.Input(shape=(num_features,), name="numerical_input")
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
def train_autoencoder(autoencoder, num_cols, train_data, val_data, test_data, epochs=20, batch_size=256):

    train_num, train_artist, train_genre, train_emotion = train_data
    val_num, val_artist, val_genre, val_emotion = val_data

    print("Training on device:", tf.test.gpu_device_name() or "CPU")
    print(f"Training with batch size={batch_size}, epochs={epochs}")
    
    with tf.device('/GPU:0'):
        history = autoencoder.fit(
            x=[train_num, train_artist, train_genre, train_emotion],
            y=np.concatenate([train_num, 
                              autoencoder.get_layer("artist_embedding")(train_artist), 
                              autoencoder.get_layer("genre_embedding")(train_genre), 
                              autoencoder.get_layer("emotion_embedding")(train_emotion)], axis=1),
            validation_data=([val_num, val_artist, val_genre, val_emotion], 
                             np.concatenate([val_num, 
                                            autoencoder.get_layer("artist_embedding")(val_artist), 
                                            autoencoder.get_layer("genre_embedding")(val_genre), 
                                            autoencoder.get_layer("emotion_embedding")(val_emotion)], axis=1)),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
            callbacks=[tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)]
        )

    return history

# Tests the autoencoder with the test data
def evaluate_autoencoder(autoencoder, test_data, batch_size=256):
    test_num, test_artist, test_genre, test_emotion = test_data

    test_target = np.concatenate([test_num,
                                  autoencoder.get_layer("artist_embedding")(test_artist),
                                  autoencoder.get_layer("genre_embedding")(test_genre),
                                  autoencoder.get_layer("emotion_embedding")(test_emotion)], axis=1)
    
    with tf.device("/GPU:0"):
        test_loss = autoencoder.evaluate(
            x=[test_num, test_artist, test_genre, test_emotion],
            y=[test_target],
            batch_size=batch_size,
            verbose=0
        )

        predictions = autoencoder.predict([test_num, test_artist, test_genre, test_emotion])

    return test_loss, predictions, test_target


if __name__ == "__main__":

    # number of input features
    num_features = 17
    batch_size = 16384

    # load pre-processed data
    df, embedding_data = load_preprocessed_data()

    # prepare the pre-processed data
    num_cols, train_data, val_data, test_data = prepare_data(df, embedding_data)

    # get number stats for embedding layers
    num_artists, num_genres, num_emotions = get_training_data_stats(df)

    # build, train, and evaluate the autoencoder
    autoencoder, encoder_model = build_autoencoder(num_features=num_features, num_artists=num_artists,num_emotions=num_emotions, num_genres=num_genres)
    
    print(autoencoder.summary())

    history = train_autoencoder(autoencoder, num_cols, train_data, val_data, test_data, epochs=50, batch_size=batch_size)

    test_loss, predictions, test_target = evaluate_autoencoder(autoencoder, test_data, batch_size=batch_size)

    # Visualize the results
    #visualize_latent_space(encoder_model, test_data, method="tsne", save_path="../visualizations/training/latent-space.png")

    #plot_training_history(history)

    # save the model for future use
    save_model(autoencoder, encoder_model)

    print("Successfully trained and saved the model.")


    






