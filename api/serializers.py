from articles.models import Article
from polls.models import Question, Choice
from rest_framework import serializers

from shop.models import Category, Product


# ________________________________________________POLLS_________________________________________________________________
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'


# _______________________________________________ARTICLE________________________________________________________________
class ArticleSerializer(serializers.ModelSerializer):
    # authors = ChoiceSerializer(many=True)

    class Meta:
        model = Article
        fields = "__all__"


# ________________________________________________SHOP__________________________________________________________________
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"
