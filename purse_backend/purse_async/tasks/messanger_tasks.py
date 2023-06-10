from celery import shared_task

from purse_async.tasks.base import BaseCeleryTask
from purse_messanger.messanger import NetWorthMessanger


@shared_task(bind=True, name="send_sms_networth_task", base=BaseCeleryTask)
def send_sms_networth_task(
    self, 
    networth_data: dict, 
    user_id: int, 
    *args, 
    **kwargs
    ):
    messanger = NetWorthMessanger(user_id=user_id)
    return messanger.run(networth_data=networth_data)