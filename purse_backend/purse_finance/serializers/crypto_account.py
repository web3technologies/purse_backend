from rest_framework import serializers

from purse_finance.models import CryptoAccount


class CryptoAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = CryptoAccount
        fields = "__all__"
