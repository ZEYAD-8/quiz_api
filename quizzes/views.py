from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quiz, Question
from .serializers import QuizSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from users.premissions import IsCreator



class QuestionDetailView(APIView):
    def get_object(self, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return None

    def get(self, request, question_id=None):
        if question_id == None:
            question = Question.objects.order_by('?').first()
        else:
            question = self.get_object(question_id)
            if question is None:
                return Response(
                    {"detail": "Question not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, question_id):
        question = self.get_object(question_id)
        if question is None:
            return Response(
                {"detail": "Question not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionSerializer(question, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id=None):
        question = self.get_object(question_id)
        if question is None:
            return Response(
                {"detail": "Question not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        question.delete()
        return Response(
            {"detail": "Question deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class QuestionRandomView(APIView):
    def get(self, request, limit=None):
        questions = Question.objects.order_by('?')[:limit]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizListView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizHandlerView(APIView):

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            print("POST, PUT, DELETE")
            return [IsAuthenticated(), IsCreator()]
        return []

    def get_object(self, quiz_id):
        try:
            return Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return None

    def post(self, request):
        print("POST")
        self.check_permissions(request)
        serializer = QuizSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, quiz_id):
        if quiz_id == None:
            quiz = Quiz.objects.order_by('?').first()
        else:
            quiz = self.get_object(quiz_id)
            if quiz is None:
                return Response(
                    {"detail": "Quiz not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, quiz_id):
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        if quiz is None:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, quiz)

        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, quiz_id):
        self.check_permissions(request)
        quiz = self.get_object(quiz_id)
        if quiz is None:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, quiz)

        quiz.delete()
        return Response(
            {"detail": "Quiz deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )