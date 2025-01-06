from django.urls import path
from .views import CategoryListView, CategoryDetailView, CategoryQuizView, CategoryQuestionView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<str:identifier>/', CategoryDetailView.as_view(), name='category-detail'),

    path('<str:identifier>/quizzes/', CategoryQuizView.as_view(), name='category-quiz-list'),
    path('<str:identifier>/quizzes/<int:limit>/', CategoryQuizView.as_view(), name='category-quiz-list-limit'),

    path('<str:identifier>/questions/', CategoryQuestionView.as_view(), name='category-question-list'),
    path('<str:identifier>/questions/<int:limit>/', CategoryQuestionView.as_view(), name='category-question-list-limit'),
]
