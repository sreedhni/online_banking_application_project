from rest_framework import serializers
from .models import BudgetPlan,Expenses,SavingsGoal

class BudgetPlanSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)  

    """
    Serializer for BudgetPlan model.
    """
    class Meta:
        model = BudgetPlan
        fields = ['category', 'amount','user']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['category', 'amount']


class SavingsGoalSerializer(serializers.ModelSerializer):
    current_amount_id = serializers.PrimaryKeyRelatedField(source='current_amount', read_only=True)

    class Meta:
        model = SavingsGoal
        fields = ['id', 'user', 'name', 'target_amount', 'current_amount_id', 'deadline', 'completed']
        read_only_fields = ['user', 'current_amount_id', 'completed']
