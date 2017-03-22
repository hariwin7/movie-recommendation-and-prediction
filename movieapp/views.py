from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd
from movieapp.models import UserProfile,Movie,Ratings
from django.contrib.auth import authenticate,login
from django.db.models import Max
from recommender import recommend,loadmodel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.

def login(request):
	if request.method=='POST':
		username = request.POST['uname']
		password = request.POST['psw']
		user= UserProfile.objects.filter(username=username)
		if user is not None:
			print "exist"
			request.session['uname']=user[0].username
			request.session['userid']=user[0].userid
			userdict={'username':username, 'userid':1}
			print userdict
			return redirect('reco')
			# return render(request,"movieapp/recommendation.html",userdict)
		else:
			print "doesnot exist"




		# return render(request,"movieapp/movie_main.html",{'username':'user'})
	# if UserProfile.objects.get(username=username,password=password):
	# 	print "exist"
	return render(request,"movieapp/login.html")



def reco(request):
	if 'userid' in request.session:
		onlyonce=0
		reco=[]
		disjoint_movies = []

		glob_userid = request.session['userid']
		print "userid",glob_userid
		dat = Movie.objects.all().order_by("-movieid")
		val = Ratings.objects.filter(userid=glob_userid)
		uniq_rated_movieids = set(x.movieid for x in val)
		disjoint_movies=[x for x in dat if x.movieid not in uniq_rated_movieids]
		paginator = Paginator(disjoint_movies, 9)
		page = request.GET.get('page')
		try:
			contacts = paginator.page(page)
		except PageNotAnInteger:
		    # If page is not an integer, deliver first page.
		    contacts = paginator.page(1)
		except EmptyPage:
		    # If page is out of range (e.g. 9999), deliver last page of results.
		    contacts = paginator.page(paginator.num_pages)
		print "enterd reco"
		if request.method=='POST':
			name = request.POST['id']
			rating = request.POST['rat']
			print request.session['userid'],name,rating
			if int(rating)<=5:
				rat = Ratings.objects.filter(userid=glob_userid,movieid=int(name))
				if not rat:
					rate = Ratings(userid=glob_userid,movieid=int(name),rating=int(rating))
					rate.save()
					recomended = recommend(glob_userid)
					for x in recomended:
						reco.append(x['movieid'])
					recdat = Movie.objects.filter(movieid__in=reco)
			context = {'mov':contacts,'rating':rating,'id':int(name),'username':request.session['uname'],'userid':glob_userid,'contacts':contacts,'recommended':recdat}
			print "enterd if"
			return render(request,"movieapp/recommendation.html",context)
		else:
			print "enterd else"
			if onlyonce == 1:
				recomended = recommend(glob_userid)
				for x in recomended:
					reco.append(x['movieid'])
			else:
				recomended = loadmodel(glob_userid)
				for x in recomended:
					reco.append(x['movieid'])
			recdat = Movie.objects.filter(movieid__in=reco)
			print recdat

			context = {'contacts':contacts,'mov':contacts,'username':request.session['uname'],'userid':glob_userid,'recommended':recdat}
			return render(request,"movieapp/recommendation.html",context)
	else:
		return redirect('login')


def pred(request):
	return render(request,"movieapp/prediction.html")

def logout(request):
	if 'userid' in request.session:
		del request.session['userid']
		del request.session['uname']
		return redirect('login')

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
				message = {'msg':"Already a user please try another username"}
				print "already a user"
				return render(request,"movieapp/register.html",message)
			else:
				print maxid['userid__max']
				user = UserProfile(userid=maxid['userid__max']+1,username=name,password=passw)
				user.save()
				return redirect('login')
		else:
			message = {'msg':"One of the passwords does not match"}
			return render(request,"movieapp/register.html",message)

	return render(request,"movieapp/register.html")
