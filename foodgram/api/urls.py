from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, SubscriptionsViewSet,
                    TagViewSet, UserSubscribeView)

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/<int:id>/subscribe/', UserSubscribeView.as_view()),
    path(
        'users/subscriptions/', SubscriptionsViewSet.as_view({'get': 'list'})
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
