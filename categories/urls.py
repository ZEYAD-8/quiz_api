from django.urls import path
from .views import CategoryListView, CategoryQuizView, CategoryQuestionView, CategoryHandlerView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'), # GET
    path('create/', CategoryHandlerView.as_view(), name='category-create'), # POST
    path('<str:identifier>/', CategoryHandlerView.as_view(), name='category-detail'), # GET, PUT, DELETE

    path('<str:identifier>/quizzes/', CategoryQuizView.as_view(), name='category-quiz-list'), # GET
    path('<str:identifier>/quizzes/<int:limit>/', CategoryQuizView.as_view(), name='category-quiz-list-limit'), # GET

    path('<str:identifier>/questions/', CategoryQuestionView.as_view(), name='category-question-list'), # GET
    path('<str:identifier>/questions/<int:limit>/', CategoryQuestionView.as_view(), name='category-question-list-limit'), # GET
]
