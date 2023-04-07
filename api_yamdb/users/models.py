from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_not_me(value):
    if value == 'me':
        raise ValidationError('Нельзя использовать "me" как имя пользователя.')


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    password = models.CharField(
        'Пароль',
        max_length=128,
        default=False
    )
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=256,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLE_CHOICES,
        default='user'
    )
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='150 characters, fewer. Letters, digits and @/./+/-/_.',
        validators=[AbstractUser.username_validator, validate_not_me],
    )
    email = models.EmailField('email address', blank=False, unique=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
