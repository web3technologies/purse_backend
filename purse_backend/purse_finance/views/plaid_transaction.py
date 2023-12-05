from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from purse_finance.models import PlaidTransaction
from purse_finance.serializers import PlaidTransactionSerializer


class PlaidTransactionViewset(ModelViewSet):
    
    queryset = PlaidTransaction.objects.all()
    serializer_class = PlaidTransactionSerializer
    
    
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(
            plaid_account__id=self.kwargs.get("account_pk"),
            plaid_account__user=self.request.user 
        ).order_by("-date")
        
        

class PlaidTransactionSaveView(APIView):

    def post(self, request, *args, **kwargs):
        transaction_id = request.data.get("transaction_id")
        qs = PlaidTransaction.objects.filter(
            id=transaction_id, 
            plaid_account__user=self.request.user
        )
        if trans := qs.last():
            trans.is_saved = not trans.is_saved
            # b = Budget.objects.last()
            # trans.budget = b
            trans.save(update_fields=["is_saved"])
            return Response(data={"detail": f"{trans.id} updated"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)



