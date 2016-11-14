import base64

import requests
import environ

env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env()

# CLIENT_ID = ''
# SECRET = ''
# AUTH = 'Basic ' + base64(CLIENT_ID:SECRET)

def get_token():
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    paypal_authorization = env('PAYPAL_AUTHORIZATION')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {0}'.format(paypal_authorization)
    }
    payload = {'grant_type':'client_credentials'}
    r = requests.post(url, headers=headers, data=payload)
    return r.json()['access_token']
