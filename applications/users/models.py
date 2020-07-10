from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                      BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):

    def create_user(self, email, password):

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(
        primary_key=True

    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=False
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return self.email
