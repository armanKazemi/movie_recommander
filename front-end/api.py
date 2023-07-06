from model import *

model = Model()


def get_random_users(num):
    res = []
    ids = list(range(1, 672))
    for i in range(num):
        res.append(f'user_{ids[i]}')
    return res


def text_search(text, m=model):
    return m.search(text)


def movie_search(movie, m=model):
    return m.improved_recommendations(movie)


def user_movie_search(user, movie, m=model):
    userid = user.split('_')[1]
    return m.hybrid(userid, movie)


def user_search(user, m=model):
    userid = user.split('_')[1]
    return m.user_search(userid)
