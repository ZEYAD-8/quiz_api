from django.urls import path
from .views import AttemptQuizView, UserAttemptsView

urlpatterns = [
    path('', UserAttemptsView.as_view(), name='user_attempts'),
    path('<int:quiz_id>/', AttemptQuizView.as_view(), name='attempt_quiz'),
    path('<int:quiz_id>/submit/', AttemptQuizView.as_view(), name='submit_quiz'),

]