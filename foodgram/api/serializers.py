from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingList, Tag)
from users.models import Follow, User


class CustomDjoserUsersGetSerializer(UserSerializer):
    """
    Сериализатор для Djoser на GET-запрос к эндпоинту /users/ и /users/me/.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(reader=request.user, author=obj).exists()


class CustomDjoserUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для Djoser при регистрации пользователя.
    POST-запрос на эндпоит /users/.
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'password')


class UserFoodSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User базовый.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(reader=request.user, author=obj).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class UserProfileSerializer(UserFoodSerializer):
    """
    Сериализатор для выдачи информации об авторе при подписке на него.
    """
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context['request']
        recipes = Recipe.objects.filter(author=obj)
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return FavoriteRecipeSerializer(recipes,
                                        many=True,
                                        context={'request': request}).data


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра информации о тегах.
    По эндпоинту /tags/ GET-запрос.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра информации по ингредиентам.
    Для эндпоинта /ingredients/, GET-запрос.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeGetSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиентов при просмотре рецепта.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления ингредиентов в рецепт.
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    """
    Cериализатор для рецептов на GET-запрос и выдачу после публикации рецепта.
    """
    author = CustomDjoserUsersGetSerializer(read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeGetSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return ShoppingList.objects.filter(user=request.user,
                                           recipe=obj).exists()


class RecipePostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления/редактирования/удаления рецептов.
    """
    ingredients = IngredientRecipePostSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    image = Base64ImageField(required=False)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time')

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError('нет тегов')
        tag_list = []
        for tag in value:
            if tag in tag_list:
                raise serializers.ValidationError('Этот тег уже выбран')
            tag_list.append(tag)
        return tag_list

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError('Из чего же мы будем готовить?')
        ingredients_list = []
        for ingredient in value:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError('Этот ингредиент уже выбран')
            if ingredient['amount'] == 0:
                raise serializers.ValidationError(
                    'Количество должно быть больше 0')
            ingredients_list.append(ingredient['id'])
        return value

    def validate_cooking_time(self, value):
        if value == 0:
            raise serializers.ValidationError('Добавим хотя бы минутку')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            amount = ingredient['amount']
            ingredient_recipe = IngredientRecipe(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
            ingredients_list.append(ingredient_recipe)
        IngredientRecipe.objects.bulk_create(ingredients_list)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        IngredientRecipe.objects.filter(recipe=instance).delete()
        super().update(instance, validated_data)
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            amount = ingredient['amount']
            ingredient_recipe = IngredientRecipe(
                recipe=instance,
                ingredient=current_ingredient,
                amount=amount
            )
            ingredients_list.append(ingredient_recipe)
        IngredientRecipe.objects.bulk_create(ingredients_list)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context['request']
        return RecipeGetSerializer(instance, context={'request': request}).data


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и удаления подписки на автора.
    """

    class Meta:
        model = Follow
        fields = ('reader', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('reader', 'author'),
                message='Вы уже подписаны на этого автора'
            )
        ]

    def validate(self, data):
        if data['reader'] == data['author']:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context['request']
        return UserProfileSerializer(instance.author,
                                     context={'request': request}).data


class FavoriteRecipeSerializer(RecipeGetSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для избранных рецептов.
    """
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в избранном'
            )
        ]

    def to_representation(self, instance):
        request = self.context['request']
        return FavoriteRecipeSerializer(instance.recipe,
                                        context={'request': request}).data


class ShoppingListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка покупок.
    """
    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в списке покупок'
            )
        ]

    def to_representation(self, instance):
        request = self.context['request']
        return FavoriteRecipeSerializer(instance.recipe,
                                        context={'request': request}).data
