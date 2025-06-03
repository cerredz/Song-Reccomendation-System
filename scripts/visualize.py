from data import load_data
import matplotlib.pyplot as plt

def vis_hist(data, column_name):
    values = data[column_name]
   
    plt.hist(values, bins=20, edgecolor="black")
    plt.xlabel(column_name)
    plt.ylabel("Value")
    plt.savefig(f"../visualizations/histograms/{column_name}")
    plt.close()


if __name__ == "__main__":
    data = load_data(p_col_names=False, max_rows=50000)
    num_features = ["Popularity", "Energy", "Liveness", "Danceability", "Positiveness", "Speechiness", "Acousticness", "Instrumentalness"]
    for feature in num_features:
        vis_hist(data, feature)


