# permissions.py

from rest_framework.permissions import BasePermission

class IsStaffPermission(BasePermission):
    """
    Custom permission to only allow staff members to access a view.
    """

    def has_permission(self, request, view):
        """
        Check if the user is a staff member.
        """
        return request.user and request.user.is_staff


