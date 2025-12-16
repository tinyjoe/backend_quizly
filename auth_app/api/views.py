from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    """
    The `RegistrationView` class is an API view for user registration with permission for any user to access.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        This Python function handles POST requests for user registration, validating the data and
        returning appropriate responses.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginTokenObtainPairView(TokenObtainPairView):
    """
    This class is a custom implementation of a token obtain pair view in Django REST framework for handling user login and setting cookies for access and refresh tokens.
    """
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        """
        This function handles the POST request for user login, validates the data, sets cookies for
        access and refresh tokens, and returns a response with user details.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data.get('refresh')
        access = serializer.validated_data.get('access')
        user = serializer.user
        response = Response({'detail': 'Login successfully', 'user': {'id': user.id, 'username': user.username, 'email': user.email}}, status=status.HTTP_200_OK)
        response.set_cookie(key='access_token', value=access, httponly=True, secure=False, samesite="Lax")
        response.set_cookie(key='refresh_token', value=refresh, httponly=True, secure=False, samesite="Lax")
        return response
    
 
class LogoutTokenDeleteView(APIView):
    """
    This class defines a view in a Django REST framework API that handles logging out a user by deleting their access and refresh tokens stored in cookies.
    """
    def post(self, request, *args, **kwargs):
        """
        The function logs out a user by deleting their access and refresh tokens stored in cookies.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None: 
            return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
        

class CustomTokenRefreshView(TokenRefreshView):
    """
    This class extends TokenRefreshView to handle refreshing access tokens using a refresh token stored in a cookie.
    """
    def post(self, request, *args, **kwargs):
        """
        This function refreshes an access token using a provided refresh token and sets a new
        access token as a cookie in the response.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None: 
            return Response({'detail': 'Refresh token not found'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data={'refresh': refresh_token})
        try: 
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'detail': 'Refresh token invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        access_token = serializer.validated_data.get('access')
        response = Response({'detail': 'Token refreshed', 'access': access_token}, status=status.HTTP_200_OK)
        response.set_cookie(key='access_token', value=access_token, httponly=True, secure=True, samesite="Lax")
        return response