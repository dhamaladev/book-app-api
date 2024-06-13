from app.managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .base import BaseModel


class CustomUser(AbstractBaseUser, BaseModel):
    """custom user model"""

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
    class Meta:
        db_table = 'users'
