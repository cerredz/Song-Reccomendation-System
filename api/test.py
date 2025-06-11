import requests

# Function to test the /recommend endpoint
def test_recommend(data):
    try:
        response = requests.post(
            "http://localhost:5000/recommend",
            json=data
        )

        print(response.json())
            
        return response.json()

    
    except Exception as e:
        print("/recommend error: ", e)


if __name__ == "__main__":

    data = {
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
        "genre": "hip hop", # Common genre for Drake, ID 0 in genre-json.json
        "emotion": "joy",   # Common emotion for some of Drake's popular tracks, ID 1 in emotion-json.json
        "n": 1
    }

    test_recommend(data)
        