from django.urls import path
from .views import QuizHandlerView, QuizFilterView

urlpatterns = [
    path('', QuizFilterView.as_view(), name='quiz-filter'), # GET

    path('create/', QuizHandlerView.as_view(), name='quiz-create'), # POST
    path('<int:quiz_id>/', QuizHandlerView.as_view(), name='quiz-detail'), # GET, PUT, DELETE

]