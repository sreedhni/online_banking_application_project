from rest_framework import serializers
from .models import OpenAccount,LoanApply,LoanDetail
from Staff.models import AccountType
from .models import Transaction

class LoanApplySerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant_name.name', read_only=True)
    loan_name=serializers.CharField(source='loan_name.loan_type.loan_type',read_only=True)
    class Meta:
        model = LoanApply
        fields = "__all__"
    def validate(self, attrs):
        loan_detail = attrs['loanname']
        loan_amount = attrs['loanAmount']

        if loan_amount > loan_detail.maximum_amount:
            raise serializers.ValidationError("Loan amount exceeds maximum amount allowed")

        return attrs


class DepositeSerializer(serializers.ModelSerializer):
    """
    Serializer for depositing an amount into a user's account.

    This serializer is used to serialize and validate data when depositing an amount into a user's account.

    Attributes:
        username (CharField): Username of the account owner (read-only).
        your_account_number (CharField): Account number of the account where the amount is deposited (read-only).
        total_amount (IntegerField): Total amount in the account after the deposit (read-only).

    Methods:
        create: Creates a new transaction record for the deposit.
    """

    username = serializers.CharField(source='username.username', read_only=True)
    your_account_number = serializers.CharField(source='your_account_number.account_number', read_only=True)
    total_amount = serializers.IntegerField(source='your_account_number.total_amount', read_only=True)

    class Meta:
        model = Transaction
        fields = [ 'deposit_amount', 'username', 'your_account_number', 'total_amount']

    def create(self, validated_data):
        """
        Create a new transaction record for the deposit.

        Args:
            validated_data (dict): Validated data for creating the transaction.

        Returns:
            Transaction: The newly created transaction object.
        """
        # Retrieve the your_account_number instance from validated_data
        your_account_number = validated_data.pop('your_account_number', None)
        # Create the Transaction object with the your_account_number instance
        instance = Transaction.objects.create(your_account_number=your_account_number, **validated_data)
        return instance


class WithdrawSerializer(serializers.Serializer):
    """
    Serializer for withdrawing an amount from a user's account.

    This serializer is used to validate and deserialize data when withdrawing an amount from a user's account.

    Attributes:
        your_account_number (CharField): Account number from which the amount will be withdrawn.
        withdraw_amount (IntegerField): Amount to be withdrawn from the account.
        upi_pin (CharField): UPI PIN for authentication.
        transaction_account_number (CharField): Account number where the withdrawn amount will be transferred.

    Note:
        The UPI PIN is used for authentication purposes to verify the transaction.

    """

    your_account_number = serializers.CharField(max_length=30)
    withdraw_amount = serializers.IntegerField()
    upi_pin = serializers.CharField(max_length=6,write_only=True)
    transaction_account_number = serializers.CharField(max_length=30)





class OpenAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the OpenAccount model.

    This serializer is used to serialize OpenAccount instances, excluding certain fields.

    """
    # Serializer fields
    name = serializers.CharField(source='name.name', read_only=True)  
    # minimum_age = serializers.IntegerField(read_only=True) 
    upi_pin=serializers.IntegerField(write_only=True)

    class Meta:
        model = OpenAccount
        exclude = ('status', 'account_number', 'total_amount')



class MyAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the MyAccount model.

    This serializer is used to serialize MyAccount instances, including all fields.
    """
    recent_deposition = DepositeSerializer(many=True, read_only=True)
    recent_withdrawal = WithdrawSerializer(many=True, read_only=True)  # Corrected spelling of withdrawal
    # Serializer fields
    name = serializers.CharField(source='name.name', read_only=True)
    branch = serializers.StringRelatedField()
    account_type = serializers.StringRelatedField()
    account_category = serializers.StringRelatedField()
    upi_pin = serializers.IntegerField(write_only=True)

    class Meta:
        model = OpenAccount
        fields = "__all__"



class EditAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for editing account details.

    This serializer is used to handle editing account details, such as
    mobile number, date of birth, Aadhar number, PAN card number, and
    related documents. It includes fields for updating the account's
    mobile number, date of birth, Aadhar number, PAN card number, photo,
    PAN card document, Aadhar card document, branch, and account type.

    Attributes:
    - mobile_number (str): The mobile number associated with the account.
    - date_of_birth (date): The date of birth of the account holder.
    - adhar_number (str): The Aadhar number of the account holder.
    - pancard_number (str): The PAN card number of the account holder.
    - photo (image): The photo of the account holder.
    - pancard_document (file): The PAN card document of the account holder.
    - adarcard_document (file): The Aadhar card document of the account holder.
    - branch (int): The branch associated with the account.
    - account_type (int): The type of account associated with the account.

    Methods:
    - Meta: Defines the model and fields used for serialization.

    Example:
    ```python
    serializer = EditAccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    ```
    """
    class Meta:
        model = OpenAccount
        fields = ['mobile_number', 'date_of_birth', 'adhar_number', 'pancard_number', 'photo',
                   'pancard_document', 'adarcard_document', 'branch', 'account_type','age']
        
        def validate(self, attrs):
            account_type = attrs.get('account_type')
            minimum_age = attrs.get('minimum_age')

            if account_type and minimum_age:
                if account_type.minimum_age > minimum_age:
                    raise serializers.ValidationError("Minimum age requirement for this account type is not met.")
        
            return attrs

    # class Meta:
    #     model = OpenAccount
    #     fields = ['mobile_number', 'date_of_birth', 'adhar_number', 'pancard_number', 'photo',
    #               'pancard_document', 'adarcard_document', 'branch', 'account_type']
        






from .models import LoanRepayment

class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = ['id', 'applicant_name', 'loan_application', 'amount_paid', 'payment_date']
        read_only_fields = ['applicant_name', 'payment_date']

    def create(self, validated_data):
        loan_repayment = super().create(validated_data)
        loan_application = loan_repayment.loan_application
        remaining_balance = loan_application.loanAmount - loan_repayment.amount_paid
        loan_application.remaining_balance = remaining_balance
        loan_application.save()
        return loan_repayment
