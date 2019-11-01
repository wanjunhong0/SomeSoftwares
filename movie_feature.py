import pandas as pd
import numpy as np
from tqdm import tqdm
import re
from imdb import IMDb


feature = pd.read_csv('output/movie_feature_all.csv')
del feature['Unnamed: 0']
movies = pd.read_csv('data/ml-1m/movies.dat', header=None, sep='::', engine='python',
                     names=['movieID', 'title', 'genres'], encoding='cp1252')
movies['title'] = movies['title'].apply(lambda x: re.sub(r" ?\([^)]+\)", "", x))
movies = movies[movies['movieID'].isin(feature['movieId'])]

# get movies feature
# movies['mpaa'] = feature['mpaa']
# movies['runtime'] = feature['runtime'].astype('int')

# get movies feature from imdbpy
imdb = {}
for i in tqdm(feature['imdbMovieId']):
    flag = True
    while flag:
        try:
            imdb[i] = IMDb().get_movie(i)
            if len(imdb[i]) > 0:
                flag = False
        except:
            pass































#
# fa = feature.genres.apply(lambda x: x.strip('[]').replace("'", '').split(','))
# fb = movies.genres.apply(lambda x : x.split("|"))

# actors = pd.read_csv('data/ml-2k/movie_actors.dat', sep='\t')
# movies_2k = pd.read_csv('data/ml-2k/movies.dat', sep='\t', encoding='cp1252')





































