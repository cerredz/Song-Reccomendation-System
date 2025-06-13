import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.Recommender import Recommender
import numpy as np
import heapq

# Create a Flask application instance
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Lazy load the recommender to avoid initialization during import
recommender = None

def get_recommender():
    global recommender
    if recommender is None:
        print("Initializing recommender for the first time...")
        recommender = Recommender()
        print("Recommender initialized successfully!")
    return recommender

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/recommend", methods=["POST", "GET"])
def recommend_songs():
    try:
        print("Recommending a song based on user data...")
        data = request.get_json()
        
        # Get the recommender instance (lazy loaded)
        rec = get_recommender()
        
        n = data.get('n', 5)
    
        # Generate the latent space for this combination
        latent_space = rec.generate_latent_space(n, data)
        print("Generated the latent space for user.")

        # Get similar latent spaces
        similar_songs = rec.get_similiar_latent_space(latent_space, n)

        if similar_songs:
            print("Successfully retrieved similiar songs for user")
            
            # Convert numpy float32 to regular Python float for JSON serialization
            for song in similar_songs:
                if isinstance(song['score'], np.float32):
                    song['score'] = float(song['score'])
            
            return jsonify({
                "status": "success",
                "message": "Songs recommended successfully",
                "data": similar_songs
            })
        
        print("Failed to find similiar songs for a user")
        return jsonify({
            "status": "error",
            "message": "Failed to recommend songs",
            "data": None
        })
        
    except Exception as e:
        print(f'Internal Server Error: /recommend: {e}')
        return jsonify({
            'status': 'error',
            'message': 'Failed to recommend a song, internal server error'
        }), 500

# Run the application if the script is executed directly
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Export the app for Render/gunicorn
application = app
    