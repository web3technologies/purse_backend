from rest_framework.viewsets import ModelViewSet


from purse_finance.models import PlaidTransaction
from purse_finance.serializers import PlaidTransactionSerializer


class PlaidTransactionViewset(ModelViewSet):
    
    queryset = PlaidTransaction.objects.all()
    serializer_class = PlaidTransactionSerializer



