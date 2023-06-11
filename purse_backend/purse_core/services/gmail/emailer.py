# from envelope import Envelope
# from src.settings import settings


# def send_new_email(file_buffer) -> None:

#     file_buffer.seek(0)
#     binary_data = file_buffer.read()

#     try:
#         Envelope()\
#         .from_(settings.gmail_user)\
#         .subject("Subject")\
#         .to(settings.email_to)\
#         .message("Here is your report")\
#         .attach(binary_data, name="test.xlsx")\
#         .smtp('smtp.gmail.com', 465, settings.gmail_user, settings.gmail_app_password)\
#         .send()
#         print("Email sent!")
        
#     except Exception as e:
#         print("###WARNING: EMAIL FAILED TO SEND###")
#         print(e)