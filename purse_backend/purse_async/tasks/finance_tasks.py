from celery import shared_task

from purse_async.tasks.base import BaseCeleryTask
from purse_finance.calculations import (
    RetrieveCryptoAccountValue, RetrieveCryptoAccountValueForUser,
    RetrievePlaidAccountBalance, RetrievePlaidAccountBalanceForUser, 
    NetWorthCreator, SyncPlaidAccounts
)


@shared_task(bind=True, name="calculate_networth_task", base=BaseCeleryTask)
def calculate_networth_task(self, user_id, *args, **kwargs):
    return NetWorthCreator(user_id=user_id).run()


@shared_task(bind=True, name="sync_plaid_accounts_task", base=BaseCeleryTask)
def sync_plaid_accounts_task(self, user_id, *args, **kwargs):
    return SyncPlaidAccounts(user_id=user_id).run()


@shared_task(bind=True, name="retrieve_plaid_account_balance_task", base=BaseCeleryTask)
def retrieve_plaid_account_balance_task(self, plaid_account_id, *args, **kwargs):
    return RetrievePlaidAccountBalance().run(plaid_account_id=plaid_account_id)


@shared_task(bind=True, name="retrieve_plaid_account_data_for_user_task", base=BaseCeleryTask)
def retrieve_plaid_account_data_for_user_task(self, user_id, *args, **kwargs):
    return RetrievePlaidAccountBalanceForUser().run(user_id=user_id)


@shared_task(bind=True, name="retrieve_crypto_account_value_task", base=BaseCeleryTask)
def retrieve_crypto_account_value_task(self, crypto_account_id, *args, **kwargs):
    return RetrieveCryptoAccountValue().run(crypto_account_id=crypto_account_id)


@shared_task(bind=True, name="retrieve_crypto_account_value_for_user_task", base=BaseCeleryTask)
def retrieve_crypto_account_value_for_user_task(self, user_id, *args, **kwargs):
    return RetrieveCryptoAccountValueForUser().run(user_id=user_id)


