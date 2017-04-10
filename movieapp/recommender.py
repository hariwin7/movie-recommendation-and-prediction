# Recommendation using graphlab
import sqlite3
import graphlab as gl
import os
import pickle
from graphlab.toolkits.recommender.util import precision_recall_by_user

def recommend(userid=None):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    Datpath = os.path.join(BASE_DIR, 'db.sqlite3')
    print Datpath
    conn = sqlite3.connect(Datpath)
    cur = conn.cursor()

    actions= gl.SFrame.from_sql(conn, "SELECT * FROM movieapp_ratings")

    training_data, validation_data = gl.recommender.util.random_split_by_user(actions, 'userid', 'movieid')
    # model = gl.item_similarity_recommender.create(training_data, user_id='userid', item_id='movieid', target='rating', similarity_type='pearson')
    model = gl.recommender.create(training_data, 'userid', 'movieid')
    # results = model.recommend([int(userid)])
    if userid:
        results = model.recommend([int(userid)],k=9)
    testrec = model.recommend()
    print precision_recall_by_user(validation_data, testrec, cutoffs=[5, 10])
    model.save("my_model")
    return results
def loadmodel(userid):
    model = gl.load_model("my_model")
    results = model.recommend([int(userid)],k=9)
    return results
