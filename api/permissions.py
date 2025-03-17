from rest_framework import permissions

class Admin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

class StaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if  request.user.is_staff:
            return True

class RegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
