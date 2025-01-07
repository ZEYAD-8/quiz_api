from django.urls import path
from .views import QuestionHandlerView, QuestionFilterView, QuestionRandomView

urlpatterns = [
    path('create/', QuestionHandlerView.as_view(), name='question-list'),
    path('<int:question_id>/', QuestionHandlerView.as_view(), name='question-detail'),

    path('random/', QuestionRandomView.as_view(), name='question-random'),
    path('random/<int:limit>/', QuestionRandomView.as_view(), name='question-random'),

    path('', QuestionFilterView.as_view(), name='question-filter'),
    path('<str:category>/', QuestionFilterView.as_view(), name='question-filter-categories'),
    path('<str:category>/<str:difficulty>/', QuestionFilterView.as_view(), name='question-filter-difficulty'),
    path('<str:category>/<str:difficulty>/<str:ordering>/', QuestionFilterView.as_view(), name='question-filter-ordering'),
    path('<str:category>/<str:difficulty>/<str:ordering>/<int:limit>/', QuestionFilterView.as_view(), name='question-filter-limit'),
]