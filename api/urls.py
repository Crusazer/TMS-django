from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
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
    path('users/register/', views.UserCreateView.as_view(), name="register"),
    path('users/register/<int:pk>/', views.UserCreateView.as_view(), name="update_user"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
