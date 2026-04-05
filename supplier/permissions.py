

from rest_framework import permissions
from rest_framework.response import Response


class SupplierPermission(permissions.BasePermission):
    message = 'access error, you are not a supplier'

    def has_permission(self, request, view):
        if (request.user.is_authenticated and request.user.group == 'S'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):

        return request.user.id == obj.supplier.user_id
