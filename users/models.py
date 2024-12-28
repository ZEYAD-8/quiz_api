from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class UserCustom(AbstractUser):
    email = models.EmailField(unique=True)
    is_creator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_creator', 'is_admin']

    def created_quizzes(self):
        return self.quizzes.all()

    def __str__(self):
        return f"User with ID: {self.id} and email: {self.email}"

