from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from django.shortcuts import get_object_or_404
from quizzes.serializers import QuizSerializer
from quizzes.serializers import QuestionSerializer

# Create your views here.
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryGenericView(APIView):
    def get_object(self, identifier):
        # it's eiter a digit
        if identifier.isdigit():
            return get_object_or_404(Category, id=identifier)

        # or a slug
        return get_object_or_404(Category, slug__iexact=identifier)

class CategoryDetailView(CategoryGenericView):
    def get(self, request, identifier):
        category = self.get_object(identifier)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryQuizView(CategoryGenericView):
    def get(self, request, identifier, limit=None):
        category = self.get_object(identifier)
        quizzes = category.quizzes.all()
        if limit:
            quizzes = quizzes[:int(limit)]
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryQuestionView(CategoryGenericView):
    def get(self, request, identifier, limit=None):
        category = self.get_object(identifier)
        quizzes = category.questions.all()
        if limit:
            quizzes = quizzes[:int(limit)]
        serializer = QuestionSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
