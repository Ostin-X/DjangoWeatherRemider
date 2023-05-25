import requests
import json

webhook_url = 'http://localhost/api/v1/webhook/'
token_url = 'http://localhost/api/v1/token/'
# webhook_url = 'https://webhook.site/b7614c93-7a69-425b-9c6c-40ba4c7b5c77'

login_data = {'username': 'ostin', 'password': 'scxscx'}
r = requests.post(token_url, data=json.dumps(login_data), headers={'Content-Type': 'application/json'})
access_token = r.json().get("access")

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
}
data = {'user': 'ostin', 'city': 'rome', 'time_period': '1',
        'url': 'https://webhook.site/b7614c93-7a69-425b-9c6c-40ba4c7b5c77'}

r = requests.post(webhook_url, data=json.dumps(data), headers=headers)

print(r.status_code, r.reason)
