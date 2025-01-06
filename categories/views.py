from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryDetailView(APIView):
    def get_object(self, identifier):
        # if the identifier is a digit, then it's an id
        if identifier.isdigit():
            return get_object_or_404(Category, id=identifier)

        # otherwise, it's a slug
        return get_object_or_404(Category, slug__iexact=identifier)

    def get(self, request, identifier):
        category = self.get_object(identifier)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
