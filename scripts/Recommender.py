from models import load_saved_model
import pandas as pd
import sys
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import heapq

class Recommender():
    autoencoder, encoder_model = load_saved_model()
    latent_dict = {}
    age_dict = {}
    normalized_params = {} # min/max values used for normalizing input

    def __init__(self):
        if not Recommender.latent_dict:
            Recommender.latent_dict = self.create_latent_lookup_table()

        if not Recommender.age_dict:
            Recommender.age_dict = self.create_age_dict()

        if not Recommender.normalized_params:
            Recommender.normalized_params = self.create_normalized_params()

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
    
    def create_normalized_params(self):
        with open("../data/normalization-params.json") as json_file:
            return json.load(json_file)
    
    def normalize_value(self, value, feature_name):
        if value is None:
            return 0.0
        
        params = Recommender.normalized_params.get(feature_name)
        if not params:
            return 0.0
            
        x_min = params["min"]
        x_max = params["max"]
        
        if x_max == x_min:
            return 0.0
        else:
            return (value - x_min) / (x_max - x_min)

    # Generates a latent space on the user inputted data using the encoder model
    def generate_latent_space(self, n, data):
        
        # process 17 numerical features of data (same column order as pre-processed-data.csv)
        num_data = []
        
        feature_mapping = {
            "tempo": "Tempo",
            "popularity": "Popularity", 
            "energy": "Energy",
            "danceability": "Danceability",
            "positiveness": "Positiveness",
            "speechiness": "Speechiness",
            "liveness": "Liveness",
            "acousticness": "Acousticness",
            "instrumentalness": "Instrumentalness",
            "good_for_party": "Good for Party",
            "good_for_work_study": "Good for Work/Study",
            "good_for_exercise": "Good for Exercise",
            "good_for_running": "Good for Running",
            "good_for_driving": "Good for Driving",
            "good_for_social_gatherings": "Good for Social Gatherings",
            "good_for_morning_routine": "Good for Morning Routine",
            "good_for_meditation_stretching": "Good For Meditation/Stretching"
        }
        
        # Normalize each numerical feature
        for input_key, feature_name in feature_mapping.items():
            normalized_value = self.normalize_value(data.get(input_key), feature_name)
            num_data.append(normalized_value)
        
        # process the non-numerical data
        artist_value = 0 if data["artist"] is None else Recommender.age_dict["artist"].get(data["artist"].lower(), 0)
        genre_value = 0 if data["genre"] is None else Recommender.age_dict["genre"].get(data["genre"].lower(), 0) 
        emotion_value = 0 if data["emotion"] is None else Recommender.age_dict["emotion"].get(data["emotion"], 0)

        # run the model with the properly formatted input data
        num_data_array = np.array([num_data]) 
        artist_array = np.array([artist_value])  
        genre_array = np.array([genre_value])  
        emotion_array = np.array([emotion_value])  
        
        predictions = Recommender.encoder_model.predict([num_data_array, artist_array, genre_array, emotion_array])

        # return the 32d latent space
        return predictions[0]
    
    # Find similiar latent spaces to a given latent space
    def get_similiar_latent_space(self, latent_space, n):
        min_heap = []
        
        for key, value in Recommender.latent_dict.items():
            latent_key = [float(x) for x in key]
            cosine_similarity_score = self.get_cosine_similiarity([latent_key], [latent_space])
            
            if cosine_similarity_score > 0.6:  # Only consider items above threshold
                print(cosine_similarity_score)
                if len(min_heap) < n:
                    # Heap not full, just add the item
                    heapq.heappush(min_heap, (cosine_similarity_score, value))
                elif cosine_similarity_score > min_heap[0][0]:
                    # New score is better than the worst in our top-n
                    # Remove the worst and add the new one
                    heapq.heapreplace(min_heap, (cosine_similarity_score, value))
        
        # Convert heap to sorted list (highest scores first)
        # Since it's a min heap, we need to sort in descending order
        results = sorted(min_heap, key=lambda x: x[0], reverse=True)
        
        # Return as list of dictionaries with score and metadata
        return [{"score": score, "metadata": metadata} for score, metadata in results]

    # Helper function, used to determine the cosine similiarity between two arrays
    def get_cosine_similiarity(self, x, y):
        similiarity_matrix = cosine_similarity(x, y)
        similiarity = similiarity_matrix[0][0]
        return similiarity

if __name__ == "__main__":
    recommender = Recommender()
    
    # Sample data for testing
    sample_data = {
        "tempo": 120.5,
        "popularity": 40,
        "energy": 83,
        "danceability": 50 ,
        "positiveness": 80,
        "speechiness": 0.1,
        "liveness": 80,
        "acousticness": 60,
        "instrumentalness": 40,
        "good_for_party": 1,
        "good_for_work_study": 0,
        "good_for_exercise": 1,
        "good_for_running": 1,
        "good_for_driving": 0,
        "good_for_social_gatherings": 1,
        "good_for_morning_routine": 0,
        "good_for_meditation_stretching": 0,
        "artist": "Taylor Swift",
        "genre": "pop",
        "emotion": "happy"
    }
    
    # Call the function
    print("Testing generate_latent_space with sample data:")
    latent_space = recommender.generate_latent_space(n=5, data=sample_data)
    recommender.get_similiar_latent_space(latent_space, 2)
    
