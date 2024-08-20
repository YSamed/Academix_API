from rest_framework import serializers
from academics.models import Faculty, Department, Class, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SubjectLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class ClassLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['department', 'name']
     
class DepartmentSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'

class DepartmentLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

class FacultySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    class Meta:
        model = Faculty
        fields = '__all__'

class FacultyLimitedSerializer(serializers.ModelSerializer):
    departments = DepartmentLimitedSerializer(many= True, read_only=True)
    class Meta:
        model = Faculty
        fields = ['name' ,'departments']

