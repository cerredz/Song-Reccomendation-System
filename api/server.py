from flask import Flask, request, jsonify
from scripts.Recommender import Recommender

# Create a Flask application instance
app = Flask(__name__)
recommender = Recommender()

# Define a route for the home page
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/recommend", methods=["POST"])
def recommend_songs():
    try:
        data = request.get_json()
        print(data)
    
    except Exception as e:
        print(f"Internal Server Error: /recommend: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to recommend a song, internal server error"
        }), 500

# Run the application if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)