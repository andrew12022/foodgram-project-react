# Generated by Django 3.2.16 on 2023-11-23 15:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=256, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'объект "Ингредиент"',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение = 1')], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipes', to='recipes.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'объект "Ингредиент в рецепте"',
                'verbose_name_plural': 'Ингредиенты в рецептах',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('image', models.ImageField(upload_to='recipes_images', verbose_name='Картинка')),
                ('text', models.TextField(verbose_name='Текстовое описание')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение = 1')], verbose_name='Время приготовления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='Ингредиенты')),
            ],
            options={
                'verbose_name': 'объект "Рецепт"',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('color', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Ошибка! Проверьте вводимый формат', regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')], verbose_name='Цветовой код')),
                ('slug', models.SlugField(unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'объект "Тег"',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Shoppinglist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_lists', to='recipes.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_lists', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'объект "Список покупок"',
                'verbose_name_plural': 'Список покупок',
                'default_related_name': 'shopping_lists',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipes', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='recipes.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'объект "Избранное"',
                'verbose_name_plural': 'Избранное',
                'default_related_name': 'favourites',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_list'),
        ),
        migrations.AddConstraint(
            model_name='favourite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favourite'),
        ),
    ]
