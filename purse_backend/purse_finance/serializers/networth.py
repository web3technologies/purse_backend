from rest_framework import serializers
from purse_finance.models import NetWorth


class NetWorthSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetWorth
        fields = "__all__"