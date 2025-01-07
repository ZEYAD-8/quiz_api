from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class UserCustom(AbstractUser):
    email = models.EmailField(unique=True)
    is_creator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=30, unique=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_creator', 'is_admin']

    groups = models.ManyToManyField(
        Group,
        related_name='usercustom_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usercustom_premissions',
        blank=True
    )

    def created_quizzes(self):
        return self.quizzes.all()
    
    def created_questions(self):
        return self.questions.all()

    def __str__(self):
        return f"User with ID: {self.id} and email: {self.email}"

