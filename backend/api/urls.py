from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()

v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('tags', TagViewSet, basename='tags')
v1_router.register(
    'ingredients', IngredientViewSet, basename='ingredients'
)

urlpatterns = [
    path('', include(v1_router.urls)),
]