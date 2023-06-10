from django.conf import settings
import plaid
from plaid.api import plaid_api


_api_client = plaid.ApiClient(settings.PLAID_API_ENVIRONMENT_CONFIGURATION)
plaid_client = plaid_api.PlaidApi(_api_client)