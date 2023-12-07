from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipePostSerializer, RecipeReadSerializer,
                             ShoppingCartSerializer, SubscribeSerializer,
                             SubscribeShowSerializer, TagSerializer,
                             UserSerializer)
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscriber

User = get_user_model()


class UserViewSet(UserViewSet):
    """Вьюсет для пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

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
        serializer = SubscribeShowSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(
            User,
            id=self.kwargs.get('id'),
        )
        data = {
            'user': request.user.id,
            'author': author.id
        }
        serializer = SubscribeSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, **kwargs):
        author = get_object_or_404(
            User,
            id=self.kwargs.get('id'),
        )
        try:
            subscription = Subscriber.objects.get(
                user=request.user,
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
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, IngredientFilter)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipePostSerializer

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        try:
            recipe = Recipe.objects.get(
                id=pk,
            )
        except Recipe.DoesNotExist:
            return Response(
                {'errors': 'Рецепта не существует!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe = get_object_or_404(
            Recipe,
            id=pk,
        )
        try:
            recipe = Favorite.objects.get(
                user=request.user,
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
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        try:
            recipe = Recipe.objects.get(
                id=pk,
            )
        except Recipe.DoesNotExist:
            return Response(
                {'errors': 'Рецепта не существует!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            'user': request.user.id,
            'recipe': recipe.id
        }
        serializer = ShoppingCartSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        recipe = get_object_or_404(
            Recipe,
            id=pk,
        )
        try:
            recipe = ShoppingCart.objects.get(
                user=request.user,
                recipe=recipe,
            )
            recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ShoppingCart.DoesNotExist:
            return Response(
                {'errors': 'Рецепта нет!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_carts.exists():
            return Response(
                {'errors': 'Список покупок пуст!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_carts__user=user,
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit',
        ).annotate(amount=Sum('amount'))
        shopping_list = f'Список покупок для пользователя {user.username}:\n\n'
        for idx, ingredient in enumerate(ingredients, start=1):
            shopping_list += (
                f'{idx}. {ingredient["ingredient__name"].capitalize()} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' — {ingredient["amount"]}\n'
            )
        shopping_list += '\nВаш любимый Foodgram\nНе забудьте всё купить!'
        filename = f'{user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
