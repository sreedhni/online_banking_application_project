from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, StaffRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    """
    Generate JWT tokens for the given user.

    Args:
        user: The user instance.

    Returns:
        dict: A dictionary containing refresh and access tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationAPIView(APIView):
    """
    API view for user registration.

    This view handles user registration and generates JWT tokens upon successful registration.
    """
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        """
        Handle POST request for user registration.

        Args:
            request (HttpRequest): The HTTP request object.
            format (str): The format of the request data.

        Returns:
            Response: HTTP response indicating the result of the registration.
        """

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token": token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StaffRegistrationAPIView(APIView):
    """
    API view for staff registration.

    This view handles staff registration and generates JWT tokens upon successful registration.
    """
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        """
        Handle POST request for staff registration.

        Args:
            request (HttpRequest): The HTTP request object.
            format (str): The format of the request data.

        Returns:
            Response: HTTP response indicating the result of the registration.
        """
        serializer = StaffRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token": token, 'msg': 'You are registered as staff'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    """
    API view for user login.
    """

    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        """
        Handle POST request for user login.

        Args:
            request (HttpRequest): The HTTP request object.
            format (str, optional): The format of the request data. Defaults to None.

        Returns:
            Response: HTTP response indicating the result of the login attempt.
        """

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_account_locked():
                    return Response({'errors': {"non_field_errors": ['Account is locked. Please try again later.']}}, status=status.HTTP_403_FORBIDDEN)
                else:
                    token = get_tokens_for_user(user)
                    user.reset_failed_login_attempts()  # Reset failed login attempts upon successful login
                    return Response({"token": token, 'msg': 'Login success'}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                try:
                    user = User.objects.get(email=email)
                    user.increase_failed_login_attempts()  # Increase failed login attempts
                    if user.check_password(password):
                        return Response({'errors': {"non_field_errors": ['Invalid email']}}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'errors': {"non_field_errors": ['Invalid password']}}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    # If the email does not exist, return an error indicating so
                    return Response({'errors': {"non_field_errors": ['Email does not exist']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class LogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    """
    API endpoint to logout a user.

    Users must be authenticated to access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST request to logout a user.

        Returns:
            HTTP 205 RESET CONTENT: Logout successful.
        """
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)