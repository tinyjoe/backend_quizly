from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    confirmed_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {'password': {'write_only': True}, 'email': {'required': True}}

    def validate_confirmed_password(self, value):
        """
        The function `validate_confirmed_password` compares the password and confirmed password values
        and raises a validation error if they do not match.
        """
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value
    
    def save(self):
        """
        The `save` function creates a new user account with the provided email, username, and password,
        and saves it to the database.
        """
        pw = self.validated_data['password']
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account