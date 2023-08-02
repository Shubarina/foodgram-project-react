from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        max_length=25,
        unique=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Название блюда'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        verbose_name='Изображение'
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание приготовления блюда'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'

    )
    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избранное'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping'
    )

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок')
