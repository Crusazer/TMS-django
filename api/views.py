from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.request import Request

from articles.models import Article
from polls.models import Question, Choice
from shop.models import Category, Product
from . import serializers
from .filters import MinChoiceCountFilter, MaxChoiceCountFilter, MinArticleTextLength
from .pagination import DefaultPagination


# Create your views here.
# ________________________________________________POLLS_________________________________________________________________

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('choices').order_by('id')
    serializer_class = serializers.QuestionSerializer
    pagination_class = DefaultPagination

    filter_backends = [MinChoiceCountFilter, MaxChoiceCountFilter, filters.OrderingFilter, filters.SearchFilter]

    search_fields = ["id", "question_text", "pub_date"]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all().order_by('id')
    serializer_class = serializers.ChoiceSerializer

    filter_backends = [MinChoiceCountFilter, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "choice_text", "question__question_text"]


@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(Question, id=question_id,
                                 status=Question.Status.APPROVED,
                                 pub_date__lte=timezone.now())
    # question = get_object_or_404(Question, id=question_id)
    selected_choice = get_object_or_404(question.choices, id=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)
    # return Response(QuestionSerializer(question).data)


# _______________________________________________ARTICLE________________________________________________________________
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('id')
    serializer_class = serializers.ArticleSerializer
    pagination_class = DefaultPagination

    filter_backends = [filters.SearchFilter, MinArticleTextLength]
    search_fields = ["id", "title", "authors__first_name", "authors__last_name"]


# ________________________________________________SHOP__________________________________________________________________
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("products").order_by('id')
    serializer_class = serializers.CategorySerializer
    pagination_class = DefaultPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "name"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = serializers.ProductSerializer
    pagination_class = DefaultPagination

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "name"]