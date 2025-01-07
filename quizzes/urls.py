from django.urls import path
from .views import QuizHandlerView, QuizRandomView, QuizFilterView
from .views import QuestionHandlerView, QuestionRandomView, QuestionFilterView

urlpatterns = [
    path('quizzes/', QuizFilterView.as_view(), name='quiz-list'),
    path('quizzes/<str:category>/', QuizFilterView.as_view(), name='quiz-list-categories'),
    path('quizzes/<str:category>/<str:ordering>/', QuizFilterView.as_view(), name='quiz-list-ordering'),
    path('quizzes/<str:category>/<str:ordering>/<int:limit>/', QuizFilterView.as_view(), name='quiz-list-limit'),

    path('quizzes/create/', QuizHandlerView.as_view(), name='quiz-create'),
    path('quizzes/<int:quiz_id>/', QuizHandlerView.as_view(), name='quiz-detail'),

    path('questions/create/', QuestionHandlerView.as_view(), name='question-list'),
    path('questions/<int:question_id>/', QuestionHandlerView.as_view(), name='question-detail'),

    path('quizzes/random/', QuizRandomView.as_view(), name='quiz-random'),
    path('quizzes/random/<int:limit>/', QuizRandomView.as_view(), name='quiz-random'),

    path('questions/random/', QuestionRandomView.as_view(), name='question-random'),
    path('questions/random/<int:limit>/', QuestionRandomView.as_view(), name='question-random'),

    path('questions/', QuestionFilterView.as_view(), name='question-filter'),
    path('questions/<str:category>/', QuestionFilterView.as_view(), name='question-filter-categories'),
    path('questions/<str:category>/<str:difficulty>/', QuestionFilterView.as_view(), name='question-filter-difficulty'),
    path('questions/<str:category>/<str:difficulty>/<str:ordering>/', QuestionFilterView.as_view(), name='question-filter-ordering'),
    path('questions/<str:category>/<str:difficulty>/<str:ordering>/<int:limit>/', QuestionFilterView.as_view(), name='question-filter-limit'),
]