from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    The `CookieJWTAuthentication` class extends `JWTAuthentication` and provides a method to authenticate users using a JWT token stored in a cookie.
    """
    def authenticate(self, request):
        """
        The `authenticate` function checks for an access token in the request cookies, validates it, and
        returns the corresponding user and token if valid.
        """
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        validated_token = self.get_validated_token(token)
        return self.get_user(validated_token), validated_token