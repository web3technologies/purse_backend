from rest_framework import serializers

from purse_finance.models import PlaidAccount
from purse_finance.serializers import ItemSerializerReduced


class PlaidAccountSerializer(serializers.ModelSerializer):

    item = ItemSerializerReduced()

    class Meta:
        model = PlaidAccount
        fields = "__all__"

