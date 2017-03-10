from django.shortcuts import render
import pandas as pd

# Create your views here.

def index(request):
	df=pd.read_csv("links.csv")
	na=df[df['movieId']<19]
	name=["2054","63","8012","862","949","9603"]
	base=[]
	for n in na['movieId']:
		base.append('/static/movieapp/images/{}p.jpg'.format(n))
	return render(request,"movieapp/movie_main.html",{'base':base})
