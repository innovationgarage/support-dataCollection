from credentials import credentials as cred
import requests
import time

def requests_get(*arg, **kw):
    while True:
        try:
            response = requests.get(*arg, **kw)
        except Exception as e:
            print(e)
            time.sleep(5)
        else:
            if response.status_code == 200:
                return response
            if response.status_code == 401:
                raise Exception(response.content)
            print("Error %s. Sleeping 5s" % (r.status_code,))
            time.sleep(5)

def get_ticket_fields():
    url = '{}/ticket_fields.json'.format(cred['url'], )
    response = requests_get(url, auth=(cred['user'], cred['pwd']))
    return response.json()

with open("fields.json", "w") as f:
    json.dump(get_ticket_fields(), f)
