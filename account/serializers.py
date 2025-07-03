from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
             'username': {'validators': []}
        }

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error": "The username already exists"})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "The email already exists"})

        if password != confirm_password:
            raise serializers.ValidationError({"error": "The password and confirm password don't match!"})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user




# serializer for login 

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()