from rest_framework import permissions
from excersise.models import Sport_Fav


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        if isinstance(obj, Sport_Fav):
            return obj.student == request.user
        return obj.user == request.user
