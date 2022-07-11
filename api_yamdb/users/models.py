from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('admin', 'Administrator'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField('email address')
    role = models.CharField(
        max_length=9,
        choices=USER_ROLES,
        default='user'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user_email'
            )
        ]

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = make_password(None)

        super().save(*args, **kwargs)
