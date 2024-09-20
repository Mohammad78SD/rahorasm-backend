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
from ippanel import Client, Error, HTTPError, ResponseCode

def send_otp(phone, otp):
    
    client = Client("8en9TUYaGHPVU-gCdUSCCe4XxHuZhZUp62SQTIkY7ho=")
    ptrn = {
        'code': otp
        }

    client.send_pattern('zz9qp2vzfbtairt', "+983000505", str(phone), ptrn)
        
    return True

def send_sms(phone_number, ptrn):
    client = Client("8en9TUYaGHPVU-gCdUSCCe4XxHuZhZUp62SQTIkY7ho=")
    for num in phone_number:
        client.send_pattern('bxzxz3df41xdvfm', "+983000505", str(num), ptrn)