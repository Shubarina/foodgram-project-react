from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import RecipeFilter
from api.mixins import CustomListViewSet
from api.pagination import FoodgramPagination
from api.permissions import AdminAuthorOrReadOnly, AdminOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeGetSerializer, RecipePostSerializer,
                             ShoppingListSerializer, SubscribeSerializer,
                             TagSerializer, UserProfileSerializer)
from api.utils import model_object_create, model_object_delete
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingList, Tag)
from users.models import Follow, User


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка тегов или информации о теге по уникальному идентификатору.
    Для /api/tags/.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка ингредиентов с возможностью поиска по имени
    или информации об ингредиенте по уникальному идентификатору.
    Для /api/ingredients/.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Работа с рецептами - публикация, редактирование и удаление рецепта.
    Получение списка рецептов или информации по конкретной публикации.
    Формирование страницы избранных рецептов и страницы списка покупок.
    Для /api/recipes/.
    """
    queryset = Recipe.objects.all().order_by('-pub_date')
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (AdminAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = FoodgramPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipePostSerializer

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return model_object_create(request, recipe, FavoriteSerializer)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        message = 'Рецепт не добавлен в избранное'
        return model_object_delete(request, recipe, Favorite, message)

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated, ])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        return model_object_create(request, recipe, ShoppingListSerializer)

    @shopping_cart.mapping.delete
    def remove_frome_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        message = 'Рецепт не добавлен в список покупок'
        return model_object_delete(request, recipe, ShoppingList, message)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping__user=user)
        total_result = ingredients.values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
            'ingredient__name').annotate(total=Sum('quantity'))
        shopping_list = []
        for ingredient in total_result:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            total = ingredient['total']
            shopping_list.append(f'\n{name}: {total} {unit}')
        response = HttpResponse(content=shopping_list,
                                content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="My shopping list.txt"'
        return response


class UserSubscribeView(APIView):
    """
    Вьюcет для работы с User по подпискам.
    Для /api/users/id/subscribe/.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        author = get_object_or_404(User, id=id)
        reader = self.request.user.id
        serializer = SubscribeSerializer(data={'author': author.id,
                                               'reader': reader},
                                         context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        author = get_object_or_404(User, id=id)
        reader = self.request.user
        subscription = Follow.objects.filter(reader=reader, author=author)
        if not subscription.exists():
            return Response(
                {'errors': 'Вы не подписаны на автора'},
                status=status.HTTP_400_BAD_REQUEST)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(CustomListViewSet):
    """
    Вьюсет для просмотра своих подписок.
    Для /api/users/subscriptions/.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    pagination_class = FoodgramPagination

    def get_queryset(self):
        return User.objects.filter(following__reader=self.request.user)
