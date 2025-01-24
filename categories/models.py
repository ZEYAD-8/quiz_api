from django.db import models
from django.utils.text import slugify
from users.models import UserCustom

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(UserCustom, related_name='categories', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.id}] {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
