from django.contrib.auth import get_user_model
from django.db.models import F
# from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Ingredient, Tag, Recipe
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.user_subscribers.filter(author=object).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = UserSerializer(
        read_only=True,
    )
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, object):
        ingredients = object.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredient_recipes__amount'),
        )
        return ingredients

    def get_is_favorited(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=object).exists()

    def get_is_in_shopping_cart(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_carts.filter(recipe=object).exists()
