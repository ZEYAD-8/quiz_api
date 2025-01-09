from django.urls import path
from .views import QuestionHandlerView, QuestionFilterView, QuestionRandomView

urlpatterns = [
    path('', QuestionFilterView.as_view(), name='question-filter'), # GET

    path('create/', QuestionHandlerView.as_view(), name='question-list'), # POST
    path('<int:question_id>/', QuestionHandlerView.as_view(), name='question-detail'), # GET, PUT, DELETE

    path('random/', QuestionRandomView.as_view(), name='question-random'), # GET
    path('random/<int:limit>/', QuestionRandomView.as_view(), name='question-random'), # GET
]