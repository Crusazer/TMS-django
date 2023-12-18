from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Article


# Create your views here.
def articles(request):
    data = {'articles': Article.objects.all()}
    for i in data['articles']:
        print(i.title)
    page = render_to_string('articles.html', context=data)
    return HttpResponse(page)
