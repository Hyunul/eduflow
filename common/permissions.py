from rest_framework import permissions

class IsInstructorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['instructor', 'admin']

class IsSubmissionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.role == 'admin'