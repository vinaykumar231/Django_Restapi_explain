from rest_framework import serializers
from .models import AriyanspropertiesUser
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AriyanspropertiesUser
        fields = ['user_id', 'user_name', 'user_email', 'user_type', 'phone_no', 'created_on']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AriyanspropertiesUser
        fields = ['user_name', 'user_email', 'user_password', 'user_type', 'phone_no']

    def create(self, validated_data):
        """Hash the password before saving"""
        validated_data['user_password'] = make_password(validated_data['user_password'])  # Hashing password
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    user_password = serializers.CharField(write_only=True)
