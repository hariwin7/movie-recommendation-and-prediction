from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

urlpatterns = [
    url(r'^movie_main', views.index),
    url(r'^login.html$',login,{'template_name':'movieapp/login.html'}),
    url(r'^register.html$', views.register),
    
]
