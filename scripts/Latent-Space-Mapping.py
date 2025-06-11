


'''
This files serves as a script for making a lookup table for the songs with the latent spaces. In other words
'''
from models import load_saved_model
from data import load_data, embed_num_data, process_non_num_features
import pandas as pd
import numpy as np
import tensorflow as tf

def create_latent_lookup_table(n_rows=10000000, batch_size=10000):

    # load the already trained models
    autoencoder, encoder_model = load_saved_model()

    # get the data that was used to trained the model (will be used to re-calculating latent spaces)
    data = load_data(p_col_names=False, max_rows=n_rows)
    data = embed_num_data(data)
    data, artist_count, genre_count, emotion_count = process_non_num_features(data)

    # get the new data we will attach to each latent space
    metadata_cols = ["Artist(s)", "Genre", "song", "Length", "Album", "Release Date", 
                     "Similar Artist 1", "Similar Song 1", "Similarity Score 1", 
                     "Similar Artist 2", "Similar Song 2", "Similarity Score 2", 
                     "Similar Artist 3", "Similar Song 3", "Similarity Score 3"]

    metadata = data[metadata_cols]
    
    numerical_data = data.drop(columns=metadata_cols + ["text", "Key", "Loudness (db)", "Time signature", 
                                                       "Explicit", "Good for Yoga/Stretching", 
                                                       "Good for Relaxation/Meditation", "emotion", "Artist_IDS", "Genre_IDS", "Emotion_IDS"])
    
    artist_ids = data["Artist_IDS"].values
    genre_ids = data["Genre_IDS"].values
    emotion_ids = data["Emotion_IDS"].values

    # Adjust n_rows to the actual number of rows in the data after processing
    n_rows = len(numerical_data)
    print(f"Total rows after processing: {n_rows}")

    all_latent_vectors = []
    all_metadata = []

    # run the encoding model in batches, saving the resulting latent spaces along with the new data into a csv file
    batches = (n_rows + batch_size - 1) // batch_size  
    for i in range(batches):
        # get start and end index of batch
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, n_rows)

        # Skip if the batch is empty
        if start_idx >= n_rows:
            print(f"Skipping batch {i} as start_idx ({start_idx}) exceeds data length ({n_rows})")
            continue

        # get the data in the current batch
        batch_numerical = numerical_data.iloc[start_idx:end_idx].values
        batch_artists = artist_ids[start_idx:end_idx]
        batch_genres = genre_ids[start_idx:end_idx]
        batch_emotion = emotion_ids[start_idx:end_idx]
        batch_meta = metadata.iloc[start_idx:end_idx]

        # Check if batch is empty or has incorrect shape
        if len(batch_numerical) == 0:
            print(f"Skipping empty batch {i} (start_idx: {start_idx}, end_idx: {end_idx})")
            continue

        print(f"Processing batch {i+1}/{batches} with {len(batch_numerical)} samples")

        # run the encoder model with the batch data
        predictions = encoder_model.predict([batch_numerical, batch_artists, batch_genres, batch_emotion], batch_size=batch_size)

        # Append to lists
        all_latent_vectors.append(predictions)
        all_metadata.append(batch_meta)

    # Concatenate all batches
    all_latent_vectors = np.vstack(all_latent_vectors)
    all_metadata = pd.concat(all_metadata, ignore_index=True)
    
    # Determine the number of latent dimensions from the shape of all_latent_vectors
    latent_dim = all_latent_vectors.shape[1]
    print(f"Latent dimension detected: {latent_dim}")

    # Create a DataFrame with metadata and latent vectors
    latent_df = pd.concat([all_metadata.reset_index(drop=True), 
                          pd.DataFrame(all_latent_vectors, columns=[f"latent_{i}" for i in range(latent_dim)])], 
                          axis=1)

    # Save to CSV
    latent_df.to_csv("../data/latent-space-lookup.csv", index=False)

if __name__ == "__main__":
    create_latent_lookup_table()



