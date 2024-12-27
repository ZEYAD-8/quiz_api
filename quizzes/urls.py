from django.urls import path
from .views import QuizCreateView, QuizListView, QuizDetailView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/random/', QuizDetailView.as_view(), name='quiz-random')
]