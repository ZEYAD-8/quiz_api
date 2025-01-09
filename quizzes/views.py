from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quiz
from .serializers import QuizSerializer
from rest_framework.permissions import IsAuthenticated
from users.premissions import IsCreator

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

    def get(self, request, quiz_id=None):
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

    def post(self, request):
        self.check_permissions(request)
        serializer = QuizSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class QuizFilterView(APIView):

    def get(self, request, category=None, ordering=None, limit=None):
        filters = {}

        category = request.query_params.get('category') or category
        if isinstance(category, int):
            filters['category__id'] = category
        if isinstance(category, str):
            filters['category__slug__iexact'] = category

        quizzes = Quiz.objects.filter(**filters)

        ordering = request.query_params.get('ordering') or ordering
        if ordering:
            quizzes = quizzes.order_by(ordering)

        limit = request.query_params.get('limit') or limit
        if limit and int(limit) > 0:
            quizzes = quizzes[:int(limit)]

        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizRandomView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, limit=1):
        quizzes = Quiz.objects.order_by('?')[:limit]
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

