from purse_async.tasks.finance_tasks import *
from purse_async.tasks.grouped_tasks import *
from purse_async.tasks.messanger_tasks import *
from purse_async.tasks.combined_tasks import *
from purse_async.task_schedule import setup_task_scheduler


_finance_tasks = [
    "calculate_networth_task",
    "calculate_all_user_networth_and_notify_task",  # function located in combined task
    "retrieve_crypto_account_value_task",
    "retrieve_crypto_account_value_for_user_task",
    "retrieve_crypto_account_value_for_all_users_task",
    "retrieve_plaid_account_data_for_user_task",
    "retrieve_plaid_account_data_for_all_users_task",
    "retrieve_plaid_account_balance_task",
    "retrieve_plaid_account_transactions_task",
    "retrieve_plaid_account_transactions_for_user_task",
    "retrieve_all_user_plaid_account_transactions_task",
    "sync_plaid_accounts_task"
]

_messanger_tasks = [
    "send_sms_networth_task"
]

__all__ = [
    "setup_task_scheduler",
    *_finance_tasks,
    *_messanger_tasks
]