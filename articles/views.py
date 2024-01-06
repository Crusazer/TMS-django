from django.db.models import Count
from django.shortcuts import render, redirect
from .models import Article, Author
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    context = {'articles': Article.objects.all().order_by("title")}
    return render(request, 'articles/index.html', context=context)


def detail(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    votes = article.users.aggregate(count=Count('id'))['count']
    authors = article.authors.all()
    context = {'article': article, 'votes': votes, 'authors': authors}
    return render(request, 'articles/article.html', context)


def like(request, article_id: int):
    article = get_object_or_404(Article, pk=article_id)
    user = article.users.filter(pk=1)
    if user:
        article.users.remove(User.objects.get(pk=1))
    else:
        article.users.add(User.objects.get(pk=1))
    return redirect('articles:article', article_id=article_id)


def author(request, author_id: int):
    author_ = get_object_or_404(Author, pk=author_id)
    articles = author_.articles.all()
    context = {'author': author_, 'articles': articles}
    return render(request, 'articles/author.html', context)
