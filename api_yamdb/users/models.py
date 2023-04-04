from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


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
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters, fewer. Letters, digits and @/./+/-/_.'),
        validators=[AbstractUser.username_validator, validate_not_me],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=False, unique=True)

    class Meta:
        constraints = [UniqueConstraint(
            fields=['username', 'email'],
            name='unique_username_email',
        )]

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
