from rest_framework.views import APIView
from rest_framework.response import Response
from quizzes.models import Quiz
from .serializers import QuizReadAttemptSerializer

# Create your views here.
class AttemptQuizView(APIView):

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        serializer = QuizReadAttemptSerializer(quiz)
        return Response(serializer.data)
    

