from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingList, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
    list_display_links = ('name',)


admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('name',)
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


class IngredientRecipeInLine(admin.TabularInline):
    model = IngredientRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'text', 'cooking_time',
                    'pub_date', 'favorite_count')
    list_display_links = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = [IngredientRecipeInLine, ]

    def favorite_count(self, obj):
        return obj.favorite.count()


admin.site.register(Recipe, RecipeAdmin)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'quantity')


admin.site.register(IngredientRecipe, IngredientRecipeAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


admin.site.register(Favorite, FavoriteAdmin)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


admin.site.register(ShoppingList, ShoppingListAdmin)
