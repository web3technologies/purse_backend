from rest_framework import serializers
from purse_finance.models import Budget


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = "__all__"

