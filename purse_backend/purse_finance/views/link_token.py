from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_create_request_update import LinkTokenCreateRequestUpdate
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid import ApiClient
from plaid.api.plaid_api import PlaidApi

from purse_finance.models import PlaidAccount, Item


class LinkTokenInterface:

    _api_client = ApiClient(settings.PLAID_API_ENVIRONMENT_CONFIGURATION)
    _client = PlaidApi(_api_client)

    def get_link_token(self, user_id, product, account_id=None, item_id=None, update_accounts=False):
        
        access_token = self._get_access_token(account_id=account_id, item_id=item_id)

        params = {
            "products": [Products(product)],
            "client_name": "Plaid Test App",
            "country_codes": [CountryCode('US')],
            "redirect_uri": settings.PLAID_REDIRECT_URI,
            "language": 'en',
            "user": LinkTokenCreateRequestUser(
                client_user_id=user_id
            )
        }

        if access_token:
            params["access_token"] = access_token
        if update_accounts:
            params["update"] = LinkTokenCreateRequestUpdate(account_selection_enabled=True)

        request = LinkTokenCreateRequest(**params)
        response = self._client.link_token_create(request)

        return response

    def _get_access_token(self, item_id=None, account_id=None):
        if item_id:
            if isinstance(item_id, list):
                item_id = item_id[0]
            access_token = Item.objects.get(id=item_id).access_token
        elif account_id:
            if isinstance(account_id, list):
                account_id = account_id[0]
            access_token = PlaidAccount.objects.select_related("item").get(id=account_id).item.access_token
        else:
            return None
        return access_token


                        
class LinkTokenView(APIView, LinkTokenInterface):

	# """ This provides the view for creating the link token to connect with the plaid api """
	# permission_classes = (IsAuthenticated, )

    ''' This function handles creation of the link token'''
    ''' It is called when the user first contacts the link button to connect their account '''


    def get(self, request, *args, **kwargs):

		# This is method that is used to created the token
		# Code for it is found in plaidapi file
        token_res = self.get_link_token(str(self.request.user.id), 'transactions')
        
        return Response(data={"link_token": token_res.get("link_token")})


class LinkTokenUpdateView(APIView, LinkTokenInterface):

    def get(self, request, *args, **kwargs):
        token_res = self.get_link_token(
            str(self.request.user.id),
            'transactions',
            update_accounts=True,
            **request.query_params
        )
        return Response(data={"link_token": token_res.get("link_token")})



