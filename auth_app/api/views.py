from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LoginTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.get('refresh')
        access = response.get('access')
        response = Response({'detail': 'Login successfully', 'user': {'id': request.user.id, 'username': request.user.username, 'email': request.user.email}}, status=status.HTTP_200_OK)
        response.set_cookie(key='access_token', value=access, httponly=True, secure=True, samesite="Lax")
        response.set_cookie(key='refresh_token', value=refresh, httponly=True, secure=True, samesite="Lax")
        return response
    

class LogoutTokenDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None: 
            return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({'detail': 'Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid.'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
        

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None: 
            return Response({'detail': 'Refresh token not found'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data={'refresh': refresh_token})
        try: 
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'detail': 'Refresh token invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        access_token = serializer.validated_data.get('access_token')
        response = Response({'detail': 'Token refreshed', 'access': access_token}, status=status.HTTP_200_OK)
        response.set_cookie(key='access_token', value=access_token, httponly=True, secure=True, samesite="Lax")
        return response