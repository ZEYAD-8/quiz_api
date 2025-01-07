from django.urls import path
from .views import QuizListView, QuizHandlerView
#from .views import QuestionCreateView, QuestionListView, QuestionDetailView
from .views import QuestionDetailView, QuestionFilterView

urlpatterns = [
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/create/', QuizHandlerView.as_view(), name='quiz-create'),
    path('quizzes/<int:quiz_id>/', QuizHandlerView.as_view(), name='quiz-detail'),
    path('quizzes/random/', QuizHandlerView.as_view(), name='quiz-random'),

    # path('quizzes/<int:quiz_id>/questions/', QuestionListView.as_view(), name='question-list'),
    # path('quizzes/<int:quiz_id>/questions/create/', QuestionCreateView.as_view(), name='question-create'),

    path('questions/create/', QuestionDetailView.as_view(), name='question-list'),
    path('questions/<int:question_id>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:question_id>/update/', QuestionDetailView.as_view(), name='question-update'),
    path('questions/<int:question_id>/delete/', QuestionDetailView.as_view(), name='question-delete'),

    path('questions/random/', QuestionDetailView.as_view(), name='question-random'),
    path('questions/random/<int:limit>/', QuestionDetailView.as_view(), name='question-random'),

    path('questions/', QuestionFilterView.as_view(), name='question-filter'),
    path('questions/<str:category>/', QuestionFilterView.as_view(), name='question-filter-categories'),
    path('questions/<str:category>/<str:difficulty>/', QuestionFilterView.as_view(), name='question-filter-difficulty'),
    path('questions/<str:category>/<str:difficulty>/<str:ordering>/', QuestionFilterView.as_view(), name='question-filter-ordering'),
    path('questions/<str:category>/<str:difficulty>/<str:ordering>/<int:limit>/', QuestionFilterView.as_view(), name='question-filter-limit'),
]