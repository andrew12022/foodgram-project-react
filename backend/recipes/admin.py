from django.contrib import admin

from recipes.models import (Favourite, Ingredient, IngredientRecipe, Recipe,
                            Shoppinglist, Tag)

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
        'added_to_shopping_list',
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
        return object.favourites.count()
    added_to_favorites.short_description = 'Количество в избранных'

    def added_to_shopping_list(self, object):
        return object.shopping_lists.count()
    added_to_shopping_list.short_description = 'Количество в списке покупок'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(Shoppinglist)
class ShoppinglistAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
