from django.urls import path

from . import views

app_name = 'game'

urlpatterns = [
    path('',views.index,name='index'),
    path('game/',views.singlePlayer,name='game'),
    path('getRandomArticles/',views.getRandomArticles,name='getRandomArticles')
]
