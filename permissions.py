from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'admin')

class IsAuthenticatedUser(BasePermission):
    """
    Allows access to authenticated users with any role (admin, employee, or user).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.role in ['admin', 'employee', 'user'])
