from django.urls import path
from .views import CategoryListView, CategoryDetailView, CategoryQuizView, CategoryQuestionView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'), # GET
    path('<str:identifier>/', CategoryDetailView.as_view(), name='category-detail'), # GET

    path('<str:identifier>/quizzes/', CategoryQuizView.as_view(), name='category-quiz-list'), # GET
    path('<str:identifier>/quizzes/<int:limit>/', CategoryQuizView.as_view(), name='category-quiz-list-limit'), # GET

    path('<str:identifier>/questions/', CategoryQuestionView.as_view(), name='category-question-list'), # GET
    path('<str:identifier>/questions/<int:limit>/', CategoryQuestionView.as_view(), name='category-question-list-limit'), # GET
]
