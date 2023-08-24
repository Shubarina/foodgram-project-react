from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.SMALL_FIELD_LENGTH,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Название тега'
    )
    color = ColorField(
        max_length=settings.SHORT_FIELD_LENGTH,
        unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        max_length=settings.SHORT_FIELD_LENGTH,
        unique=True,
        verbose_name='Слаг тэга'
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.TITLE_LENGTH,
        unique=True,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=settings.SHORT_FIELD_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name} в {self.measurement_unit}'


class Recipe(models.Model):

    REGEX = '.*[a-zA-Z].*'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=settings.TITLE_LENGTH,
        null=False,
        blank=False,
        verbose_name='Название блюда',
        validators=[RegexValidator(
            regex=REGEX,
            message='В названии рецепта совсем нет букв')]
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False,
        verbose_name='Изображение'
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание приготовления'
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
        validators=(MinValueValidator(settings.MIN_COOKING_TIME),
                    MaxValueValidator(settings.MAX_COOKING_TIME)),
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество',
        validators=((MinValueValidator(settings.MIN_QUANTITY),
                    MaxValueValidator(settings.MAX_QUANTITY)))
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Популярные ингредиенты'
        ordering = ('ingredient',)

    def __str__(self):
        return f'{self.amount} {self.ingredient} для {self.recipe}'


class BaseUserRecipeModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')

    class Meta:
        abstract = True


class Favorite(BaseUserRecipeModel):

    class Meta:
        default_related_name = 'favorite'
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избранное'


class ShoppingList(BaseUserRecipeModel):

    class Meta:
        default_related_name = 'shopping'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок')
