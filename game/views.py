from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from game.models import Article
from random import randint,choice,sample
from time import sleep

def index(request):
    return render(request,'index.html')

def singlePlayer(request):
    return render(request,'game.html');

def getRandomArticles(request):
    count = int(request.GET.get('count',1))

    if count > Article.objects.count():
        count = Article.objects.count()


    articles = []

    allArticles = list(Article.objects.all())
    randomArticles = sample(allArticles,count)
    for article in randomArticles:
        articles.append({
            "title":article.title,
            "url":article.url,
            "id":article.id,
            "real":article.real
        })

    return JsonResponse(articles,safe=False) #jsonresponse requires safe to be false to serialize lists
