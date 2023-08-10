from django_filters import rest_framework as django_filters

from recipes.models import Recipe


class CharFilterInFilter(django_filters.BaseInFilter,
                         django_filters.CharFilter):
    pass


class RecipeFilter(django_filters.FilterSet):
    author__name = django_filters.CharFilter(lookup_expr='icontains')
    tags = CharFilterInFilter(field_name='tags__name', lookup_expr='in')
    is_favorited = django_filters.BooleanFilter(
        method='get_favorite', field_name='is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_shopping', field_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def get_favorite(self, queryset, field_name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_shopping(self, queryset, field_name, value):
        if value:
            return queryset.filter(shopping__user=self.request.user)
        return queryset
