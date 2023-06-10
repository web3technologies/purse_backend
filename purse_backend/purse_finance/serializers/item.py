from rest_framework import serializers
from purse_finance.models.item import Item


class ItemSerializerReduced(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "id", "institution"

class ItemSerializer(serializers.ModelSerializer):

    accounts = serializers.SerializerMethodField("get_related_accounts")

    class Meta:
        model = Item
        fields = "__all__"

    def get_related_accounts(self, obj):
        return [
            {"id": account.id, "account_id": account.plaid_account_id, "account_type": account.account_type, "name": account.name} 
            for account in obj.plaidaccount_set.all()
        ]