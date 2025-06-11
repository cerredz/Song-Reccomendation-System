import tensorflow as tf
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Save the full model after training it
def save_model(autoencoder, encoding_model):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    autoencoder.save(os.path.join(project_root, 'models', 'autoencoder-model.keras'))
    encoding_model.save(os.path.join(project_root, 'models', 'encoder-model.keras'))

    return True

# Load and return the saved model from previous training session 
def load_saved_model():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    autoencoder = tf.keras.models.load_model(os.path.join(project_root, 'models', 'autoencoder-model.keras'))
    encoder_model = tf.keras.models.load_model(os.path.join(project_root, 'models', 'encoder-model.keras'))

    encoder_model.compile(optimizer='adam', loss='mse', metrics=['mse'])

    return autoencoder, encoder_model
