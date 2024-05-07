from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from Customer.models import OpenAccount,LoanApply
from Customer.serializers import *
from .permissions import IsStaffPermission
from .serializers import AccountListSerializer,AccountStatusChangeSerializer,LoanStatusChangeSerializer
import random
from rest_framework.permissions import IsAdminUser
from django.core.mail import send_mail



class AccountListView(APIView):
    """
    API view for retrieving a list of accounts.

    This view allows staff users to retrieve a list of all accounts.
    """

    permission_classes = [IsAuthenticated, IsStaffPermission]

    def get(self, request):
        """
        Handle GET request to retrieve a list of accounts.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: HTTP response containing the list of accounts.
        """
        accounts = OpenAccount.objects.all()
        serializer = AccountListSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountStatusChangeView(APIView):
    """
    API view for changing the status of an account and sending notifications.

    This view allows staff members to change the status of an account and send
    a notification email to the account holder.

    Authentication:
    - Only authenticated users with staff permissions can access this view.

    Required Payload:
    - account_id: The ID of the account to be modified.
    - new_status: The new status to be assigned to the account.

    Response:
    - If the request is successful, returns the serialized account data with a
      status code of 200.
    - If the account is not found, returns an error response with a status code
      of 404.
    - If the request payload is invalid, returns an error response with a status
      code of 400.

    Email Notification:
    - Sends an email notification to the account holder regarding the change
      in status. If an account number is generated for the first time, it is
      included in the email.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStaffPermission]

    def post(self, request, format=None):
        """
        Handle POST request for changing the status of an account.

        Args:
            request (HttpRequest): The HTTP request object.
            format (str): The format of the request data.

        Returns:
            Response: HTTP response indicating the result of the account status
            change attempt.
        """
        serializer = AccountStatusChangeSerializer(data=request.data)
        if serializer.is_valid():
            account_id = serializer.validated_data.get('account_id')
            new_status = serializer.validated_data.get('new_status')
            try:
                account = OpenAccount.objects.get(id=account_id)
                account.status = new_status
                if not account.account_number:
                    account_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                    account.account_number = account_number
                account.save()
                serialized_account = OpenAccountSerializer(account)

                subject = 'Account Status Change Notification'
                message = f'Your account status has been changed to {new_status}.'
                if not account.account_number:
                    message += f' Your account number is {account_number}.'
                recipient_email = account.name.email
                sender_email = 'your_email@example.com'
                send_mail(subject, message, sender_email, [recipient_email])
                return Response(serialized_account.data, status=status.HTTP_200_OK)
            except OpenAccount.DoesNotExist:
                return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanApplicationListView(APIView):
    """
    API view for retrieving all loan applications.
    
    This view allows staff users to retrieve all loan applications.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStaffPermission]

    def get(self, request, format=None):
        """
        Retrieve all loan applications.

        Returns:
            Response: HTTP response containing serialized loan applications.
        """
        loan_applications = LoanApply.objects.all()
        serializer = LoanApplySerializer(loan_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoanStatusChangeView(APIView):
    """
    API view for changing the status of a loan application.

    This view allows staff users to change the status of a loan application.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsStaffPermission]

    def post(self, request, format=None):
        """
        Handle POST request to change the status of a loan application.

        Args:
            request (HttpRequest): The HTTP request object.
            format (str): The format of the request data.

        Returns:
            Response: HTTP response indicating the result of the status change attempt.
        """
        serializer = LoanStatusChangeSerializer(data=request.data)
        if serializer.is_valid():
            loan_id = serializer.validated_data['loan_id']
            new_status = serializer.validated_data['new_status']
            try:
                loan = LoanApply.objects.get(id=loan_id)
                if loan.status=="Approved":
                    loan.applicant_name.has_loan=True
                    loan.applicant_name.save()



            except LoanApply.DoesNotExist:
                return Response({"error": "Loan does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer.update(loan, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)