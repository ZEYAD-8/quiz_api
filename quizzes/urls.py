from django.urls import path
from .views import QuizCreateView, QuizListView, QuizDetailView
from .views import QuestionCreateView, QuestionListView, QuestionDetailView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/random/', QuizDetailView.as_view(), name='quiz-random'),

    path('quizzes/<int:quiz_id>/questions/', QuestionListView.as_view(), name='question-list'),
    path('quizzes/<int:quiz_id>/questions/create/', QuestionCreateView.as_view(), name='question-create'),
    path('questions/<int:question_id>/', QuestionDetailView.as_view(), name='question-detail'),

]