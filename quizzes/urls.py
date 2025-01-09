from django.urls import path
from .views import QuizHandlerView, QuizFilterView, QuizRandomView

urlpatterns = [
    path('', QuizFilterView.as_view(), name='quiz-list'), # GET

    path('create/', QuizHandlerView.as_view(), name='quiz-create'), # POST
    path('<int:quiz_id>/', QuizHandlerView.as_view(), name='quiz-detail'), # GET, PUT, DELETE

    path('random/', QuizRandomView.as_view(), name='quiz-random'), # GET
    path('random/<int:limit>/', QuizRandomView.as_view(), name='quiz-random'), # GET
]