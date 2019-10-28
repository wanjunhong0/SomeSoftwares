import pandas as pd
import numpy as np
from imdb import IMDb
from tqdm import tqdm
import re

# read data
users = pd.read_csv('Data/ml-1m/users.dat', header=None, sep='::', engine='python',
                    names=['userID', 'gender', 'age', 'occupation', 'zipcode'])
movies = pd.read_csv('Data/ml-1m/movies.dat', header=None, sep='::', engine='python',
                     names=['movieID', 'title', 'genres'], encoding='cp850')
ratings = pd.read_csv('Data/ml-1m/ratings.dat', header=None, sep='::', engine='python',
                      names=['userID', 'movieID', 'rating', 'timestamp'])
movies_20m = pd.read_csv('Data/ml-20m/movies.csv')
links = pd.read_csv('Data/ml-20m/links.csv')

# get imdbID from 20m dataset
assert not movies.title.duplicated().any()
movies_in = movies['title'][movies['title'].isin(movies_20m['title'])].tolist()
movies_out = movies['title'][-movies['title'].isin(movies_20m['title'])].tolist()

# drop duplicate title
imdb_in = movies_20m[movies_20m['title'].isin(movies_in)]
duplicated_title = imdb_in[imdb_in.duplicated('title')]['title'].tolist()
for i in duplicated_title:
    movies_in.remove(i)
imdb_in = imdb_in.drop_duplicates('title', keep=False)[['movieId', 'title']]

# fill in imdbID for ml-1m dataset
imdb_in = links[['movieId', 'imdbId']].merge(right=imdb_in, how='inner', on='movieId')
movies = movies.merge(right=imdb_in[['title', 'imdbId']], how='outer', on='title')

# # get movie with only one confirmed IMDb ID
# imdb_out = {}
# for i in tqdm(movies_out):
#     flag = True
#     while flag:
#         try:
#             movie = IMDb().search_movie(i)
#             flag = False
#         except:
#             pass
#     if len(movie) == 1:
#         imdb_out[i] = movie[0].movieID
#
# for i in imdb_out.keys():
#     movies.loc[movies['title'] == i, 'imdbId'] = imdb_out[i]

# drop na
movies = movies.dropna()
movies = movies.rename({'imdbId': 'imdbID'}, axis='columns')
movies['imdbID'] = movies['imdbID'].astype('int')
movies.to_csv('imdb.csv', index=False)

# get movies feature from imdbpy
feature = {}
for i in tqdm(movies['imdbID']):
    flag = True
    while flag:
        try:
            feature[i] = IMDb().get_movie(i)
            if len(feature[i]) > 0:
                flag = False
        except:
            pass


# extract feature from summary
movies['director'] = np.nan
movies['cast'] = np.nan
movies['runtime'] = np.nan
movies['language'] = np.nan
movies['director'] = np.nan
movies['rating_imdb'] = np.nan

for i in tqdm(movies['imdbID']):
    for j in summary[i]:
        if j.split(sep=': ')[0] == 'Director':
            movies.loc[movies['imdbID'] == i, 'director'] \
                = re.sub(r" ?\([^)]+\)", "", j.split(sep=': ')[1][:-1]).replace(', ''', '|')
        if j.split(sep=': ')[0] == 'Cast':
            movies.loc[movies['imdbID'] == i, 'cast'] \
                = re.sub(r" ?\([^)]+\)", "", j.split(sep=': ')[1][:-1]).replace(', ''', '|')
        if j.split(sep=': ')[0] == 'Runtime':
            movies.loc[movies['imdbID'] == i, 'runtime'] \
                = re.sub(r" ?\([^)]+\)", "", j.split(sep=': ')[1][:-1]).replace(', ''', '|')
        if j.split(sep=': ')[0] == 'Country':
            movies.loc[movies['imdbID'] == i, 'country'] \
                = re.sub(r" ?\([^)]+\)", "", j.split(sep=': ')[1][:-1]).replace(', ''', '|')
        if j.split(sep=': ')[0] == 'Language':
            movies.loc[movies['imdbID'] == i, 'language'] \
                = re.sub(r" ?\([^)]+\)", "", j.split(sep=': ')[1][:-1]).replace(', ''', '|')
        if j.split(sep=': ')[0] == 'Rating':
            movies.loc[movies['imdbID'] == i, 'rating_imdb'] \
                = re.sub(r" ?\([^)]+\)", "", j.split(sep=': ')[1][:-1]).replace(', ''', '|')
movies.to_csv('movies.csv', index=False)

movies_na = movies[movies.isnull().any(axis=1)]







