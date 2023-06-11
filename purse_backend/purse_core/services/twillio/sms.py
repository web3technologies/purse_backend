from abc import ABC
from django.contrib.auth import get_user_model
from django.conf import settings
from twilio.rest import Client

from purse_messanger.models import Message


class SMSSender(ABC):

    user_model = get_user_model()

    twilio_phone_number = settings.TWILIO_PHONE_NUMBER
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def __init__(self, user_id):
        self.user = self.user_model.objects.get(id=user_id)

    def send_sms(self, input_message):

        message = self.client.messages \
                    .create(
                        body=input_message,
                        from_=self.twilio_phone_number,
                        to=self.user.phone_number.as_international
                    )
        
        Message.objects.create(
            user=self.user,
            type="SMS",
            message=input_message,
            message_id=message.sid
        )

        return message.sid