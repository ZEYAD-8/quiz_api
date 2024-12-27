from django.db import models

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255, default='No title available')
    description = models.TextField(default='No description available', max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Quiz: {self.title} with id: {self.id}"


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

    quiz = models.ForeignKey('Quiz', related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES, default=MULTIPLE_CHOICE)
    tf_correct_answer = models.BooleanField(default=False)

    def validate_choices(self):
        choices_count = self.choices.count()
        if choices_count != 4:
            raise ValueError("Each question must have exactly 4 choices.")

    def validate_correct_answer(self):
        correct_count = self.choices.filter(is_correct=True).count()
        if correct_count == 0:
            raise ValueError("At least one choice must be marked as correct.")

    def __str__(self):
        return f"Question with id: {self.id} for quiz with id: {self.quiz.id}"

class MCQ(models.Model):
    question = models.ForeignKey('Question', related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"MCQ choice: {self.text} with id: {self.id} for question: {self.question.text}"

class MatchingPair(models.Model):
    question = models.ForeignKey('Question', related_name='matching_pairs', on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    match = models.CharField(max_length=255)

    def __str__(self):
        return f"Matching Pair: {self.item} -> {self.match} For Question: {self.question.text}"

class OrderingItem(models.Model):
    question = models.ForeignKey('Question', related_name='ordering_items', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"Order item: {self.text} ({self.order}) for question: {self.question.text}"
