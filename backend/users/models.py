from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Q

from foodgram import constants


class User(AbstractUser):
    """Модель для пользователя."""
    email = models.EmailField(
        max_length=constants.MAX_LENGTH_FIELD_OF_EMAIL,
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_USERS,
        verbose_name='Уникальный юзернейм',
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Ошибка! Проверьте вводимый формат'
            )
        ],
    )
    first_name = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_USERS,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_USERS,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=constants.MAX_LENGTH_FIELDS_OF_USERS,
        verbose_name='Пароль',
        validators=[validate_password],
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'объект "Пользователь"'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Subscriber(models.Model):
    """Модель для подписчика."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='user_subscribers',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author_subscribers',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'объект "Подписчик"'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscriber',
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='user_not_author',
            ),
        ]

    def __str__(self) -> str:
        return (
            f'{self.user} подписался на {self.author}'
        )
