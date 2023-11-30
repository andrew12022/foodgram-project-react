from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import Subscriber

from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeSerializer, ShoppingCartSerializer,
                             SubscribeSerializer, TagSerializer,
                             UserSerializer)

User = get_user_model()


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(author_subscribers__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(
            User,
            id=self.kwargs.get('id'),
        )
        if request.method == 'POST':
            if user == author:
                return Response(
                        {'errors': 'На самого себя нельзя подписаться!'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            if Subscriber.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Подписка уже есть!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscriber.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                subscription = Subscriber.objects.get(
                    user=user,
                    author=author,
                )
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Subscriber.DoesNotExist:
                return Response(
                    {'errors': 'Нет такой подписки!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(
            Recipe,
            id=pk,
        )
        data = {
            'user': user.id,
            'recipe': recipe.id
        }
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже есть!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = FavoriteSerializer(
                data=data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                recipe = Favorite.objects.get(
                        user=user,
                        recipe=recipe,
                )
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Favorite.DoesNotExist:
                return Response(
                    {'errors': 'Рецепта нет!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(
            Recipe,
            id=pk,
        )
        data = {
            'user': user.id,
            'recipe': recipe.id
        }
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Рецепт уже есть!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = ShoppingCartSerializer(
                data=data,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                recipe = ShoppingCart.objects.get(
                        user=user,
                        recipe=recipe,
                )
                recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ShoppingCart.DoesNotExist:
                return Response(
                    {'errors': 'Рецепта нет!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
