from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from articles.models import Article
from polls.models import Question, Choice
from shop.models import Category, Product
from . import serializers


# Create your views here.
# ________________________________________________POLLS_________________________________________________________________

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.prefetch_related('choices')
    serializer_class = serializers.QuestionSerializer
    filter_backends = [filters.SearchFilter]

    search_fields = ["id", "question_text", "pub_date"]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ["id", ""]


@api_view(['POST'])
def choice_vote(request: Request, question_id: int):
    question = get_object_or_404(Question, id=question_id,
                                 status=Question.Status.APPROVED,
                                 pub_date__lte=timezone.now())
    selected_choice = get_object_or_404(question.choices, id=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)
    # return Response(QuestionSerializer(question).data)


# _______________________________________________ARTICLE________________________________________________________________
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = serializers.ArticleSerializer


# ________________________________________________SHOP__________________________________________________________________
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related("products")
    serializer_class = serializers.CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
