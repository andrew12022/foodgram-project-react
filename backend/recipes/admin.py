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
    search_fields = (
        'name',
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
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )


class IngredientRecipeInline(admin.StackedInline):
    """Админ модель для управления ингредиентов в рецептах."""
    model = IngredientRecipe
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ модель для рецептов."""
    list_display = (
        'name',
        'text',
        'author',
        'display_tags',
        'display_ingredients',
        'count_of_in_favorites',
        'count_of_in_shopping_cart',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    filter_horizontal = (
        'tags',
    )
    inlines = (
        IngredientRecipeInline,
    )

    @admin.display(description='Теги')
    def display_tags(self, object):
        return ', '.join(
            [tags.name for tags in object.tags.all()]
        )

    @admin.display(description='Ингредиенты')
    def display_ingredients(self, object):
        return ', '.join(
            [ingredients.name for ingredients in object.ingredients.all()]
        )

    @admin.display(description='Количество в избранных')
    def count_of_in_favorites(self, object):
        return object.favorites.count()

    @admin.display(description='Количество в списке покупок')
    def count_of_in_shopping_cart(self, object):
        return object.shopping_carts.count()


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Админ модель для ингредиентов в рецептах"""
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
