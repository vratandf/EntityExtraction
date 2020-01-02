from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movies, name='movies'),
    path('joint_movies/', views.joint_movies, name='joint_movies'),
    path('actors/', views.actors, name='actors'),
    path('separation/', views.separation, name='separation'),
    path('graphexp/', views.graphexp, name='graphexp'),
]
