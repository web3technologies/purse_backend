from rest_framework import serializers


class IncomeExpenseSerializer(serializers.Serializer):
    month = serializers.DateField()
    total_income = serializers.DecimalField(max_digits=100, decimal_places=5, required=False)
    total_expense = serializers.DecimalField(max_digits=100, decimal_places=5, required=False)
