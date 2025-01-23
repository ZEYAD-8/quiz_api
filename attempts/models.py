from django.db import models
from quizzes.models import Quiz, Question
from users.models import UserCustom


# Create your models here.
class QuizAttempt(models.Model):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')

    total_questions = models.IntegerField(default=0)
    total_questions_answered = models.IntegerField(default=0)
    total_correct = models.IntegerField(default=0)

    user_score = models.FloatField(default=-1)
    max_score = models.FloatField(default=0)

    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.id}] Attempt by user: [{self.user.id}] on quiz: [{self.quiz.id}]"

class QuestionAttempt(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, related_name='question_attempts', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.JSONField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.id}] QuestionAttempt for QuizAttempt [{self.quiz_attempt.id}]"
