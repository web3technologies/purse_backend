from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from purse_finance.serializers.crypto_account import CryptoAccountSerializer, CryptoAccount
from purse_async.tasks import (
    retrieve_crypto_account_value_task, 
    retrieve_crypto_account_value_for_user_task
)


class CryptoAccountViewSet(ModelViewSet):

    serializer_class = CryptoAccountSerializer
    queryset = CryptoAccount.objects.all()
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


    @action(
        detail=False,
        methods=["post"],
        url_path="refresh",
        name="refresh crypto account value",
    )
    def refresh_all_account_value(self, request, *args, **kwargs):
        account_id = request.data.get("account_id")
        task_sig = retrieve_crypto_account_value_task.delay(crypto_account_id=account_id)
        return Response(data={"detail": task_sig.id}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        url_path="refresh-all-accounts",
        name="refresh crypto accounts ",
    )
    def refresh_all_account_values(self, request, *args, **kwargs):
        task_sig = retrieve_crypto_account_value_for_user_task.delay(user_id=request.user.id)
        return Response(data={"detail": task_sig.id}, status=status.HTTP_200_OK)
