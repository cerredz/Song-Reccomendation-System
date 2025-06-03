from data import load_data
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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

