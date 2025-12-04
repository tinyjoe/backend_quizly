from django.urls import path
from .views import RegistrationView, LoginTokenObtainPairView, LogoutTokenDeleteView, CustomTokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutTokenDeleteView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]