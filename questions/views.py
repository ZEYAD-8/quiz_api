from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated
from users.premissions import IsCreator


class QuestionHandlerView(APIView):

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            print("POST, PUT, DELETE")
            return [IsAuthenticated(), IsCreator()]
        return []

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

    def post(self, request):
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
    def get(self, request, category=None, difficulty=None, ordering=None, limit=None):
        filters = {}

        category = request.query_params.get('category') or category
        if isinstance(category, int):
            filters['category__id'] = category
        if isinstance(category, str):
            filters['category__slug__iexact'] = category
        
        difficulty = request.query_params.get('difficulty') or difficulty
        if isinstance(difficulty, int):
            filters['difficulty'] = difficulty
        if isinstance(difficulty, str):
            difficulty_map = {string: number for number, string in Question.DIFFICULTY_CHOICES}
            filters['difficulty'] = difficulty_map.get(difficulty)

        questions = Question.objects.filter(**filters)

        ordering = request.query_params.get('ordering') or ordering
        if ordering:
            questions = questions.order_by(ordering)

        limit = request.query_params.get('limit') or limit
        if limit and int(limit) > 0:
            questions = questions[:int(limit)]

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionRandomView(APIView):

    def get(self, request, limit=3):
        questions = Question.objects.order_by('?')[:limit]
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

