from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

urlpatterns = [
    url(r'^login.html$',views.login,name="login"),
    url(r'^register.html$', views.register,name="register"),
    url(r'^prediction.html$', views.pred,name="pred"),
    url(r'^recommendation.html$', views.reco, name="reco"),
    url(r'^logout.html$', views.logout, name="logout"),
    url(r'^search.html$', views.search, name="search"),
    url(r'^ratedmovies.html$', views.rated, name="ratedmovies"),
    url(r'^predictionresult.html$', views.predresult, name="predresult"),


]
