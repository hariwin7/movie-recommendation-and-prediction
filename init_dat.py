# used for initialising the data set
from movieapp.models import UserProfile,Ratings,Movie
import pandas as pd

def initrating(df):
    for uid,mid,rat in zip(df['userId'],df['movieId'],df['rating']):
        Rat=Ratings(userid=uid,movieid=mid,rating=rat)
        Rat.save()
def initmovies(df):
    for mid,tit,gen in zip(df['movieId'],df['title'],df['genres']):
        Mov=Movie(movieid=mid,moviename=tit,genre=gen)
        Mov.save()



if __name__ == '__main__':
    df=pd.read_csv('ratings.csv')
    initrating(df)
