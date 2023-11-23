from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class NameModel(models.Model):
    """Абстрактная модель для Тег, Ингредиент и Рецепт."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )

    class Meta:
        abstract = True


class Tag(NameModel):
    """Модель Тег."""
    color = models.CharField(
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Ошибка! Проверьте вводимый формат',
            )
        ],
        verbose_name='Цветовой код',
        max_length=7,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'объект "Тег"'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(NameModel):
    """Модель Ингредиент."""
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=256,
    )

    class Meta:
        verbose_name = 'объект "Ингредиент"'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Recipe(NameModel):
    """Модель Рецепт."""
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
                1,
                'Минимальное значение = 1',
            )
        ],
        verbose_name='Время приготовления',
    )

    class Meta:
        verbose_name = 'объект "Рецепт"'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    """Промежуточная модель для Ингредиента и Рецепта."""
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
                1,
                'Минимальное значение = 1',
            )
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


class FavouriteAndShoppinglistModel(models.Model):
    """Абстрактная модель для Избранное и Список покупок."""
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


class Favourite(FavouriteAndShoppinglistModel):
    """Модель Избранное."""
    class Meta:
        verbose_name = 'объект "Избранное"'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favourites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self) -> str:
        return (
            f'{self.user} добавил {self.recipe} в Избранное'
        )


class Shoppinglist(FavouriteAndShoppinglistModel):
    """Модель Список покупок."""
    class Meta:
        verbose_name = 'объект "Список покупок"'
        verbose_name_plural = 'Список покупок'
        default_related_name = 'shopping_lists'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_list'
            )
        ]

    def __str__(self) -> str:
        return (
            f'{self.user} добавил {self.recipe} в Список покупок'
        )
