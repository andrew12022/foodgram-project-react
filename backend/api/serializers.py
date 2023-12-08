from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.fields import Base64ImageField, Hex2NameColor
from foodgram import constants
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscriber

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользования."""
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

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя создать пользователя с юзернеймом me!'
            )
        return value


class UserSerializer(UserSerializer):
    """Сериализатор пользователя."""
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


class SubscribeShowSerializer(UserSerializer):
    """Сериализатор для просмотра подписок."""
    recipes_count = serializers.ReadOnlyField(source='recipes.count')
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
        )

    def get_recipes(self, object):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = object.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(
            recipes,
            many=True,
            read_only=True,
        )
        return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки."""

    class Meta:
        model = Subscriber
        fields = (
            'id',
            'user',
            'author',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscriber.objects.all(),
                fields=('user', 'author'),
                message='Подписка уже есть!'
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        return SubscribeShowSerializer(
            instance.author,
            context={
                'request': self.context.get('request')
            },
        ).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для связи ингредиентов и рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        error_messages=constants.ERROR_MESSAGE,
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )
    amount = serializers.IntegerField(
        min_value=constants.MIN_VALIDATION_VALUE,
        max_value=constants.MAX_VALIDATION_VALUE_OF_AMOUNT,
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов."""
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = UserSerializer(
        read_only=True,
    )
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='ingredient_recipes',
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

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


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования рецепта."""
    ingredients = IngredientRecipeSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages=constants.ERROR_MESSAGE,
    )
    image = Base64ImageField()
    author = UserSerializer(
        read_only=True,
    )
    cooking_time = serializers.IntegerField(
        min_value=constants.MIN_VALIDATION_VALUE,
        max_value=constants.MAX_VALIDATION_VALUE_OF_COOKING_TIME,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        if not data.get('tags'):
            raise serializers.ValidationError(
                'Теги должны быть указаны!'
            )
        if not data.get('ingredients'):
            raise serializers.ValidationError(
                'Ингредиенты должны быть указаны!'
            )
        return data

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Теги не могут быть пустыми!'
            )
        tags_set = set(value)
        if len(value) != len(tags_set):
            raise serializers.ValidationError(
                'Теги не могут повторяться!'
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Ингредиенты не могут быть пустыми!'
            )
        ingredient_set = {ingredient['id'] for ingredient in value}
        if len(value) != len(ingredient_set):
            raise serializers.ValidationError(
                'Ингредиенты не могут повторяться!'
            )
        return value

    def create_ingredients(self, ingredients, recipe):
        ingredient_list = []
        for ingredient_data in ingredients:
            ingredient_list.append(
                IngredientRecipe(
                    ingredient=ingredient_data.pop('id'),
                    amount=ingredient_data.pop('amount'),
                    recipe=recipe,
                )
            )
        ingredient_list.sort(key=lambda x: x.ingredient.name)
        IngredientRecipe.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            },
        ).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для кратких рецептов."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FavoriteAndShoppingCartSerializer(serializers.ModelSerializer):
    """Общий сериализатор для избранного и списка покупок."""

    class Meta:
        fields = (
            'user',
            'recipe',
        )

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={
                'request': self.context.get('request')
            },
        ).data


class FavoriteSerializer(FavoriteAndShoppingCartSerializer):
    """Сериализатор для избранных рецептов."""

    class Meta(FavoriteAndShoppingCartSerializer.Meta):
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже есть!',
            ),
        ]


class ShoppingCartSerializer(FavoriteAndShoppingCartSerializer):
    """Сериализатор для списка покупок."""

    class Meta(FavoriteAndShoppingCartSerializer.Meta):
        model = ShoppingCart
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже есть!',
            ),
        ]
