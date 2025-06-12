import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.models import load_saved_model
import pandas as pd
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import requests
import shutil
import csv

# Function to download file from URL
def download_file(url, local_path):
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Downloading from {url} to {local_path}")
        
        response = requests.get(url, stream=True, timeout=300)  # 5 minute timeout
        response.raise_for_status()  # Raise an exception for bad status codes
        
        with open(local_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        
        # Verify file was created and has content
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            print(f"Successfully downloaded {local_path} ({os.path.getsize(local_path)} bytes)")
            return local_path
        else:
            raise Exception(f"Download failed: file {local_path} is empty or doesn't exist")
            
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        raise e

def read_csv_without_pandas(file_path):
    data = []
    headers = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Get headers
        
        for row in csv_reader:
            data.append(row)
    
    return headers, data

class Recommender():
    autoencoder = None
    encoder_model = None
    latent_dict = {}
    age_dict = {}
    normalized_params = {} # min/max values used for normalizing input

    def __init__(self):
        # Load models during initialization, not at class definition
        if Recommender.autoencoder is None or Recommender.encoder_model is None:
            print("Loading TensorFlow models...")
            Recommender.autoencoder, Recommender.encoder_model = load_saved_model()
            print("Models loaded successfully!")
        # Define GitHub Release URLs (replace with actual URLs from your GitHub Release)
        self.github_urls = {
            'latent_space_lookup': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/latent-space-lookup.csv',
            'artist_json': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/artist-json.json',
            'genre_json': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/genre-json.json',
            'emotion_json': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/emotion-json.json',
            'normalization_params': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/normalization-params.json',
            'encoder_model': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/encoder-model.keras'
        }
        # Define local temporary paths for serverless environment
        self.local_paths = {
            'latent_space_lookup': os.path.join('/tmp', 'data', 'latent-space-lookup.csv'),
            'artist_json': os.path.join('/tmp', 'data', 'artist-json.json'),
            'genre_json': os.path.join('/tmp', 'data', 'genre-json.json'),
            'emotion_json': os.path.join('/tmp', 'data', 'emotion-json.json'),
            'normalization_params': os.path.join('/tmp', 'data', 'normalization-params.json'),
            'encoder_model': os.path.join('/tmp', 'models', 'encoder-model.keras')
        }
        
        if not Recommender.latent_dict:
            Recommender.latent_dict = self.create_latent_lookup_table()

        if not Recommender.age_dict:
            Recommender.age_dict = self.create_age_dict()

        if not Recommender.normalized_params:
            Recommender.normalized_params = self.create_normalized_params()

    # Download files if not present locally
    def ensure_file(self, key):
        local_path = self.local_paths.get(key)
        if not os.path.exists(local_path):
            url = self.github_urls.get(key)
            print(f'Downloading {key} from {url} to {local_path}')
            download_file(url, local_path)
        return local_path

    # Creates a lookup table based on our 32D latent space
    def create_latent_lookup_table(self):
        table = {}
        data_path = self.ensure_file('latent_space_lookup')
        
        # Read CSV without pandas
        headers, rows = read_csv_without_pandas(data_path)
        
        # Find latent column indices
        latent_indices = [i for i, header in enumerate(headers) if header.startswith('latent_')]
        
        for row in rows:
            # Extract latent values
            latent_values = tuple(float(row[i]) for i in latent_indices)
            
            # Extract metadata
            metadata = {
                "artist": row[headers.index("Artist(s)")],
                "genre": row[headers.index("Genre")],
                "song": row[headers.index("song")],
                # ... add other fields as needed
            }
            
            table[latent_values] = metadata
        
        return table

    # creates the age (artist, genre, emotion) dict (corresponding values to each a.g.e we used during training)
    def create_age_dict(self):
        age_dict = {}

        artist_path = self.ensure_file('artist_json')
        with open(artist_path) as json_file:
            artist_data = json.load(json_file)
            age_dict['artist'] = artist_data
        
        genre_path = self.ensure_file('genre_json')
        with open(genre_path) as json_file:
            genre_data = json.load(json_file)
            age_dict['genre'] = genre_data
        
        emotion_path = self.ensure_file('emotion_json')
        with open(emotion_path) as json_file:
            emotion_data = json.load(json_file)
            age_dict['emotion'] = emotion_data
        
        return age_dict
    
    def create_normalized_params(self):
        params_path = self.ensure_file('normalization_params')
        with open(params_path) as json_file:
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
    
    # Find similar latent spaces to a given latent space
    def get_similiar_latent_space(self, latent_space, n):
        # Convert latent_space to a NumPy array if it isn't already
        latent_space = np.array(latent_space, dtype=np.float32)
        
        # Extract all latent vectors and metadata from latent_dict
        latent_keys = np.array([list(map(float, key)) for key in Recommender.latent_dict.keys()], dtype=np.float32)
        metadata_list = list(Recommender.latent_dict.values())
        
        if latent_keys.shape[0] == 0:
            return []
            
        # Compute cosine similarity for all vectors at once
        # Cosine similarity = dot product / (norm of latent_space * norm of each key)
        latent_space_norm = np.linalg.norm(latent_space)
        keys_norms = np.linalg.norm(latent_keys, axis=1)
        dot_products = np.dot(latent_keys, latent_space)
        cosine_similarities = dot_products / (latent_space_norm * keys_norms)
        
        # Filter by threshold
        threshold = 0.9
        mask = cosine_similarities > threshold
        
        # Get indices of vectors above threshold
        valid_indices = np.where(mask)[0]
        valid_similarities = cosine_similarities[valid_indices]
        valid_metadata = [metadata_list[i] for i in valid_indices]
        
        if len(valid_indices) == 0:
            return []
            
        # Get top n indices based on similarity scores
        if len(valid_indices) <= n:
            top_n_indices = np.arange(len(valid_indices))
        else:
            top_n_indices = np.argpartition(valid_similarities, -n)[-n:]
            
        # Sort the top n by similarity score (descending)
        top_n_indices = top_n_indices[np.argsort(valid_similarities[top_n_indices])[::-1]]
        
        # Return results as list of dictionaries
        return [{"score": valid_similarities[idx], "metadata": valid_metadata[idx]} for idx in top_n_indices]

    # Helper function, used to determine the cosine similiarity between two arrays
    def get_cosine_similiarity(self, x, y):
        similiarity_matrix = cosine_similarity(x, y)
        similiarity = similiarity_matrix[0][0]
        return similiarity

# Returns the default function for input data
def get_default_data(self):
    return {
        "artist": "unknown",
        "genre": "unknown",
        "emotion": "unknown",
        "num": 0.0
    }

if __name__ == "__main__":
    recommender = Recommender()
    
    # Sample data for testing - designed to match popular songs for high similarity
    sample_data = {
        "tempo": 120,  # Within range (31-200), a common tempo for hip hop/rap tracks
        "popularity": 85,  # High popularity (0-100), typical for Drake's chart-topping hits
        "energy": 70,  # Moderate to high energy (0-100), common for rap/hip hop
        "danceability": 80,  # High danceability (6-99), as Drake's songs often have strong beats
        "positiveness": 50,  # Neutral to slightly positive valence (0-100), reflecting a mix of emotions in his music
        "speechiness": 20,  # Moderate speechiness (2-97), as his songs often feature rapping
        "liveness": 30,  # Moderate liveness (1-100), suggesting some live feel or crowd energy
        "acousticness": 20,  # Low to moderate acousticness (0-100), as his music is often produced with electronic elements
        "instrumentalness": 0,  # Not instrumental (0-100), typical for vocal-heavy tracks
        "good_for_party": 1,  # Suitable for parties (0-2), common for his upbeat tracks
        "good_for_work_study": 0,  # Not for work/study (0-2)
        "good_for_exercise": 1,  # Suitable for exercise (0-2), due to high energy
        "good_for_running": 1,  # Suitable for running (0-2), due to tempo and energy
        "good_for_driving": 1,  # Suitable for driving (0-2), as his music is often played in cars
        "good_for_social_gatherings": 1,  # Suitable for social events (0-2)
        "good_for_morning_routine": 0,  # Not for morning routine (0-2)
        "good_for_meditation_stretching": 0,  # Not for meditation (0-2)
        "artist": "drake",  # Popular artist, ID 250 in artist-json.json, likely to have many similar songs
        "genre": "hip hop",  # Common genre for Drake, ID 0 in genre-json.json
        "emotion": "joy"  # Common emotion for some of Drake's popular tracks, ID 1 in emotion-json.json
    }
    
    latent_space = recommender.generate_latent_space(n=5, data=sample_data)
    similiar = recommender.get_similiar_latent_space(latent_space, 15)
    similiar_scores = [score["score"] for score in similiar]
    print([score["metadata"]["artist"] for score in similiar])
    print(similiar_scores)
    
