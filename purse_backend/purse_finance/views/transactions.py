from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from purse_finance.serializers.plaid_transaction import PlaidTransaction, PlaidTransactionSerializer



class TransactionListView(APIView):
    def get(self, request):
        qs = PlaidTransaction.objects.filter(plaid_account__user=self.request.user).order_by('-date')
        serialized_data = PlaidTransactionSerializer(qs, many=True)
        
        return Response(data=serialized_data.data, status=status.HTTP_200_OK)


