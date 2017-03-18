from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd
from movieapp.models import UserProfile,Movie,Ratings
from django.contrib.auth import authenticate,login
from django.db.models import Max

# Create your views here.

def index(request):
	# df=pd.read_csv("movies.csv")
	# na=df[df['movieId']<19]
	# name=["2054","63","8012","862","949","9603"]
	# movieid=[]
	# try:
	#
	# 	uname= request.POST['uname']
	# except:
	# 	uname=""
	#
	# try:
	# 	rating = request.POST['rat']
	# except:
	# 	rating=""
	# try:
	# 	idmov = int(request.POST['id'])
	# except:
	# 	idmov= None
	#
	# for n in na['movieId']:
	# 	movieid.append(int(n))
	# print request.POST
	#
	#
	# print type(idmov)
	# context={'base':movieid,'uname':uname,'name':name,'rating':rating,'id':idmov,'mov':df}
	if request.method=='POST':
		name = request.POST['id']
		rating = request.POST['rat']
		print type(int(rating))
		dat = Movie.objects.filter(movieid__lte=20)
		for x in dat:
			print type(x.movieid)
		context = {'mov':dat,'rating':int(rating),'id':int(name)}
		print "enterd if"
		return render(request,"movieapp/movie_main.html",context)
	else:
		print "enterd else"
		dat = Movie.objects.filter(movieid__lte=20)
		context = {'mov':dat}
		return render(request,"movieapp/movie_main.html",context)


def login(request):
	if request.method=='POST':
		username = request.POST['uname']
		password = request.POST['psw']
		user= UserProfile.objects.filter(username=username)
		if user is not None:
			print "exist"
			userdict={'username':username, 'userid':1}
			print userdict
			# return redirect('movie')
			return render(request,"movieapp/recommendation.html",userdict)
		else:
			print "doesnot exist"



		# return render(request,"movieapp/movie_main.html",{'username':'user'})
	# if UserProfile.objects.get(username=username,password=password):
	# 	print "exist"
	return render(request,"movieapp/login.html")



def reco(request):
	if request.method=='POST':
		name = request.POST['id']
		rating = request.POST['rat']
		print type(int(rating))
		dat = Movie.objects.filter(movieid__lte=20)
		for x in dat:
			print type(x.movieid)
		context = {'mov':dat,'rating':int(rating),'id':int(name)}
		print "enterd if"
		return render(request,"movieapp/recommendation.html",context)
	else:
		print "enterd else"
		dat = Movie.objects.filter(movieid__lte=20)
		context = {'mov':dat}
		return render(request,"movieapp/recommendation.html",context)

def pred(request):
	return render(request,"movieapp/prediction.html")


def register(request):
	if request.method=='POST':
		name = request.POST['uname']
		passw = request.POST['psw']
		passw_rpt = request.POST['psw_repeat']
		print name,passw,passw_rpt
		if passw==passw_rpt:
			test = UserProfile.objects.filter(username=name)
			if UserProfile.objects.all():
				maxid = UserProfile.objects.all().aggregate(Max('userid'))
			else:
				maxid = Ratings.objects.all().aggregate(Max('userid'))
			if test:
				print "already a user"
			else:
				print maxid['userid__max']
				user = UserProfile(userid=maxid['userid__max']+1,username=name,password=passw)
				user.save()
				return redirect('login')

	return render(request,"movieapp/register.html")
