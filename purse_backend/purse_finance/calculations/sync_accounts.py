from django.db import transaction

from purse_core.base_task import BaseTask
from purse_finance.calculations.base_calculation import BaseCalculation

from purse_finance.models import PlaidAccount, Item



class SyncPlaidAccounts(BaseCalculation, BaseTask):

    def run(self, *args, **kwargs):

        items = Item.objects.filter(user_id=self.user_id)

        with transaction.atomic():
            for item in items:
                plaid_accounts = item.get_account_data()
                for account in plaid_accounts:
                        _, created = PlaidAccount.objects.get_or_create(
                            plaid_account_id=account["account_id"],
                            defaults={
                                "user_id": self.user_id,
                                "account_type": account["type"].upper(),
                                "account_subtype": "PLAID",
                                "item": item,
                                "name": account["name"],
                            }
                        )
                        if created:
                            self.results["created"].append(f"{item.institution} -- {account['account_id']} was created.")
                        else:
                            self.results["existing"].append(f"{item.institution} -- {account['account_id']} already exists.")

        return super().run(*args, **kwargs)