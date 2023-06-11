from rest_framework import viewsets

from purse_finance.models import Budget
from purse_finance.serializers import BudgetSerializer


class BudgetViewset(viewsets.ModelViewSet):
    
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer


    def get_object(self):
        return super().get_object().get(user=self.request.user)


    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

