from models import load_saved_model
import pandas as pd
import sys
import json

class Recommender():
    autoencoder, encoding_model = load_saved_model()
    latent_dict = {}
    age_dict = {}

    def __init__(self):
        if not Recommender.latent_dict:
            Recommender.latent_dict = self.create_latent_lookup_table()

        if not Recommender.age_dict:
            Recommender.age_dict = self.create_age_dict()
            print(Recommender.age_dict)

    # Creates a lookup table based on our 32D latent space
    def create_latent_lookup_table(self):
        table = {}

        data = pd.read_csv("../data/latent-space-lookup.csv", delimiter=",") 
        
        # Much faster vectorized approach
        # Extract all latent columns at once (assuming 32 dimensions: latent_0 to latent_31)
        latent_cols = [f"latent_{i}" for i in range(32)]
        latent_data = data[latent_cols].values  # Convert to numpy array
        
        # Create tuples from each row (vectorized)
        latent_tuples = [tuple(row) for row in latent_data]
        
        # Extract all metadata at once
        metadata_list = data[[
            "Artist(s)", "Genre", "song", "Length", "Album", "Release Date",
            "Similar Artist 1", "Similar Song 1", "Similarity Score 1",
            "Similar Artist 2", "Similar Song 2", "Similarity Score 2", 
            "Similar Artist 3", "Similar Song 3", "Similarity Score 3"
        ]].to_dict('records')  # Convert to list of dictionaries
        
        # Create the lookup table using zip (much faster than loop)
        for latent_tuple, metadata_row in zip(latent_tuples, metadata_list):
            # Clean up the metadata keys (remove special characters if needed)
            metadata = {
                "artist": metadata_row["Artist(s)"],
                "genre": metadata_row["Genre"],
                "song": metadata_row["song"],
                "length": metadata_row["Length"],
                "album": metadata_row["Album"],
                "release_date": metadata_row["Release Date"],
                "similar_artist_1": metadata_row["Similar Artist 1"],
                "similar_song_1": metadata_row["Similar Song 1"],
                "similarity_score_1": metadata_row["Similarity Score 1"],
                "similar_artist_2": metadata_row["Similar Artist 2"],
                "similar_song_2": metadata_row["Similar Song 2"],
                "similarity_score_2": metadata_row["Similarity Score 2"],
                "similar_artist_3": metadata_row["Similar Artist 3"],
                "similar_song_3": metadata_row["Similar Song 3"],
                "similarity_score_3": metadata_row["Similarity Score 3"]
            }
            
            table[latent_tuple] = metadata
        
        print(f"Created lookup table with {len(table)} entries")
        return table
    

    # creates the age (artist, genre, emotion) dict (corresponding values to each a.g.e we used during training)
    def create_age_dict(self):
        age_dict = {}

        with open("../data/artist-json.json") as json_file:
            artist_data = json.load(json_file)
            age_dict["artist"] = artist_data
        
        with open("../data/genre-json.json") as json_file:
            genre_data = json.load(json_file)
            age_dict["genre"] = genre_data
        
        with open("../data/emotion-json.json") as json_file:
            emotion_data = json.load(json_file)
            age_dict["emotion"] = emotion_data
        
        return age_dict

    # Recommends a certain number of songs based on the input
    def recommend_song(self, n, data):
        pass



if __name__ == "__main__":
    recommender = Recommender()



        




    
        