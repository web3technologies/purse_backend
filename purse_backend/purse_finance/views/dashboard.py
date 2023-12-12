import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import Case, When, Sum, Value, DecimalField, ExpressionWrapper
from django.db.models.functions import Abs
from django.utils.decorators import method_decorator
from django.utils import timezone

from plaid.exceptions import ApiException as PlaidApiException

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from purse_core.cache.cache_user import cache_user_view
from purse_core.expressions import Round, MonthName
from purse_finance.models import PlaidAccount, PlaidTransaction
from purse_finance.serializers import AggregatedAccountSerializer, LastSixMonthDataSerializer, PlaidTransactionSerializer


class DashboardView(APIView):


    def __get_stats(self, request):
        stats_query = PlaidAccount.objects.filter(user=self.request.user).aggregate(
            cash=Sum(ExpressionWrapper(Round(Case(
                When(account_type="DEPOSITORY", then='current_balance'),
                default=Value(0),
                output_field=DecimalField()
            ),2), output_field=DecimalField())),
            assets=Sum(ExpressionWrapper(Round(Case(
                When(account_type="INVESTMENT", then="current_balance"),
                default=Value(0),
                output_field=DecimalField()
            ),2), output_field=DecimalField())),
            debt=Sum(ExpressionWrapper(Round(Case(
                When(account_type__in=["CREDIT", "LOAN"], then="current_balance"),
                default=Value(0),
                output_field=DecimalField()
            ),2), output_field=DecimalField()))
        )
        stats_serializer = AggregatedAccountSerializer(data=stats_query)
        if stats_serializer.is_valid(raise_exception=True):
            stats_data = stats_serializer.data

        return {
                "cash": stats_data.get("cash"),
                "assets": stats_data.get("assets"),
                "debt": stats_data.get("debt"),
                "unsaved_transactions": PlaidTransaction.objects.filter(plaid_account__user=self.request.user, is_saved=False).count()
            }

    def __get_last_six_months_data(self, request, date_6_months_ago):
        last_six_month_qs = PlaidTransaction.objects.filter(plaid_account__user=self.request.user, date__gte=date_6_months_ago).annotate(
            month=MonthName("date")).values("month").annotate(
                income=Sum(
                    ExpressionWrapper(
                        Round(
                            Case(
                                When(is_income=True, then="amount"),
                                default=Value(0),
                                output_field=DecimalField()
                            ),
                            2
                        ),
                        output_field=DecimalField()
                    )
                ),
                expense=Sum(
                    ExpressionWrapper(
                        Round(
                            Abs(
                                Case(
                                    When(is_income=False, then="amount"),
                                    default=Value(0),
                                    output_field=DecimalField()
                                )
                            ),
                            2
                        ),
                        output_field=DecimalField()
                    )
                )
        ).order_by("month")
        last_six_month_data_serializer = LastSixMonthDataSerializer(last_six_month_qs, many=True)
        return last_six_month_data_serializer.data

    def __get_budget_data(self, transactions, today):
        budget_this_month = {}
        # initialize the values for checking
        curr_date_name_check = transactions[0].date.strftime("%b")

        for transaction in transactions:
            current_amount = transaction.amount
            transaction_date = transaction.date
            main_transaction_category = transaction.category.subcategories.first().label
            current_date_name = transaction_date.strftime("%b")
            if transaction_date.month == today.month:
                if current_amount < 0:
                    if main_transaction_category not in budget_this_month:
                        budget_this_month[main_transaction_category] = current_amount
                    else:
                        budget_this_month[main_transaction_category] -= current_amount


        budget_return_data = {
            "series": [],
            "labels": [],
        }

        for key, item in budget_this_month.items():
            budget_return_data["labels"].append(key)
            if item < 0:
                budget_return_data["series"].append(item * -1)
            else:
                budget_return_data["series"].append(item)

        return budget_return_data

    # @method_decorator(cache_user_view())
    def get(self, request, *args, **kwargs):

        today = timezone.now().today().date()
        date_6_months_ago = today - relativedelta(months=6)
        
        transactions = list(
            PlaidTransaction.objects.prefetch_related().filter(
                plaid_account__user=self.request.user, 
                date__gte=date_6_months_ago).order_by("date")
        )
        
        data = { 
            "stats": self.__get_stats(request),
            "monthly_data": self.__get_last_six_months_data(request, date_6_months_ago),
            "budget_this_month": self.__get_budget_data(transactions, today),
            "income_this_month": PlaidTransaction.objects.filter(date__year=today.year, date__month=today.month, is_income=True, plaid_account__user=self.request.user).aggregate(amount=Sum("amount")).get("amount", 0),
            "expense_this_month": PlaidTransaction.objects.filter(date__year=today.year, date__month=today.month, is_income=False, plaid_account__user=self.request.user).aggregate(amount=Sum("amount")).get("amount", 0),
            "recent_transactions": PlaidTransactionSerializer(transactions[0:5], many=True).data,
        }


        return Response(data=data, status=HTTP_200_OK)
