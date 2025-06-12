import tensorflow as tf
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import shutil

# Function to download file from URL
def download_file(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with requests.get(url, stream=True) as r:
        with open(local_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_path

# Save the full model after training it
def save_model(autoencoder, encoding_model):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    autoencoder.save(os.path.join(project_root, 'models', 'autoencoder-model.keras'))
    encoding_model.save(os.path.join(project_root, 'models', 'encoder-model.keras'))

    return True

# Load and return the saved model from previous training session 
def load_saved_model():
    # Define GitHub Release URLs for models (replace with actual URLs)
    github_urls = {
        'autoencoder_model': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/autoencoder-model.keras',
        'encoder_model': 'https://github.com/cerredz/Song-Reccomendation-System/releases/download/v1.0.0/encoder-model.keras'
    }
    
    # Define local temporary paths for serverless environment
    local_paths = {
        'autoencoder_model': os.path.join('/tmp', 'models', 'autoencoder-model.keras'),
        'encoder_model': os.path.join('/tmp', 'models', 'encoder-model.keras')
    }
    
    # Download models if not present
    for key in github_urls:
        local_path = local_paths.get(key)
        if not os.path.exists(local_path):
            url = github_urls.get(key)
            print(f'Downloading {key} from {url} to {local_path}')
            download_file(url, local_path)

    # Load models from local paths
    autoencoder = tf.keras.models.load_model(local_paths['autoencoder_model'])
    encoder_model = tf.keras.models.load_model(local_paths['encoder_model'])

    encoder_model.compile(optimizer='adam', loss='mse', metrics=['mse'])

    return autoencoder, encoder_model
