import pandas as pd
import numpy as np
from imdb import IMDb
from tqdm import tqdm
import re


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

# get movie with only one confirmed IMDb ID
imdb_out = {}
for i in tqdm(movies_out):
    flag = True
    while flag:
        try:
            movie = IMDb().search_movie(i)
            flag = False
        except:
            pass
    if len(movie) == 1:
        imdb_out[i] = movie[0].movieID

for i in imdb_out.keys():
    movies.loc[movies['title'] == i, 'imdbId'] = imdb_out[i]

movies = movies.dropna()
movies = movies.rename({'imdbId': 'imdbID'}, axis='columns')
movies['imdbID'] = movies['imdbID'].astype('int')
movies.to_csv('imdb.csv', index=False)


movies['director'] = np.nan
movies['writer'] = np.nan
movies['cast'] = np.nan
movies['runtime'] = np.nan
movies['language'] = np.nan
movies['director'] = np.nan
movies['rating_imdb'] = np.nan


for i in tqdm(movies['imdbID']):
    flag = True
    while flag:
        try:
            movie = IMDb().get_movie(i)
            summary = movie.summary().split(sep='\n')[4: -1]
            flag = False
        except:
            pass
    movies.loc[movies['imdbID'] == i, 'director'] = summary[0].split(sep=': ')[1][:-1].replace(', ', '|')
    movies.loc[movies['imdbID'] == i, 'writer'] = summary[1].split(sep=': ')[1][:-1].replace(', ', '|')
    movies.loc[movies['imdbID'] == i, 'cast'] = re.sub(r" ?\([^)]+\)", "", summary[2].
                                                       split(sep=': ')[1][:-1]).replace(', ''', '|')
    movies.loc[movies['imdbID'] == i, 'runtime'] = summary[3].split(sep=': ')[1][:-1]
    movies.loc[movies['imdbID'] == i, 'country'] = summary[4].split(sep=': ')[1][:-1].replace(', ', '|')
    movies.loc[movies['imdbID'] == i, 'language'] = summary[5].split(sep=': ')[1][:-1].replace(', ', '|')
    movies.loc[movies['imdbID'] == i, 'rating_imdb'] = re.sub(r" ?\([^)]+\)", "", summary[6].split(sep=': ')[1][:-1])



