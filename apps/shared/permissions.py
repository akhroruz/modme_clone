from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsTeacher(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(obj, 'teachers') and request.user.teachers.filter(id__in=obj.id).exists():
            return True
        return False


class IsAdministrator(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True

        # user.branch

        return False
