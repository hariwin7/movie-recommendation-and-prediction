import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model,svm
from sklearn.cross_validation import train_test_split,cross_val_score
import clean
from collections import defaultdict
from sklearn import preprocessing

from collections import defaultdict
import pickle

def predict_profit(feature_pred=None):

    df = clean.doit()
    df=df[df['title_year']>=1990]
    df.keys()
    m=preprocessing.LabelEncoder()
    u=m.fit_transform(df['content_rating'])
    y=pd.Series(u,index=df.index)
    ya=pd.DataFrame({"Rating":y})
    df=df.join(ya)
    s = df['genres'].str.split('|').apply(pd.Series, 1)
    s=s.fillna('')
    le = defaultdict(preprocessing.LabelEncoder)

    genres_num = s.apply(lambda x: le[x.name].fit_transform(x))
    df=df.join(genres_num)
    feature = df.ix[:,['bud','director_avg_profit','director_movie_count','actor_1_avg_profit','actor_1_movie_count','actor_2_avg_profit','actor_2_movie_count','actor_3_avg_profit','actor_3_movie_count']]#,'title_year',0,1,2,3,4,'Rating']]
    label= df['profit']
    feat_train,feat_test,lab_train,lab_test = train_test_split(feature,label,random_state=1)
    regress = linear_model.LassoLarsCV(cv=10,precompute=False)
    regress.fit(feat_train,lab_train)
    sco=cross_val_score(regress,feat_test,lab_test,cv=10)
    cross_score = sco.mean()
    print "cross validated score:",cross_score
    print "coefficients:",regress.coef_
    print "intercept:",regress.intercept_

    plt.clf()
    plt.scatter(feat_train['actor_1_avg_profit'],lab_train,color='blue',label='training data')
    plt.scatter(feat_test['actor_1_avg_profit'],lab_test,color='red',label='testing data')
    plt.plot(feat_test['actor_1_avg_profit'],regress.predict(feat_test),color='black',linewidth='2')
    plt.xlabel('director_profit')
    plt.ylabel('profit_of_movie')
    plt.show()
    with open("prediction.pickle","wb") as f:
        pickle.dump(regress,f)
    # if predict_profit is not None:
    #     return regress.predict(predict_profit)

if __name__=="__main__":

    pick=open("prediction.pickle","rb")
    if pick:
        print "loaded pickle"
        regress=pickle.load(pick)
    predict_profit()
