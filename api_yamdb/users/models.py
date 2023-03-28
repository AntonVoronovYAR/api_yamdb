from django.db import models
from django.contrib.auth.models import AbstractUser


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

    class Meta:
        ordering = ['-date_joined']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='not_me'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
