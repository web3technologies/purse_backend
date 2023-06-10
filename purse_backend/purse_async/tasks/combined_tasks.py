from celery import shared_task, chain, group 
from purse_auth.models import User

from purse_async.tasks.base import BaseCeleryTask
from purse_async.tasks.finance_tasks import calculate_networth_task
from purse_async.tasks.messanger_tasks import send_sms_networth_task


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