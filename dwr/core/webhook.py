import requests
import json

webhook_url = 'http://127.0.0.1:8000/webhook/'
# webhook_url = 'localhost/webhook'
# webhook_url = 'https://webhook.site/b7614c93-7a69-425b-9c6c-40ba4c7b5c77'

data = {'name': 'ostin', 'status': 'cool'}

r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

print(r.status_code, r.reason)
