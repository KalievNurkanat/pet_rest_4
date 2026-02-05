from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsGuest(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
class OwnerRights(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return  request.user and request.user.is_staff

class NotForAdmin(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff
