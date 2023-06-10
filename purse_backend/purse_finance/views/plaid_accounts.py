from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from purse_async.tasks import retrieve_plaid_account_balance_task
from purse_finance.models import PlaidAccount
from purse_finance.serializers.account import PlaidAccountSerializer


class PlaidAccountsViewset(ModelViewSet):

    queryset = PlaidAccount.objects.all()
    serializer_class = PlaidAccountSerializer
    http_method_names = ["get", "post"] 

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id).order_by("-account_type")

    @action(
        detail=False,
        methods=["post"],
        url_path="refresh",
        name="refresh plaid account balance",
    )
    def refresh_plaid_account_balance(self, request, *args, **kwargs):
        account_id = request.data.get("account_id")
        task_sig = retrieve_plaid_account_balance_task.delay(plaid_account_id=account_id)
        return Response(data={"detail": task_sig.id}, status=status.HTTP_200_OK)
    


