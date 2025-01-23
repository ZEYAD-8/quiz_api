from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quiz
from .serializers import QuizSerializer
from rest_framework.permissions import IsAuthenticated
from users.premissions import IsCreator
from django.http import HttpResponseNotAllowed


class QuizHandlerView(APIView):

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsCreator()]
        return []

    def get_object(self, quiz_id):
        try:
            return Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return None

    def dispatch(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name

        allowed_methods = {
            "quiz-create": ["POST"],
            "quiz-detail": ["GET", "PUT", "DELETE"],
        }

        methods = allowed_methods.get(url_name, [])
        if request.method not in methods:
            return HttpResponseNotAllowed(
                permitted_methods=methods,
                content=f'Method "{request.method}" not allowed.'
            )

        return super().dispatch(request, *args, **kwargs)

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

    def post(self, request, quiz_id=None):
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
    def get_permissions(self):
        return []

    def get(self, request):
        filters = {}

        category = request.query_params.get('category', None)
        if isinstance(category, int):
            filters['category__id'] = category
        if isinstance(category, str):
            filters['category__slug__iexact'] = category

        quizzes = Quiz.objects.filter(**filters)

        ordering = request.query_params.get('ordering', None)
        if ordering:
            quizzes = quizzes.order_by(ordering)
        else:
            quizzes = quizzes.order_by('?')

        limit = request.query_params.get('limit', 1)
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            return Response(
                {"detail": "Invalid limit value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if limit <= 0 or limit > 10:
            return Response(
                {"detail": "limit must be between 1 and 10."},
                status=status.HTTP_400_BAD_REQUEST
            )
        quizzes = quizzes[:limit]
    
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from attempts.serializers import QuizAttemptSerializer
class QuizSelfAttemptsView(APIView):

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        if quiz is None:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        user = request.user
        attempts = quiz.attempts.filter(user=user)
        serializer = QuizAttemptSerializer(attempts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class QuizOthersAttemptsView(APIView):

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(id=quiz_id)
        if quiz is None:
            return Response(
                {"detail": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        self.check_object_permissions(request, quiz)
        serializer = QuizAttemptSerializer(quiz.attempts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
