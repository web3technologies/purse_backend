import datetime

from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from purse_core.cache.cache_user import cache_user_view
from purse_core.exceptions import PlaidServiceException
from purse_finance.models import PlaidAccount


class TransactionListView(APIView):
    @method_decorator(cache_user_view())
    def get(self, request):

        if date_str := request.query_params.get("start_date"):
            start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            start_date = None

        transaction_data = []

        for item in self.request.user.item_set.all():
            transaction_data.extend(item.get_transactions(start_date=start_date))
        
        transaction_data.sort(key=lambda x: x["date"], reverse=True)
            
        return Response(data=transaction_data, status=status.HTTP_200_OK)



class TransactionsByAccountView(APIView):
    @method_decorator(cache_user_view())
    def get(self, request, account_id):
        try:
            plaid_account = PlaidAccount.objects.get(id=account_id)
            transaction_data = plaid_account.get_transactions()
            transaction_data.sort(key=lambda x: x["date"], reverse=True)
            return Response(data=transaction_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(data=e.args, status=status.HTTP_400_BAD_REQUEST)
        except PlaidServiceException as e:
            return Response(data=e.args, status=status.HTTP_400_BAD_REQUEST)
        

