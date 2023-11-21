from rest_framework.viewsets import ModelViewSet


from purse_finance.models import PlaidTransaction
from purse_finance.serializers import PlaidTransactionSerializer


class PlaidTransactionViewset(ModelViewSet):
    
    queryset = PlaidTransaction.objects.all()
    serializer_class = PlaidTransactionSerializer
    
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(
            plaid_account__id=self.kwargs.get("account_pk"),
            plaid_account__user=self.request.user 
        ).order_by("date")



