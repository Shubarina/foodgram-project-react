from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    REGEX = r'^[\w.@+-]+\Z'

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(REGEX)],
        verbose_name='Логин'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Пароль'
    )

    class Meta:
        ordering = ('id',)
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
        constraints = [
            models.UniqueConstraint(
                fields=['reader', 'author'],
                name='unique_follow'
            )
        ]
