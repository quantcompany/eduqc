import base64

import requests

# CLIENT_ID = ''
# SECRET = ''
# AUTH = 'Basic ' + base64(CLIENT_ID:SECRET)

def get_token():
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Authorization': 'Basic QWFoNVlXVDBzS25uMndIZXNad0xQUV9TSGpGQUJ3X2lob1pfczlkcFV5SlczNlF6NmNaZkl4a0dlZW96WHpCcHZ5b0tYRE8tMk10WmxwSG06RUZ0ZzhVSmN3Z0VzejN0Qm1leW5lQmVydEtNTGxMaG1BZFJqTkotSzJUekNEQng1WTJMNl9LRGNIWHF0YVZiTTVMUkRrVGF1QTNpbXM2QVU=' # eduqc
        'Authorization': 'Basic QWR1ZEUxMDJVa3FKYzVWOHo5TE91d0JjRFoxZDBNUXNwZ2I0R2t0YXJRTnRXWWZBRGRQNVhpc2NXeDJCTHJtbW1FS3hLa3RHY2pteVJvSS06RUM4dFIwb0pNdFY1ZnFvQUlMYmpOXzdmUWhnM2Y3V0xnUkJIUkNXTWZlY083LVpRdnY2d0k5bjhQWHJ3Q0lUeE13dW5MbDVFejFWR2RYMDI=' # segunda_prueba
    }
    payload = {'grant_type':'client_credentials'}
    r = requests.post(url, headers=headers, data=payload)
    return r.json()['access_token']
