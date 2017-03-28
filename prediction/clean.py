import pandas as pd
import matplotlib.pyplot as plt
import os



def pre(df):

	z=[x.find('Documentary') for x in df['genres']]
	c=[]
	for x in z:
	    if x==0:
	        c.append(False)
	    else:
	        c.append(True)
	df=df[c]
	rem_list = ['color','num_critic_for_reviews','director_facebook_likes','actor_3_facebook_likes',
	       'actor_1_facebook_likes','num_voted_users','cast_total_facebook_likes',
	       'facenumber_in_poster','num_user_for_reviews','actor_2_facebook_likes',
	       'movie_facebook_likes']

	df = df.drop(rem_list,1)
	impbud=df['budget'].mode()
	budget=df['budget'].fillna(impbud)
	impgross=df['gross'].mode()
	gross=df['gross'].fillna(impgross)
	imputed=pd.DataFrame({"bud":budget,"revenue":gross})
	df=df.join(imputed)
	df=df.dropna()
	df=df[df['language']=='English']
	df['profit']=df.apply (lambda row: profit (row),axis=1) #creates a new column profit in df which has the profit of each movie
	#initialize the variables for director profit and gross
	return df


def profit(row): #function that  computes the profit of each movie
    return (row['revenue']-row['bud'])/row['bud']

def compute(df,placeholder): #function to compute all the required attributes for machine learning

	count=[]
	tot_prof=[]
	avg_prof=[]
	top_prof=[]
	tot_gross=[]
	avg_gross=[]

	_name = placeholder + "_name"
	_tot_profit = placeholder + "_total_profit"
	_avg_profit = placeholder + "_avg_profit"
	_count = placeholder + "_movie_count"
	_tot_gross = placeholder +"_tot_gross"
	_avg_gross = placeholder +"_avg_gross"
	_top_profit = placeholder +"_top_profit"



	unique_name= df[_name].unique()#selecting the unique list of director name

	#looping to find director gross(total and average),director profit(total,average and top)
	for name in unique_name:

	    x=df.ix[df[_name]==name]#selecting the movies of each director
	    gross=x['revenue'].sum()#finding sum of gross for  director's movies
	    prof=x['profit'].sum()#finding sum of profit for  director's movies
	    no_mov= (x[_name].count())#counting the number of movies of a director
	    count.append(no_mov)#appending the number of movies to count
	    tot_gross.append(gross)#appending to total_gross list the gross calculated above
	    tot_prof.append(prof)#appending to total_prof list the profit calculated above
	    avg_gross.append(gross/no_mov)#appending to avg_gross list the average gross
	    avg_prof.append(prof/no_mov)#appending to avg_profit list the average profit
	    top_prof.append(x['profit'].max())#appending most profitable movie profit of a director

	#print len(count),",",len(tot_gross),",",len(tot_prof),",",len(avg_gross),",",len(avg_prof),",",len(top_prof)
	#print tot_prof

	    #create a new dataframe with calculated values
	dfdir = pd.DataFrame({_name:unique_name,_tot_profit:tot_prof,_count:count,_tot_gross:tot_gross,_avg_profit:avg_prof,_avg_gross:avg_gross,_top_profit:top_prof})
	csvname = _name+'.csv'
	dfdir.to_csv(csvname)
	df = pd.merge(df,dfdir,on=_name)
	return df

def doit():
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	Datpath = os.path.join(BASE_DIR,"csv/movie_metadata.csv" )
	df = pd.read_csv(Datpath)
	df = pre(df)
	dfdir=compute(df,"director")

	dfact1 = compute(dfdir,"actor_1")

	dfact2 = compute(dfact1,"actor_2")

	dfact3 = compute(dfact2,"actor_3")
	return dfact3


if __name__=="__main__":
	doit()
