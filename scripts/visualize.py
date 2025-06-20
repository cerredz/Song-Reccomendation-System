from data import load_data
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# Visualize a histogram of a column in the data
def vis_hist(data, column_name):
    values = data[column_name]
    plt.hist(values, bins=20, edgecolor="black")
    plt.xlabel(column_name)
    plt.ylabel("Value")
    plt.savefig(f"../visualizations/histograms/{column_name}")
    plt.close()

# Visualize the correlation matrix between the numerical columns in the data
def vis_corr_matrx(data, column_names):
    corr_matrix_data = data[column_names]
    corr_matrix = corr_matrix_data.corr()
    plt.figure(figsize=(15,15))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
    plt.title(f"Correlation Matrix")
    plt.savefig("../visualizations/heatmaps/correlation-matrix")
    plt.close()

# Visualizes the training history of the model
def plot_training_history(history, save_path="../visualizations/training/training.png"):
    """Plot training and validation loss over epochs"""
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Training History', fontsize=16)
    
    # Plot 1: Training and Validation Loss
    axes[0, 0].plot(history.history['loss'], label='Training Loss', color='blue', linewidth=2)
    axes[0, 0].plot(history.history['val_loss'], label='Validation Loss', color='red', linewidth=2)
    axes[0, 0].set_title('Model Loss')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Loss (MSE)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Training and Validation MSE (same as loss in this case, but good to show)
    axes[0, 1].plot(history.history['mse'], label='Training MSE', color='blue', linewidth=2)
    axes[0, 1].plot(history.history['val_mse'], label='Validation MSE', color='red', linewidth=2)
    axes[0, 1].set_title('Model MSE')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('MSE')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Loss Difference (to spot overfitting)
    loss_diff = [val - train for train, val in zip(history.history['loss'], history.history['val_loss'])]
    axes[1, 0].plot(loss_diff, label='Val Loss - Train Loss', color='green', linewidth=2)
    axes[1, 0].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    axes[1, 0].set_title('Overfitting Check')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Loss Difference')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Learning Rate (if available) or Loss on Log Scale
    axes[1, 1].plot(history.history['loss'], label='Training Loss (Log Scale)', color='blue', linewidth=2)
    axes[1, 1].plot(history.history['val_loss'], label='Validation Loss (Log Scale)', color='red', linewidth=2)
    axes[1, 1].set_yscale('log')
    axes[1, 1].set_title('Loss (Log Scale)')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Loss (Log Scale)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(history.history)
    
# Visualize the latent space to see if we have clusters of data
def visualize_latent_space(encoder_model, test_data, embedding_data_test=None, method='pca', 
                           save_path="../visualizations/latent_space.png"):
    test_num, test_artist, test_genre, test_emotion = test_data
    latent_representation = encoder_model.predict([test_num, test_artist, test_genre, test_emotion])
    
    if method.lower() == "pca":
        reducer = PCA(n_components=2, random_state=42)
        latent_2d = reducer.fit_transform(latent_representation)
        title_suffix = f"(PCA - {reducer.explained_variance_ratio_.sum():.2%} variance)"
    elif method.lower() == "tsne":
        reducer = TSNE(n_components=2, random_state=42)
        latent_2d = reducer.fit_transform(latent_representation)
        title_suffix = "(t-SNE)"

    fig, axis = plt.subplots(1,3, figsize=(18,9))
    fig.suptitle(f'Latent Space Visualization {title_suffix}', fontsize=16)

    # color by genre
    scatter1 = axis[0].scatter(latent_2d[:,0], latent_2d[:,1], c=test_genre.flatten(), cmap="tab10", alpha=.8, s=20)
    axis[0].set_title("Colored by Genre")
    axis[0].set_xlabel("Latent Dimension 1")
    axis[0].set_ylabel("Latent Dimension 2")

    plt.colorbar(scatter1, ax=axis[0], label="Genre ID")

    # color by artist
    scatter2 = axis[1].scatter(latent_2d[:,0], latent_2d[:,1], c=test_artist.flatten(), cmap="viridis", alpha=.8, s=20)
    axis[1].set_title("Colored by Artist")
    axis[1].set_xlabel("Latent Dimension 1")
    axis[1].set_ylabel("Latent Dimension 2")

    plt.colorbar(scatter2, ax=axis[1], label="Artist ID")

    # color by emotion
    scatter3 = axis[2].scatter(latent_2d[:,0], latent_2d[:,1], c=test_emotion.flatten(), cmap="tab10", alpha=.8, s=20)
    axis[2].set_title("Colored by Emotion")
    axis[2].set_xlabel("Latent Dimension 1")
    axis[2].set_ylabel("Latent Dimension 2")

    plt.colorbar(scatter3, ax=axis[2], label="Emotion ID")
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    data = load_data(p_col_names=False, max_rows=50000)
    num_features = [
        "Popularity",
        "Energy",
        "Danceability",
        "Positiveness",
        "Speechiness",
        "Liveness",
        "Acousticness",
        "Instrumentalness",
        "Tempo",
        "Good for Party",
        "Good for Work/Study",
        "Good for Relaxation/Meditation",
        "Good for Exercise",
        "Good for Running",
        "Good for Yoga/Stretching",
        "Good for Driving",
        "Good for Social Gatherings",
        "Good for Morning Routine"
    ]

    for feature in num_features:
        vis_hist(data, feature)

    vis_corr_matrx(data, num_features)

