from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    REGEX = r'^[\w.@+-]+\Z'

    username = models.CharField(
        max_length=settings.FIELD_LENGTH,
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(REGEX)],
        verbose_name='Логин'
    )
    email = models.EmailField(
        max_length=settings.EMAIL_LENGTH,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=settings.FIELD_LENGTH,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=settings.FIELD_LENGTH,
        blank=True,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=settings.FIELD_LENGTH,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Пароль'
    )

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username


class Follow(models.Model):
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Читатель'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        ordering = (models.F('author__username'),)
        verbose_name = 'Подписку'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['reader', 'author'],
                name='unique_follow'
            ),
            models.CheckConstraint(
                name='Невозможно подписаться на себя любимого',
                check=~models.Q(author=models.F('reader'))
            ),
        ]

    def __str__(self):
        return f'{self.reader.username} на {self.author.username}'
