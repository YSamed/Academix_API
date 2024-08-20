from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from teachers.models import Teacher
from academics.models import Department

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        teacher_group = Group.objects.get(name='Teacher')
        user.groups.add(teacher_group)

        return user



class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id','first_name', 'last_name', 'employee_id', 'user', 'department']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            UserSerializer().update(user, user_data)
        

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

