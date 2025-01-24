from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotAllowed
from rest_framework.permissions import IsAuthenticated
from users.premissions import IsCreator

# Create your views here.
class CategoryListView(APIView):
    permission_classes = []
    authentication_classes = []
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryGenericView(APIView):
    def get_object(self, identifier):
        # it's eiter a digit (id)
        if identifier.isdigit():
            return get_object_or_404(Category, id=identifier)
        # or a slug
        return get_object_or_404(Category, slug__iexact=identifier)


class CategoryHandlerView(CategoryGenericView):

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated(), IsCreator()]
        return []

    def dispatch(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name

        allowed_methods = {
            "category-create": ["POST"],
            "category-detail": ["GET", "PUT", "DELETE"],
        }

        methods = allowed_methods.get(url_name, [])
        
        if request.method not in methods:
            return HttpResponseNotAllowed(
                permitted_methods=methods, 
                content=f'Method "{request.method}" not allowed.'
            )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, identifier=None):
        category = self.get_object(identifier)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, identifier=None):
        self.check_permissions(request)
        user = request.user
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, identifier):
        self.check_permissions(request)
        category = self.get_object(identifier)
        if category is None:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, category)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, identifier):
        self.check_permissions(request)
        category = self.get_object(identifier)
        if category is None:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(request, category)

        category.delete()
        return Response(
            {"detail": "Category deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
