from django.contrib import admin

from recipes.models import (Favourite, Ingredient, IngredientRecipe, Recipe,
                            Shoppinglist, Tag)

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientRecipe)
admin.site.register(Favourite)
admin.site.register(Shoppinglist)
