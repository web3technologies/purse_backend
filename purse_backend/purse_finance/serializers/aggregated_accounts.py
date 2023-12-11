from rest_framework import serializers


class AggregatedAccountSerializer(serializers.Serializer):
    cash = serializers.DecimalField(max_digits=50, decimal_places=2)
    assets = serializers.DecimalField(max_digits=50, decimal_places=2)
    debt = serializers.DecimalField(max_digits=50, decimal_places=2)
