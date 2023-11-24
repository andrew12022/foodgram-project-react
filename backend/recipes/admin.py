from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)

admin.site.empty_value_display = 'Не задано'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
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
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'text',
        'author',
        'added_to_favorites',
        'added_to_shopping_cart',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    filter_horizontal = (
        'tags',
    )

    def added_to_favorites(self, object):
        return object.favorites.count()
    added_to_favorites.short_description = 'Количество в избранных'

    def added_to_shopping_cart(self, object):
        return object.shopping_carts.count()
    added_to_shopping_cart.short_description = 'Количество в списке покупок'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
