from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from purse_async.tasks.finance_tasks import (
    retrieve_plaid_account_transactions_task, 
    retrieve_plaid_account_transactions_for_user_task
)
from purse_finance.models import PlaidTransaction
from purse_finance.serializers import PlaidTransactionSerializer


class PlaidTransactionViewset(ModelViewSet):
    
    queryset = PlaidTransaction.objects.all()
    serializer_class = PlaidTransactionSerializer
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset().filter(plaid_account__user=self.request.user)
        if account_id := self.request.query_params.get("account_id"):
            qs = qs.filter(plaid_account__id=account_id)
        return qs.order_by("-date")
   

    @action(
        detail=False,
        methods=["post"],
        url_path="retrieve-transactions",
        name="retrieve plaid transactions",
    )
    def refresh_plaid_account_balance(self, request, *args, **kwargs):
        if account_id := self.request.query_params.get("account_id"):
            task_sig = retrieve_plaid_account_transactions_task.delay(account_id)
        else:
            task_sig = retrieve_plaid_account_transactions_for_user_task.delay(self.request.user.id)
        return Response(data={"detail": task_sig.id}, status=status.HTTP_200_OK)
    

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



