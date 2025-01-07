from django.urls import path
from .views import QuizHandlerView, QuizFilterView, QuizRandomView

urlpatterns = [
    path('', QuizFilterView.as_view(), name='quiz-list'),
    path('<str:category>/', QuizFilterView.as_view(), name='quiz-list-categories'),
    path('<str:category>/<str:ordering>/', QuizFilterView.as_view(), name='quiz-list-ordering'),
    path('<str:category>/<str:ordering>/<int:limit>/', QuizFilterView.as_view(), name='quiz-list-limit'),

    path('create/', QuizHandlerView.as_view(), name='quiz-create'),
    path('<int:quiz_id>/', QuizHandlerView.as_view(), name='quiz-detail'),

    path('random/', QuizRandomView.as_view(), name='quiz-random'),
    path('random/<int:limit>/', QuizRandomView.as_view(), name='quiz-random'),
]