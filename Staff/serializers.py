from rest_framework import serializers
from Customer.models import OpenAccount, LoanApply,AccountBranches,AccountType,LoanDetail

# serializers.py
from rest_framework import serializers
from .models import Account

# serializers.py
from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    account_type=serializers.StringRelatedField()
    class Meta:
        model = Account
        fields = "__all__"



class AccountListSerializer(serializers.ModelSerializer):
    """
    Serializer for the OpenAccount model.
    """
    name = serializers.CharField(source='name.name', read_only=True)  
    branch = serializers.StringRelatedField()
    account_type = serializers.StringRelatedField()
    account_category = serializers.StringRelatedField()

    class Meta:
        model = OpenAccount
        exclude=("upi_pin",)

class AccountStatusChangeSerializer(serializers.Serializer):
    """
    Serializer for changing the status of an account.
    """
    account_id = serializers.IntegerField()
    new_status = serializers.ChoiceField(choices=OpenAccount.STATUS_CHOICES)
    
    def validate_account_id(self, value):
        """
        Validate whether the provided account ID exists.
        """
        try:
            account = OpenAccount.objects.get(id=value)
        except OpenAccount.DoesNotExist:
            raise serializers.ValidationError("Account does not exist")
        return value

    def update(self, instance, validated_data):
        """
        Update the status of the account.
        """
        instance.status = validated_data.get('new_status', instance.status)
        instance.save()
        return instance
    

class LoanDetailSerializer(serializers.ModelSerializer):
    loan_type=serializers.StringRelatedField()
    class Meta:
        model = LoanDetail
        fields = '__all__'

class LoanStatusChangeSerializer(serializers.Serializer):
    """
    Serializer for changing the status of a loan application.
    """
    loan_id = serializers.IntegerField()
    new_status = serializers.ChoiceField(choices=LoanApply.STATUS_CHOICES)

    def validate_loan_id(self, value):
        """
        Validate whether the provided loan ID exists.
        """
        try:
            loan = LoanApply.objects.get(id=value)
        except LoanApply.DoesNotExist:
            raise serializers.ValidationError("Loan does not exist")
        return value

    def update(self, instance, validated_data):
        """
        Update the status of the loan application.
        """
        instance.status = validated_data.get('new_status', instance.status)
        instance.save()
        return instance
