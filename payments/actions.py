import json

import requests

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import reverse

from payments.auth import get_token


def create_payment(request, transaction):
    # url = 'https://api.sandbox.paypal.com/v1/payments/payment'
    url = 'https://api.paypal.com/v1/payments/payment'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_token()
    }

    payload = {
        'intent': 'sale',
        'redirect_urls':
            {
                'return_url': 'http://{0}{1}'.format(get_current_site(request), reverse('payments:execute')),
                'cancel_url': 'http://{0}{1}'.format(get_current_site(request), reverse('payments:cancel'))
            },
        'payer':
            {
                'payment_method': 'paypal'
            },
        'transactions': [transaction]
    }

    return requests.post(url, headers=headers, data=json.dumps(payload))


def execute_payment(request, payment_id, payer_id, enrollment_id):
    # url = 'https://api.sandbox.paypal.com/v1/payments/payment/{0}/execute/'.format(payment_id)
    url = 'https://api.paypal.com/v1/payments/payment/{0}/execute/'.format(payment_id)

    headers = {
        # 'PayPal-Request-Id': str(enrollment_id),
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_token()
    }

    payload = {
        'payer_id': payer_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    # print('****************************')
    # print(token)
    # print(payment_id)
    # print(payer_id)
    # print(response.status_code)
    # print(response.text)
    return response
    # print(r)
    # print(r.json())
    #
    # for link in r.json()['links']:
    #     if link['rel'] == 'approval_url':
    #         return HttpResponseRedirect(redirect_to=link['href'])

    # return HttpResponse('Approval Failed')
