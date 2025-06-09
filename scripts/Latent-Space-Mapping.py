


'''
This files serves as a script for making a lookup table for the songs with the latent spaces. In other words
'''
from models import load_saved_model
from data import load_data, embed_num_data, process_non_num_features
import pandas as pd

def create_latent_lookup_table(n_rows=10000, batch_size=10000):

    # load the already trained models
    autoencoder, encoding_model = load_saved_model()

    # get the data that was used to trained the model (will be used to re-calculating latent spaces)
    data = load_data(p_col_names=False, max_rows=n_rows)
    data = embed_num_data(data)
    data, artist_count, genre_count, emotion_count = process_non_num_features(data)

    # get the new data we will attach to each latent space
    dropped_data = data[["Artist(s)","Genre", "song", "Length", "Album", "Release Date", "Similar Artist 1", "Similar Song 1", "Similarity Score 1", "Similar Artist 2", "Similar Song 2", "Similarity Score 2", "Similar Artist 3", "Similar Song 3", "Similarity Score 3"]]
    
    data = data.drop(columns=["text", "Length", "Album", "Release Date", "Key", "Loudness (db)", "Time signature", "Explicit", "Good for Yoga/Stretching", "Good for Relaxation/Meditation", "Similar Artist 1", "Similar Song 1", "Similarity Score 1", "Similar Artist 2", "Similar Song 2", "Similarity Score 2", "Similar Artist 3", "Similar Song 3", "Similarity Score 3", "Artist(s)", "song", "emotion", "Genre"])

    #new_data = pd.concat([dropped_data, data], axis=1)

    #new_data.to_csv("../data/latent-space-lookup.csv")

    # run the encoding model in batches, saving the resulting latent spaces along with the new data into a csv file
    batches = n_rows // batch_size
    for i in range(batches):
        pass
        

if __name__ == "__main__":
    create_latent_lookup_table()



