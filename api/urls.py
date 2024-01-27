from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"questions", views.QuestionViewSet)
router.register(r"choices", views.ChoiceViewSet)

router.register(r"articles", views.ArticleViewSet)

router.register(r"categories", views.CategoryViewSet)
router.register(r"products", views.ProductViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('questions/<int:question_id>/vote', views.choice_vote),
    path("", views.QuestionViewSet.as_view({'get': 'list'}), name="index"),
]
