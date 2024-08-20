from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def validate(self, attrs):
        # Doğrulama işlemi burada yapılabilir, ancak genellikle JWT token'larının doğruluğu backend tarafından yapılır.
        # Bu yüzden burada sadece token'ları alıyoruz ve dönüyoruz.
        refresh = attrs.get('refresh')
        access = attrs.get('access')
        return {
            'refresh': refresh,
            'access': access
        }