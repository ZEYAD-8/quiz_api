from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from users.premissions import IsCreator
from django.http import HttpResponseNotAllowed
from rest_framework.permissions import AllowAny

class QuestionHandlerView(APIView):

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsCreator()]
        return []

    def dispatch(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name

        allowed_methods = {
            "question-create": ["POST"],
            "question-detail": ["GET", "PUT", "DELETE"],
        }

        methods = allowed_methods.get(url_name, [])
        
        if request.method not in methods:
            return HttpResponseNotAllowed(
                permitted_methods=methods, 
                content=f'Method "{request.method}" not allowed.'
            )

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return None

    def get(self, request, question_id=None):
        if question_id is None:
            return Response(
                {"detail": "Question ID not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        question = self.get_object(question_id)
        if question is None:
            return Response(
                {"detail": "Question not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, question_id=None):
        if not request.resolver_match.url_name == 'question-create':
            return Response(
                {"detail": f'Method "{request.method}" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        serializer = QuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, question_id=None):
        question = self.get_object(question_id)
        if question is None:
            return Response(
                {"detail": "Question not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionSerializer(question, data=request.data, context={'request': request})

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


class QuestionFilterView(APIView):
    def get_permissions(self):
        return []

    def get(self, request):
        filters = {}

        category = request.query_params.get('category', None)
        if isinstance(category, int):
            filters['category__id'] = category
        if isinstance(category, str):
            filters['category__slug__iexact'] = category
        
        difficulty = request.query_params.get('difficulty', None)
        if isinstance(difficulty, int):
            filters['difficulty'] = difficulty
        if isinstance(difficulty, str):
            difficulty_map = {string: number for number, string in Question.DIFFICULTY_CHOICES}
            filters['difficulty'] = difficulty_map.get(difficulty)

        question_type = request.query_params.get('type', None)
        if question_type:
            filters['question_type'] = question_type

        questions = Question.objects.filter(**filters)

        ordering = request.query_params.get('ordering', None)
        if ordering:
            questions = questions.order_by(ordering)

        limit = request.query_params.get('limit', 5)
        try:
            limit = int(limit)
        except (ValueError, TypeError):
            return Response(
                {"detail": "Invalid limit value."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if limit <= 0 or limit > 100:
            return Response(
                {"detail": "limit must be between 1 and 100."},
                status=status.HTTP_400_BAD_REQUEST
            )
        questions = questions[:limit]

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
