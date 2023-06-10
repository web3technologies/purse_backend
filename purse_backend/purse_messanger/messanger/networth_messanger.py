from purse_core import BaseTask
from purse_core.services.twillio.sms import SMSSender


class NetWorthMessanger(SMSSender, BaseTask):

    def run(self, networth_data, *args, **kwargs):
        input_message = f"Your networth is: ${networth_data.get('networth')}"
        message_sid = self.send_sms(input_message=input_message)
        return message_sid