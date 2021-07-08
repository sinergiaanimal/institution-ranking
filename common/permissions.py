from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyPermission(BasePermission):
    """
    Access to all, but for read-only operations.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)
