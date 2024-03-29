from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe_api import views

app_name = 'recipe_api'
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)
router.register('recipe', views.RecipeViewSet)




urlpatterns = [
    path('', include(router.urls)),
]
