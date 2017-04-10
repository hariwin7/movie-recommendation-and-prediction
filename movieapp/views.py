from django.shortcuts import render,redirect
from django.http import HttpResponse
import pandas as pd
from movieapp.models import UserProfile,Movie,Ratings,Director,Actorone,Actortwo,Actorthree
from django.contrib.auth import authenticate,login
from django.db.models import Max
from recommender import recommend,loadmodel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import pickle
from collections import OrderedDict

# Create your views here.

def login(request):
	if 'userid' in request.session:
		del request.session['userid']
		del request.session['uname']
	if request.method=='POST':
		username = request.POST['uname']
		password = request.POST['psw']
		user= UserProfile.objects.filter(username=username)
		if user is not None and password==user[0].password:
			print "exist"
			request.session['uname']=user[0].username
			request.session['userid']=user[0].userid
			userdict={'username':username, 'userid':1}
			print userdict
			return redirect('reco')
		else:
			errordict = {'error':"username or password incorrect"}
			return render(request,"movieapp/login.html",errordict)

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
			for x in contacts:
				print x.moviename

			context = {'contacts':contacts,'mov':contacts,'username':request.session['uname'],'userid':glob_userid,'recommended':recdat}
			return render(request,"movieapp/recommendation.html",context)
	else:
		return redirect('login')

def search(request):
	if request.method=='GET':
		search=request.GET.get('search')
		print search
		if search:
			dat=Movie.objects.filter(moviename__contains=search)

	context={'mov':dat}
	return render(request,"movieapp/search.html",context)
def rated(request):
	if 'userid' in request.session:
		c=[]
		z=[]
		userid = request.session['userid']
		rated = Ratings.objects.filter(userid=userid)
		print rated
		for x in rated:	#for getting rated movie ids
			c.append(x.movieid)
		movie = Movie.objects.filter(movieid__in=c)
		for x,y in zip(rated,movie): #for creating a list of tuple of rated and movie objects
			z.append((x,y))

		ratdict = {'mov':z,'username':request.session['uname']}
		return render(request,"movieapp/ratedmovies.html",ratdict)

def pred(request):
	actor1 = Actorone.objects.order_by('act_1_name')
	actor2 = Actortwo.objects.order_by('act_2_name')
	actor3 = Actorthree.objects.order_by('act_3_name')
	director = Director.objects.order_by('dirname')
	pred= {'actorone':actor1 , 'actortwo':actor2 ,'actorthree':actor3, 'director':director}
	return render(request,"movieapp/prediction.html",pred)

def predresult(request):
	result=0
	if request.method=="POST":
		act1=request.POST['actor_one']
		act2=request.POST['actor_two']
		act3=request.POST['actor_three']
		direct=request.POST['director']
		budget = request.POST['Invest_amount']
		moviename = request.POST['movie_name']
		a1 = Actorone.objects.get(pk=int(act1))
		a2 = Actortwo.objects.get(pk=int(act2))
		a3 = Actorthree.objects.get(pk=int(act3))
		drctr = Director.objects.get(pk=int(direct))
		d = pd.DataFrame(OrderedDict((('bud',float(budget)),('director_avg_profit', drctr.dir_avg_profit),('director_movie_count',drctr.dir_no_movies),
                  ('actor_1_avg_profit',a1.act_1_avg_profit),('actor_1_movie_count',a1.act_1_no_movies),('actor_2_avg_profit',a2.act_2_avg_profit),
                  ('actor_2_movie_count',a2.act_2_no_movies),('actor_3_avg_profit',a3.act_3_avg_profit), ('actor_3_movie_count',a3.act_3_no_movies))),index=[1])
		pick=open("prediction/prediction.pickle","rb")
		if pick:
			print "loaded pickle"
			regress=pickle.load(pick)
			print regress.predict(d)
			result = regress.predict(d)
	pr=result[0] * 100
	resultdict={'a1':a1.act_1_name,'a2':a2.act_2_name,'a3':a3.act_3_name,'dr':drctr.dirname,'mname':moviename,'bd':budget,'rs':pr}
	return render(request,"movieapp/predresult.html",resultdict)

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
