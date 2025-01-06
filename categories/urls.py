from django.urls import path
from .views import CategoryListView, CategoryDetailView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<str:identifier>/', CategoryDetailView.as_view(), name='category-detail'),
]
