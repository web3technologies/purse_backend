from django.db.models import Sum, F, Q
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


from purse_finance.models import PlaidTransaction
from purse_finance.serializers import IncomeExpenseSerializer


class IncomeExpenseView(APIView):


    def get(self, request, *args, **kwargs):
        
        ## add filter on is saved
        iaggregated_data = PlaidTransaction.objects \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(
            total_income=Sum('amount', filter=Q(is_income=True)),
            total_expense=Sum('amount', filter=Q(is_income=False))
        ) \
        .order_by('month')
        
        return Response(data=IncomeExpenseSerializer(iaggregated_data, many=True).data, status=HTTP_200_OK)