from celery import shared_task, group 

from purse_auth.models import User
from purse_async.tasks.base import BaseCeleryTask
from purse_async.tasks import (
    retrieve_plaid_account_data_for_user_task, 
    retrieve_crypto_account_value_for_user_task
)


@shared_task(bind=True, name="retrieve_plaid_account_data_for_all_users_task", base=BaseCeleryTask)
def retrieve_plaid_account_data_for_all_users_task(*args, **kwargs):

    networth_calculations = group(
        [
            retrieve_plaid_account_data_for_user_task.s(user_id=user.id)
            for user in User.objects.all()
        ]
    )
    return networth_calculations.apply_async()


@shared_task(bind=True, name="retrieve_crypto_account_value_task_for_all_users_task", base=BaseCeleryTask)
def retrieve_crypto_account_value_task_for_all_users_task(*args, **kwargs):

    networth_calculations = group(
        [
            retrieve_crypto_account_value_for_user_task.s(user_id=user.id)
            for user in User.objects.all()
        ]
    )
    return networth_calculations.apply_async()