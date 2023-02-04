from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoObjectPermissions


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

        if hasattr(obj, 'branch') and user.branch == obj.branch:
            return True

        return False


class CustomDjangoObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

