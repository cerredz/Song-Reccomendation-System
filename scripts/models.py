import tensorflow as tf

# Save the full model after training it
def save_model(autoencoder, encoding_model):
    autoencoder.save("../models/autoencoder-model.keras")
    encoding_model.save("../models/encoder-model.keras")

    return True

# Load and return the saved model from previous training session 
def load_saved_model():

    autoencoder = tf.keras.models.load_model("../models/autoencoder-model.keras")
    encoder_model = tf.keras.models.load_model("../models/encoder-model.keras")

    encoder_model.compile(optimizer="adam", loss="mse", metrics=["mse"])

    return autoencoder, encoder_model
