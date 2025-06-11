# Song Recommendation System

## Overview

This project implements a sophisticated song recommendation system using a deep learning autoencoder model. The purpose of this system is to provide personalized song recommendations by learning latent representations of songs based on their features, including numerical attributes and categorical data like artist, genre, and emotion.

## Purpose of the Model

The core of this recommendation system is an autoencoder neural network designed to compress high-dimensional song data into a lower-dimensional latent space. By doing so, it captures the essential characteristics of songs, enabling the system to recommend similar songs based on their proximity in this latent space.

## Model Architecture

The model consists of an autoencoder with separate input paths for numerical and categorical data:

- **Inputs**:
  - Numerical input for song features (17 features).
  - Categorical inputs for artist, genre, and emotion IDs.
- **Embedding Layers**:
  - Artist Embedding: Maps artist IDs to a 100-dimensional vector.
  - Genre Embedding: Maps genre IDs to a 50-dimensional vector.
  - Emotion Embedding: Maps emotion IDs to a 25-dimensional vector.
- **Encoder**:
  - Concatenates numerical and embedding inputs.
  - Uses dense layers with ReLU activation and dropout for regularization.
  - Outputs a 20-dimensional latent vector representing the compressed song data.
- **Decoder**:
  - Reconstructs the input data from the latent vector using dense layers.
  - Aims to minimize reconstruction loss (Mean Squared Error).
- **Training**:
  - Trained on a dataset of songs with a batch size of 16384 for up to 60 epochs, using early stopping to prevent overfitting.
  - Utilizes GPU acceleration if available.

The system also includes a separate encoder model to map songs directly to the latent space for recommendation purposes.

## Data

The dataset used for training and evaluation is sourced from Spotify and includes:

- **Raw Data**: `spotify_dataset.csv` (1.1GB) - The original dataset containing song information.
- **Pre-processed Data**: `pre-processed-data.csv` (69MB) - Processed numerical and categorical features ready for model input.
- **Latent Space Lookup**: `latent-space-lookup.csv` (239MB) - Stores the latent representations of songs for quick recommendation lookups.
- **Metadata**: JSON files for artists, genres, and emotions, along with normalization parameters and data counts.

## Embedding Layers Information

Embedding layers are crucial for handling categorical data in the model:

- **Artist Embedding**: With a dimension of 100, it captures the unique characteristics of each artist across a large number of artists (as derived from `counts.csv`).
- **Genre Embedding**: With a dimension of 50, it represents various music genres, allowing the model to understand genre similarities.
- **Emotion Embedding**: With a dimension of 25, it encodes emotional attributes associated with songs, enhancing the personalization of recommendations.

## Additional Details

- **Scripts**: The project includes scripts for data preprocessing (`data.py`), model definition and training (`autoencoder.py`), recommendation logic (`Recommender.py`), and visualization (`visualize.py`).
- **Visualizations**: Tools to visualize the latent space and training history are provided in the `visualizations` directory.
- **API and Frontend**: The system is integrated with a backend API (`api` directory) and a Next.js frontend application (`next-app` directory) for user interaction.
- **Model Storage**: Trained models are saved as `autoencoder-model.keras` and `encoder-model.keras` in the `models` directory for reuse.

## Installation and Usage

To run this project locally:

1. Clone the repository.
2. Install dependencies listed in `requirements.txt`.
3. Run data preprocessing scripts if necessary (`scripts/data.py`).
4. Train the model using `scripts/autoencoder.py` or load pre-trained models from the `models` directory.
5. Start the API server and frontend application for user interaction.

## Contributing

Contributions to improve the model, add features, or enhance the user interface are welcome. Please submit pull requests or open issues for discussion.

## License

[Specify your license here, if applicable.]
