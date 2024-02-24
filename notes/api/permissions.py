from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and (obj.user == request.user or request.user.is_superuser)


class NotPrivateOrDontShow(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_private and request.user and request.user != obj.user:
            return False
        return True
