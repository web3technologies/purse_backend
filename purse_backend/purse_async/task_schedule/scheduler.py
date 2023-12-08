from django.conf import settings

from purse_async.celery import app as celery_app

from .scheduler_manager import TaskScheduleManager


@celery_app.on_after_finalize.connect
def setup_task_scheduler(sender, **kwargs):
    manager = TaskScheduleManager()
    manager.delete_old_tasks()
    manager.create_scheduled_task(      # CALCULATE ALL OF THE USERS NETWORTHS
        "calculate_all_user_networth_and_notify_task", 
        settings.CALCULATE_ALL_USER_NETWORTH_AND_NOTIFY_TASK_INTERVAL,
        settings.CALCULATE_ALL_USER_NETWORTH_AND_NOTIFY_TASK_ENABLE
        )
    manager.create_scheduled_task(      # GET PLAID ACCOUNT DATA FOR ALL ACCOUNTS
        "retrieve_plaid_account_data_for_all_users_task",
        settings.RETRIEVE_PLAID_ACCOUNT_DATA_FOR_ALL_USERS_TASK_INTERVAL,
        settings.RETRIEVE_PLAID_ACCOUNT_DATA_FOR_ALL_USERS_TASK_ENABLE
    )
    manager.create_scheduled_task(      # GET CRYPTO ACCOUNT DATA FOR ALL CRYPTO ACCOUNTS
        "retrieve_all_users_crypto_account_value_task",
        settings.RETRIEVE_CRYPTO_ACCOUNT_VALUE_FOR_ALL_USERS_TASK_INTERVAL,
        settings.RETRIEVE_CRYPTO_ACCOUNT_VALUE_FOR_ALL_USERS_TASK_ENABLE
    )
    manager.create_scheduled_task(      # GET CRYPTO ACCOUNT DATA FOR ALL CRYPTO ACCOUNTS
        "retrieve_all_user_plaid_account_transactions_task",
        settings.RETRIEVE_ALL_USER_PLAID_ACCOUNT_TRANSACTIONS_TASK_INTERVAL,
        settings.RETRIEVE_ALL_USER_PLAID_ACCOUNT_TRANSACTIONS_TASK_ENABLE
    )