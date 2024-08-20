from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from academics.models import Faculty, Department, Class, Subject
from academics.api.permissions import IsManager, IsTeacher, IsStudent
from academics.api.serializers import  FacultySerializer, FacultyLimitedSerializer,DepartmentSerializer, DepartmentLimitedSerializer,ClassSerializer, ClassLimitedSerializer,SubjectSerializer, SubjectLimitedSerializer 


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return FacultySerializer
        else:
            return FacultyLimitedSerializer
        
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsManager()]
        elif self.action == ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Student').exists():  
                return DepartmentLimitedSerializer  
            return DepartmentSerializer  
        else:
            return DepartmentLimitedSerializer  
        
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsManager()]  
        elif self.action in ['list', 'retrieve']:
            return()
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.filter(is_deleted=False)
        
    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name='Student').exists(): 
                return ClassLimitedSerializer
            return ClassSerializer
        return ClassLimitedSerializer
        
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsManager()]  
        elif self.action in ['update', 'partial_update']:
            if self.request.user and (IsManager().has_permission(self.request, self) or IsTeacher().has_permission(self.request, self)):
                return [IsAuthenticated()]  
            else:
                return [IsAuthenticated()] 
        elif self.action in ['list', 'retrieve']:
            return ()  
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name__in=['Teacher', 'Student']).exists():
                return SubjectLimitedSerializer
            return SubjectSerializer
        return SubjectLimitedSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsManager()]  
        elif self.action in ['update', 'partial_update']:
            if self.request.user and (IsManager().has_permission(self.request, self) or IsTeacher().has_permission(self.request, self)):
                return [IsAuthenticated()]  
            else:
                return [IsAuthenticated()] 
        elif self.action in ['list', 'retrieve']:
            return ()  
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()