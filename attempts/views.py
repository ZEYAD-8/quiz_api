from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quizzes.models import Quiz
from .models import QuizAttempt
from .serializers import QuizReadAttemptSerializer, QuizAttemptSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class AttemptQuizView(APIView):

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        serializer = QuizReadAttemptSerializer(quiz)
        return Response(serializer.data)
    
    def post(self, request, quiz_id):
        user = request.user
        quiz = get_object_or_404(Quiz, id=quiz_id)
        request.data['quiz'] = quiz_id
        request.data['user'] = user.id
        serializer = QuizAttemptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, quiz=quiz)
            return Response({
                'message': 'Quiz attempt recorded successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAttemptsView(APIView):
    def get(self, request):
        user = request.user

        quiz_id = request.query_params.get('quiz_id', None)
        if quiz_id:
            quiz = get_object_or_404(Quiz, id=quiz_id)
            attempts = QuizAttempt.objects.filter(user=user, quiz=quiz)
        else:
            attempts = QuizAttempt.objects.filter(user=user)

        serializer = QuizAttemptSerializer(attempts, many=True)
        return Response(serializer.data)
    


class OthersAttemptsView(APIView):

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)

        self.check_object_permissions(request, quiz)
        serializer = QuizAttemptSerializer(quiz.attempts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
