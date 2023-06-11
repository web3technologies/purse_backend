import datetime
from dateutil.relativedelta import relativedelta

from django.utils.decorators import method_decorator
from django.utils import timezone

from plaid.exceptions import ApiException as PlaidApiException

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView



from purse_core.cache.cache_user import cache_user_view


class DashboardView(APIView):

    @method_decorator(cache_user_view())
    def get(self, request, *args, **kwargs):

        today = timezone.now().today().date()
        date_6_months_ago = today - relativedelta(months=6)
        start_date = datetime.datetime.strptime(f"{date_6_months_ago.year}-{date_6_months_ago.month}-01", '%Y-%m-%d').date()
        
        transactions = []
        for item in self.request.user.item_set.all():

            try:
                transaction_data = item.get_transactions(start_date=start_date)
            except PlaidApiException:
                transaction_data = []

            transactions.extend(transaction_data)

        if not transactions:
            return Response(status=HTTP_204_NO_CONTENT)

        transactions.sort(key=lambda x: x["date"], reverse=True)

        monthly_data = []
        budget_this_month = {}
        income_this_month = 0
        expense_this_month = 0
        total_income = 0
        total_expense = 0
        largest_expense = 0
        largest_bar_value = 0

        # initialize the values for checking
        curr_date_name_check = transactions[0].get("date").strftime("%b")
        current_income_amount = 0
        current_expense_amount = 0

        for transaction in transactions:

            current_amount = transaction.get("amount")
            transaction_date = transaction.get("date")
            main_transaction_category = transaction.get("category")[0]

            # do not include credit card payments in count of income and expense
            # it will be read as an income item so need to remove
            # find a solution for this
            if "AMEX" in transaction.get("name") or "ONLINE PAYMENT - THANK YOU" in transaction.get("name"):
                continue

            current_date_name = transaction_date.strftime("%b")

            # if the transaction date is this year then handle
            if transaction_date.year == today.year:
                if current_amount < 0:
                    total_expense -= current_amount
                    if transaction_date.month == today.month:
                        expense_this_month -= current_amount

                    if current_amount * -1 > largest_expense:
                        largest_expense = current_amount * -1
                    
                else:
                    total_income += current_amount
                    if transaction_date.month == today.month:
                        income_this_month += current_amount

            if transaction_date.month == today.month:
                if current_amount < 0:
                    if main_transaction_category not in budget_this_month:
                        budget_this_month[main_transaction_category] = current_amount
                    else:
                        budget_this_month[main_transaction_category] -= current_amount

            # if the current month 
            if current_date_name == curr_date_name_check:
                if current_amount < 0:
                    current_expense_amount -= current_amount
                else:
                    current_income_amount += current_amount
            else:
                monthly_data.append(
                    {
                        "month": curr_date_name_check, 
                        "income": current_income_amount, 
                        "expense": current_expense_amount
                    }
                )

                # block of code to set the largest bar value amount
                if current_income_amount < current_expense_amount:
                    largest_value_bar_check = current_expense_amount
                else:
                    largest_value_bar_check = current_income_amount
                if largest_bar_value < largest_value_bar_check:
                    largest_bar_value = largest_value_bar_check 

                #reset the monthly data for checking
                ## todo find out if need to set value as current_amount or 0
                curr_date_name_check = current_date_name
                if current_amount < 0 :
                    current_income_amount = 0
                    current_expense_amount = current_amount
                else:
                    current_income_amount = current_amount
                    current_expense_amount = 0

        monthly_data.reverse()

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

        data = {
            "yearly":{
                "income": total_income,
                "expense": total_expense,
                "largest_expense": largest_expense,
                "total_transactions": len(transactions)
            },
            "monthly_data":monthly_data,
            "budget_this_month": budget_return_data,
            "income_this_month": income_this_month,
            "expense_this_month": expense_this_month,
            "recent_transactions":transactions[0:5],
            "largest_bar_value": largest_bar_value
        }


        return Response(data=data, status=HTTP_200_OK)