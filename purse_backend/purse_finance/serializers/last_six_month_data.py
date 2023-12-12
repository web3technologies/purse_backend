from rest_framework import serializers


class LastSixMonthDataSerializer(serializers.Serializer):
    month = serializers.CharField()
    income = serializers.DecimalField(max_digits=50, decimal_places=2)
    expense = serializers.DecimalField(max_digits=50, decimal_places=2)