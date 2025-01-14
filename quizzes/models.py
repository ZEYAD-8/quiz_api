from django.db import models
from users.models import UserCustom
from categories.models import Category
from questions.models import Question

class Quiz(models.Model):
    class Meta:
        verbose_name_plural = "Quizzes"

    title = models.CharField(max_length=255, default='No title available')
    description = models.TextField(default='No description available', max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(UserCustom, related_name='quizzes', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='quizzes', on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name='quizzes', blank=True)

    def __str__(self):
        return f"Quiz: {self.id} from user: {self.user.id} in category: {self.category.name}"
