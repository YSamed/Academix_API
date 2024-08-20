from rest_framework import serializers
from django.contrib.auth.models import User, Group
from students.models import Student

from rest_framework import serializers
from django.contrib.auth.models import User
from students.models import Student


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
        return user

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id','first_name', 'last_name', 'student_id', 'user', 'classroom']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', None)

        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            if 'password' in user_data:
                user.set_password(user_data['password'])
            user.save()
        

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.classroom = validated_data.get('classroom', instance.classroom)
        instance.save()
        
        return instance

