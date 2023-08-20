from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingList, Tag)


class IngredientRecipeInLine(admin.TabularInline):
    model = IngredientRecipe
    extra = 4


class TagRecipeInLine(admin.TabularInline):
    model = Recipe.tags.through


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color')
    list_display_links = ('name',)
    inlines = [TagRecipeInLine, ]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('name',)
    list_filter = ('name',)
    inlines = [IngredientRecipeInLine, ]


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'text', 'cooking_time',
                    'pub_date', 'favorite_count')
    list_display_links = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = [IngredientRecipeInLine, TagRecipeInLine]
    exclude = ['tags']

    @admin.display(description='В избранном')
    def favorite_count(self, obj):
        return obj.favorite.count()


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
