from django.urls import path
from .views import AttemptQuizView

urlpatterns = [
    path('<int:quiz_id>/', AttemptQuizView.as_view(), name='attempt_quiz'),


]