from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Student').exists() 

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Teacher').exists()

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()
