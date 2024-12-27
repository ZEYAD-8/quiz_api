from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer

class QuizCreateView(APIView):
    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class QuizListView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

class QuizDetailView(APIView):
    def get_object(self, quiz_id):
        try:
            return Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return None

    def get(self, request, quiz_id):
        quiz = self.get_object(quiz_id)
        if quiz is None:
            quiz = Quiz.objects.order_by('?').first()
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def put(self, request, quiz_id):
        quiz = self.get_object(quiz_id)
        if quiz is None:
            return Response({"detail": "Quiz not found."})
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, quiz_id):
        quiz = self.get_object(quiz_id)
        if quiz is None:
            return Response({"detail": "Quiz not found."})
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
