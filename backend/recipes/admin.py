from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)

admin.site.empty_value_display = 'Не задано'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ модель для тегов."""
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ модель для ингредиентов."""
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ модель для рецептов."""
    list_display = (
        'name',
        'text',
        'author',
        'count_of_in_favorites',
        'count_of_in_shopping_cart',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    filter_horizontal = (
        'tags',
    )

    def count_of_in_favorites(self, object):
        return object.favorites.count()
    count_of_in_favorites.short_description = 'Количество в избранных'

    def count_of_in_shopping_cart(self, object):
        return object.shopping_carts.count()
    count_of_in_shopping_cart.short_description = 'Количество в списке покупок'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Админ модель для связи ингредиентов и рецептов."""
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админ модель для избранных рецептов."""
    list_display = (
        'user',
        'recipe',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ модель для списка покупок."""
    list_display = (
        'user',
        'recipe',
    )
