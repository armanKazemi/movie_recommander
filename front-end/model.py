import pandas as pd
import numpy as np
from surprise import dump
import warnings
import zipfile
import requests
import os
from tqdm import tqdm


warnings.simplefilter(action='ignore')


def get_data():
    output_directory = './data'
    output_path = os.path.join(output_directory, 'data.zip')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_url = f''
    response = requests.get(file_url, stream=True)

    total_size = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(output_path, 'wb') as file:
        for chunk in response.iter_content(32 * 1024):
            file.write(chunk)
            progress_bar.update(len(chunk))

    while True:
        if os.path.getsize(output_path) == total_size: break

    with zipfile.ZipFile('./data/data.zip', 'r') as zip_ref:
        zip_ref.extractall('./data')


class Model:
    def __init__(self):
        get_data()

        self.C = None
        self.m = None
        self.model = None
        self.indices = pd.read_csv('./data/indices_data.csv', index_col=0).squeeze('columns')
        self.cosine_sim = np.load('./data/cosine_sim_data.npy')
        self.smd = pd.read_pickle('./data/smd_data.pkl')
        self.rating_title_data = pd.read_pickle('./data/rating_data.pkl')
        self.id_map = pd.read_pickle('./data/id_map_data.pkl')
        self.indices_map = pd.read_pickle('./data/indices_map_data.pkl')
        self.svd = dump.load('./data/model_file')[1]

    def weighted_rating(self, x):
        v = x['vote_count']
        R = x['vote_average']
        return (v / (v + self.m) * R) + (self.m / (self.m + v) * self.C)

    def improved_recommendations(self, title, head_num=200):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:26]
        movie_indices = [i[0] for i in sim_scores]

        movies = self.smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year']]
        vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
        self.C = vote_averages.mean()
        self.m = vote_counts.quantile(0.60)
        qualified = movies[
            (movies['vote_count'] >= self.m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
        qualified['vote_count'] = qualified['vote_count'].astype('int')
        qualified['vote_average'] = qualified['vote_average'].astype('int')
        qualified['wr'] = qualified.apply(self.weighted_rating, axis=1)
        qualified = qualified.sort_values('wr', ascending=False).head(head_num)
        return qualified

    def hybrid(self, user_id, title, head_num=10):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[int(idx)]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:26]
        movie_indices = [i[0] for i in sim_scores]

        movies = self.smd.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'id']]
        try:
            movies['est'] = movies['id'].apply(
                lambda x: self.svd.predict(user_id, self.indices_map.loc[x]['movieId']).est)
            movies = movies.sort_values('est', ascending=False)
            return movies.head(head_num)
        except:
            return movies.head(head_num)

    def search(self, text):
        results = [self.smd[self.smd['title'].str.contains(text, case=False)]['title'],
                   # self.smd[self.smd['overview'].str.contains(text, case=False)]['title'],
                   self.smd[self.smd['genres'].apply(lambda x: any(text.lower() in genre.lower() for genre in x))][
                       'title']]
        return results[0].tolist() + results[1].tolist()

    def get_user_top_movies(self, user_id):
        return list(
            self.rating_title_data[self.rating_title_data['userId'] == user_id].sort_values('rating', ascending=False)[
                'title'][:5])

    def user_search(self, user_id):
        movies = self.get_user_top_movies(user_id)
        if len(movies) < 1: return
        result = self.hybrid(user_id, movies[0])
        for i in range(1, len(movies)):
            result = pd.concat([result, self.hybrid(user_id, movies[i])], ignore_index=True)
        return result.sort_values('vote_average', ascending=False)


model = Model()
# res = model.search('dark')
# print(res)

# print()
# res2 = model.improved_recommendations(res[0], 15)
# print(res2)
#
# print()
# res2 = model.hybrid(1, res[0], 15)
# print(res2)

# print(model.user_search(30))
