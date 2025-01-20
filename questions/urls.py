from django.urls import path
from .views import QuestionHandlerView, QuestionFilterView

urlpatterns = [
    path('', QuestionFilterView.as_view(), name='question-filter'), # GET

    path('create/', QuestionHandlerView.as_view(), name='question-create'), # POST
    path('<int:question_id>/', QuestionHandlerView.as_view(), name='question-detail'), # GET, PUT, DELETE

]