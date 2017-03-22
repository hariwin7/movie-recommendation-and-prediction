# Recommendation using graphlab
import sqlite3
import graphlab as gl
import os
import pickle

def recommend(userid):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    Datpath = os.path.join(BASE_DIR, 'db.sqlite3')
    print Datpath
    conn = sqlite3.connect(Datpath)
    cur = conn.cursor()

    actions= gl.SFrame.from_sql(conn, "SELECT * FROM movieapp_ratings")

    training_data, validation_data = gl.recommender.util.random_split_by_user(actions, 'userid', 'movieid')
    model = gl.recommender.create(training_data, 'userid', 'movieid')
    results = model.recommend([int(userid)])
    model.save("my_model")
    return results
def loadmodel(userid):
    model = gl.load_model("my_model")
    results = model.recommend([int(userid)])
    return results
