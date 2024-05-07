from rest_framework import serializers
from account.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Method to create a new user.
        """
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        user = User.objects.create_user(**validated_data, password=password)
        return user

class StaffRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for staff member registration.
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Method to create a new staff member.
        """
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        # Create a staff member instead of a regular user
        user = User.objects.create_staff(**validated_data, password=password)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']
