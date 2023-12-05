from rest_framework import serializers
from purse_finance.models import PlaidTransaction


class PlaidTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaidTransaction
        fields = "__all__"