from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import UserManager


class UserCustomManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


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

    objects = UserCustomManager()

    def created_quizzes(self):
        return self.quizzes.all()
    
    def created_questions(self):
        return self.questions.all()
    
    def create_super_user(self):
        self.is_admin = True
        self.is_staff = True
        self.is_superuser = True
        self.save()

    def __str__(self):
        return f"User with ID: {self.id} and email: {self.email}"


