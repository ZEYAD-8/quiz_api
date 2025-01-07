from django.db import models
from users.models import UserCustom
from categories.models import Category

class Quiz(models.Model):
    title = models.CharField(max_length=255, default='No title available')
    description = models.TextField(default='No description available', max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(UserCustom, related_name='quizzes', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='quizzes', on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question', related_name='quizzes', blank=True)

    def __str__(self):
        return f"Quiz: {self.id} from user: {self.user.id} in category: {self.category.name}"


class Question(models.Model):
    MULTIPLE_CHOICE = 'MC'
    TRUE_FALSE = 'TF'
    MATCHING = 'MT'
    ORDERING = 'OR'

    QUESTION_TYPES = [
        (MULTIPLE_CHOICE, 'Multiple Choice'),
        (TRUE_FALSE, 'True/False'),
        (MATCHING, 'Matching'),
        (ORDERING, 'Ordering'),
    ]

    DIFFICULTY_CHOICES = [
        (0, "Not rated"),
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard"),
    ]

    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default=MULTIPLE_CHOICE)
    tf_correct_answer = models.BooleanField(default=False)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=0)
    explanation = models.TextField(max_length=500, null=True, blank=True)

    user = models.ForeignKey(UserCustom, related_name='questions', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)

    def validate_choices(self):
        if self.question_type == Question.MULTIPLE_CHOICE and \
            (self.choices.count() != 4 or \
                self.choices.filter(is_correct=True).count() != 1):
            return False

        return True

    def __str__(self):
        return f"Question: {self.id}"

class MCQ(models.Model):
    question = models.ForeignKey('Question', related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"MCQ choice: {self.id} for question: {self.question.id}"

class MatchingPair(models.Model):
    question = models.ForeignKey('Question', related_name='matching_pairs', on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    match = models.CharField(max_length=255)

    def __str__(self):
        return f"Matching Pair: {self.id} for Question: {self.question.id}"

class OrderingItem(models.Model):
    question = models.ForeignKey('Question', related_name='ordering_items', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Order item: {self.id} for question: {self.question.id}"
