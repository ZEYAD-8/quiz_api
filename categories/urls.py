from django.urls import path
from .views import CategoryListView, CategoryHandlerView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'), # GET
    path('create/', CategoryHandlerView.as_view(), name='category-create'), # POST
    path('<str:identifier>/', CategoryHandlerView.as_view(), name='category-detail'), # GET, PUT, DELETE

]
