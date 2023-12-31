from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from foodgram import constants

User = get_user_model()


class NameModel(models.Model):
    """Абстрактная модель для тегов, ингредиентов и рецептов."""
    name = models.CharField(
        verbose_name='Название',
        max_length=constants.MAX_LENGTH_FIELDS_OF_RECIPES,
    )

    class Meta:
        abstract = True


class Tag(NameModel):
    """Модель для тега."""
    color = models.CharField(
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Ошибка! Проверьте вводимый формат',
            ),
        ],
        verbose_name='Цветовой код',
        max_length=constants.MAX_LENGTH_FIELD_OF_COLOR,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=constants.MAX_LENGTH_FIELDS_OF_RECIPES,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'объект "Тег"'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(NameModel):
    """Модель для ингредиента."""
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=constants.MAX_LENGTH_FIELDS_OF_RECIPES,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'объект "Ингредиент"'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Recipe(NameModel):
    """Модель для рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    image = models.ImageField(
        upload_to='recipes_images',
        verbose_name='Картинка',
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                constants.MIN_VALIDATION_VALUE,
                (
                    'Минимальное значение = '
                    f'{constants.MIN_VALIDATION_VALUE}'
                ),
            ),
            MaxValueValidator(
                constants.MAX_VALIDATION_VALUE_OF_COOKING_TIME,
                (
                    'Максимальное значение = '
                    f'{constants.MAX_VALIDATION_VALUE_OF_COOKING_TIME}'
                ),
            ),
        ],
        verbose_name='Время приготовления',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'объект "Рецепт"'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    """Промежуточная модель для ингредиента и рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_recipes',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient_recipes',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                constants.MIN_VALIDATION_VALUE,
                (
                    'Минимальное значение = '
                    f'{constants.MIN_VALIDATION_VALUE}'
                ),
            ),
            MaxValueValidator(
                constants.MAX_VALIDATION_VALUE_OF_AMOUNT,
                (
                    'Максимальное значение = '
                    f'{constants.MAX_VALIDATION_VALUE_OF_AMOUNT}'
                ),
            ),
        ],
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'объект "Ингредиент в рецепте"'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self) -> str:
        return (
            f'{self.ingredient.name} - {self.amount} '
            f'{self.ingredient.measurement_unit}'
        )


class FavoriteAndShoppingCartModel(models.Model):
    """Абстрактная модель для избранных рецептов и списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True


class Favorite(FavoriteAndShoppingCartModel):
    """Модель для избранных рецептов."""
    class Meta:
        verbose_name = 'объект "Избранное"'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            ),
        ]

    def __str__(self) -> str:
        return (
            f'{self.user} добавил рецепт "{self.recipe}" в Избранное'
        )


class ShoppingCart(FavoriteAndShoppingCartModel):
    """Модель для списка покупок."""
    class Meta:
        verbose_name = 'объект "Список покупок"'
        verbose_name_plural = 'Список покупок'
        default_related_name = 'shopping_carts'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            ),
        ]

    def __str__(self) -> str:
        return (
            f'{self.user} добавил рецепт "{self.recipe}" в Список покупок'
        )
