from django.urls import path
from .views import QuizHandlerView, QuizFilterView, QuizSelfAttemptsView, QuizOthersAttemptsView

urlpatterns = [
    path('', QuizFilterView.as_view(), name='quiz-filter'), # GET

    path('create/', QuizHandlerView.as_view(), name='quiz-create'), # POST
    path('<int:quiz_id>/', QuizHandlerView.as_view(), name='quiz-detail'), # GET, PUT, DELETE

    path('<int:quiz_id>/attempts/', QuizSelfAttemptsView.as_view(), name='quiz-attempts'),
    path('<int:quiz_id>/others/', QuizOthersAttemptsView.as_view(), name='quiz-others')
]