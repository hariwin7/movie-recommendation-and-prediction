from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.

def index(request):
	df=pd.read_csv("links.csv")
	na=df[df['movieId']<19]
	name=["2054","63","8012","862","949","9603"]
	movieid=[]
	try:
		
		uname= request.POST['uname']
	except:
		uname=""
		
	try:
		rating = request.POST['rat']
	except:
		rating=""
	try:
		idmov = int(request.POST['id'])
	except:
		idmov= None

	for n in na['movieId']:
		movieid.append(int(n))
		
	print type(idmov)
	context={'base':movieid,'uname':uname,'name':name,'rating':rating,'id':idmov}
	return render(request,"movieapp/movie_main.html",context)


def login(request):

	return render(request,"movieapp/login.html")
	return HttpResponse(request.POST['uname'])


def register(request):
	return render(request,"movieapp/register.html")


	