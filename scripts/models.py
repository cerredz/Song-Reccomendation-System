import tensorflow as tf

# Save the full model after training it
def save_model(autoencoder, encoding_model):
    autoencoder.save("../models/autoencoder-model.keras")
    encoding_model.save("../models/encoder-model.keras")

    return True

# save only the weights after training the model
def save_model_weights(autoencoder, encoding_model):
    pass

# Load and return the saved model from previous training session 
def load_saved_model():

    autoencoder = tf.keras.saving.load_model("../models/autoencoder-model.keras")
    encoding_model = tf.keras.saving.load_model("../models/encoding-model.keras")

    return autoencoder, encoding_model

# Load and return the saved weights from previous training session
def load_saved_weights():
    pass
