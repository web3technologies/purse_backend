import logging

from django.db import transaction
from django.conf import settings
from django.db.utils import IntegrityError


from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.item_get_request import ItemGetRequest

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from purse_core.client import plaid_client
from purse_async.tasks import retrieve_plaid_account_data_for_user_task
from purse_finance.models import Item, PlaidAccount
from purse_finance.serializers.item import ItemSerializer


logger = logging.getLogger(__name__)


class ItemViewset(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    http_method_names = ["get", "post", "head", "patch", "delete"]

    serializer_classes = {
        'list': ItemSerializer,
        'retrieve': ItemSerializer,
        "create": ItemSerializer,
        "update": ItemSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    def _create_accounts(self, item_id, accounts):

        for account in accounts:
            print(f"{account['name'].upper()} --  {account['id']}")
            try:
                plaid_account, created = PlaidAccount.objects.get_or_create(
                    name=account["name"].upper(),
                    item_id=item_id,
                    user=self.request.user,
                    defaults={
                        "plaid_account_id": account["id"],
                        "account_type": account["type"].upper(),
                    }
                )
                if not created and plaid_account.plaid_account_id != account["id"]:     #Prevent duplicate account creation, instead change the id
                    print("not created and doesnt match id")
                    plaid_account.plaid_account_id=account["id"]
                    plaid_account.status = settings.ACTIVE
                    plaid_account.save(update_fields=["plaid_account_id", "status"])
                else:
                    print("account found updating status")
                    plaid_account.status = settings.ACTIVE
                    plaid_account.save(update_fields=["status"])
                    
            except IntegrityError as exc:
                print("integ error")
                account_found = PlaidAccount.objects.get(plaid_account_id=account["id"])
                account_found.name=account["name"].upper()
                account_found.save(update_fields=["name"])

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user)

    def list(self, request, *args, **kwargs):

        items = self.get_queryset()

        error_items = []

        for item in items:
            request = ItemGetRequest(access_token=item.access_token)
            res = plaid_client.item_get(request)
            item_error = res.get("item").get("error")
            if item_error and item.status != settings.LOGIN_REQUIRED:      #maybe change this to check the plaidapierror model
                item.status = item_error.get("error_code")
                error_items.append(item)

        if error_items:
            Item.objects.bulk_update(error_items, fields=["status"])
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=request.data["public_token"]
        )
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        request.data["access_token"] = access_token

        with transaction.atomic():
            res = super().create(request, *args, **kwargs)
            self._create_accounts(res.data.get("id"), request.data.get("accounts"))
            return res 

    def patch(self, request, *args, **kwargs):
        obj = Item.objects.get(id=request.data.get('item_id'))

        serializer = self.serializer_class(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            serializer.save()
            if request.data.get("accounts"):
                self._create_accounts(obj.id, request.data.get("accounts"))
            obj.status = settings.ACTIVE
            obj.save()

        return Response(data={"detail": "Item has been updated!"}, status=status.HTTP_200_OK)


    @action(
        detail=False,
        methods=["post"],
        url_path="refresh-all-accounts",
        name="refresh plaid accounts ",
    )
    def refresh_all_accounts(self, request, *args, **kwargs):
        task_sig = retrieve_plaid_account_data_for_user_task.delay(user_id=request.user.id)
        return Response(data={"detail": task_sig.id}, status=status.HTTP_200_OK)
    