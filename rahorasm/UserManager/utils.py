# here i write utils codes

from melipayamak.melipayamak import Api
#import environ for secrets and keys
import environ
env = environ.Env()
environ.Env.read_env()
def send_otp(phone, otp):
    print("in send otp")
    username = env("MELIPAYAMAK_USERNAME")
    password = env("MELIPAYAMAK_PASSWORD")
    api = Api(username, password)
    sms = api.sms()
    to = phone
    _from = '50004001971747'
    text = f'کد تایید شما: {otp}'
    print(sms.send(to, _from, text))
    print("otp sent")