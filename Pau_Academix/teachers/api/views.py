from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from teachers.models import Teacher
from .serializers import TeacherSerializer
from .permissions import IsManager, IsTeacher, IsStudent
from rest_framework.exceptions import PermissionDenied

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Teacher.objects.all()

    def get_permissions(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return [IsAuthenticated(), IsManager()]
        elif user.groups.filter(name='Teacher').exists():
            return [IsAuthenticated(), IsTeacher()]
        elif user.groups.filter(name='Student').exists():
            return [IsAuthenticated(), IsStudent()]
        else:
            return [IsAuthenticated()] 

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Teacher').exists():
            return Teacher.objects.filter(user=user)
        elif user.groups.filter(name='Manager').exists():
            return Teacher.objects.all()
        else:
            return Teacher.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to add new teachers.") 

    def perform_update(self, serializer):
        user = self.request.user
        if user.groups.filter(name='Manager').exists() or (user.groups.filter(name='Teacher').exists() and serializer.instance.user == user):
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update teacher data.") 

    def perform_destroy(self, instance):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete teacher data.")
