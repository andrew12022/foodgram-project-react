from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Ingredient, Recipe


class IngredientFilter(SearchFilter):
    """Фильтры для ингредиентов."""
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )


class RecipeFilter(filters.FilterSet):
    """Фильтры для рецептов."""
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = filters.NumberFilter(
        method='filter_by_field_name',
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_by_field_name',
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def filter_by_field_name(self, queryset, name, value):
        user = self.request.user
        filters_dict = {
            'is_favorited': 'favorites__user',
            'is_in_shopping_cart': 'shopping_carts__user',
        }
        if value and user.is_authenticated and name in filters_dict:
            filter_param = {filters_dict[name]: user}
            return queryset.filter(**filter_param)
        return queryset
