from rest_framework.permissions import BasePermission

class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_administrator)
    
    
class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_instructor)