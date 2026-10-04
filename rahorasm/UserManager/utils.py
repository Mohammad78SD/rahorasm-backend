# # here i write utils codes

# from melipayamak.melipayamak import Api
# #import environ for secrets and keys
# import environ
# env = environ.Env()
# environ.Env.read_env()
# def send_otp(phone, otp):
#     print("in send otp")
#     username = env("MELIPAYAMAK_USERNAME")
#     password = env("MELIPAYAMAK_PASSWORD")
#     api = Api(username, password)
#     sms = api.sms()
#     to = phone
#     _from = '50004001971747'
#     text = f'کد تایید شما: {otp}'
#     print(sms.send(to, _from, text))
#     print("otp sent")
    
    
    
from django.conf import settings
from ippanel import Client


def _client():
    return Client(settings.IPPANEL_API_KEY)


def send_otp(phone, otp):
    _client().send_pattern(
        settings.IPPANEL_OTP_PATTERN,
        settings.IPPANEL_ORIGINATOR,
        str(phone),
        {'code': otp},
    )
    return True


def send_sms(phone_number, ptrn):
    client = _client()
    for num in phone_number:
        client.send_pattern(
            settings.IPPANEL_NOTIFY_PATTERN,
            settings.IPPANEL_ORIGINATOR,
            str(num),
            ptrn,
        )
