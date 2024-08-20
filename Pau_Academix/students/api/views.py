from rest_framework import viewsets
from students.api.permissions import IsManager, IsTeacher, IsStudent
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all() 

    def get_permissions(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return [IsAuthenticated(), IsManager()]
        elif self.request.user.groups.filter(name='Teacher').exists():
            return [IsAuthenticated(), IsTeacher()]
        elif self.request.user.groups.filter(name='Student').exists():
            return [IsAuthenticated(), IsStudent()]
        else:
            return [IsAuthenticated()] 

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Student').exists():
            return Student.objects.filter(user=user)
        return super().get_queryset() 
