import pandas as pd
from imdb import IMDb
from tqdm import tqdm


users = pd.read_csv('Data/ml-1m/users.dat', header=None, sep='::', engine='python',
                    names=['userID', 'gender', 'age', 'occupation', 'zipcode'])
movies = pd.read_csv('Data/ml-1m/movies.dat', header=None, sep='::', engine='python',
                     names=['movieID', 'title', 'genres'])
movies_20m = pd.read_csv('Data/ml-20m/movies.csv')
links = pd.read_csv('Data/ml-20m/links.csv')

movies_in = movies['title'][movies['title'].isin(movies_20m['title'])].tolist()
movies_out = movies['title'][-movies['title'].isin(movies_20m['title'])].tolist()

# drop duplicate title names
movies_in = movies_20m[movies_20m['title'].isin(movies_in)]
movies_in = movies_in.drop_duplicates('title', keep=False)[['movieId', 'title']]
imdb_in = links[['movieId', 'imdbId']].merge(right=movies_in, how='inner', on='movieId')
movies = movies.merge(right=imdb_in[['title', 'imdbId']], how='outer', on='title')


imdb_out = {}
for i in tqdm(movies_out):
    movie = IMDb().search_movie(i)
    if len(movie) == 1:
        imdb_out[i] = movie[0].movieID














