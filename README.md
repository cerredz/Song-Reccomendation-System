Currently building a song reccomendation system with a neural network, using dataset found at https://www.kaggle.com/datasets/devdope/900k-spotify/data?select=900k+Definitive+Spotify+Dataset.json

Next steps:

- actually reccomend songs
  - map all latent spaces to values in a "map"
  - convert users answers into 117 dimensional array, input into the encoding model to get the latent space
  - get the N most similiar latent spaces using cosine similiarity
  - get the songs using the latent spaces "map"
  - return the song name, artist of that song, genre of that song
