from rest_framework.permissions import BasePermission

class IsCreator(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_creator

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user
