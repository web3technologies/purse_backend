from celery import shared_task, chain, group 
from django.contrib.auth import get_user_model

from purse_async.tasks.base import BaseCeleryTask
from purse_async.tasks.finance_tasks import calculate_networth_task, retrieve_plaid_account_transactions_for_user_task
from purse_async.tasks.messanger_tasks import send_sms_networth_task


User = get_user_model()

@shared_task(bind=True, name="calculate_all_user_networth_and_notify_task", base=BaseCeleryTask)
def calculate_all_user_networth_and_notify_task(*args, **kwargs):

    networth_calculations = group(
        [
            chain(
                calculate_networth_task.s(user_id=user.id), # result of this task is passed as an arg to send_sms.._task
                send_sms_networth_task.s(user_id=user.id)
            ) 
            for user in User.objects.all()
        ]
    )
    return networth_calculations.apply_async()


@shared_task(bind=True, name="retrieve_all_user_plaid_account_transactions_task", base=BaseCeleryTask)
def retrieve_all_user_plaid_account_transactions_task(*args, **kwargs):

    networth_calculations = group(
        [
            retrieve_plaid_account_transactions_for_user_task.s(user_id=user.id)
            for user in User.objects.all()
        ]
    )
    return networth_calculations.apply_async()